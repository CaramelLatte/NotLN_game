import pygame
import math
import random
from sys import exit

def main():
  pygame.init()

  class Entity:
    def __init__(self, color, x, y, width, height, speed, hp):
      self.rect = pygame.Rect(x, y, width, height)
      self.color = color
      self.speed = speed
      self.hp = hp
      self.x = x
      self.y = y
      self.fire_rate = 1
      self.shot_size = 1
      self.damage = 1
      self.exp = 0
      self.level = 1
      self.skill_points = 0
      self.skills = {
        "spray" : False
      }
    def collided(self, rect):
      return self.rect.colliderect(rect)
    def draw(self, surface):
      pygame.draw.rect(surface, self.color, self.rect)
      

  class Bullet(Entity):
    def __init__(self, color, x, y, width, height, speed, hp, targetx, targety, damage):
        super().__init__(color, x, y, width, height, speed, hp)
        self.rect = pygame.Rect(x, y, width, height)
        angle = math.atan2(targety-y, targetx-x)
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y
        self.damage = damage
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


  class Enemy(Entity):
    def __init__(self, color, x, y, width, height, speed, hp, bullet_speed, shot_damage, collide_damage, can_fire, exp):
      super().__init__(color, x, y, width, height, speed, hp)
      self.rect = pygame.Rect(x, y, width, height)
      self.bullet_speed = bullet_speed
      self.shot_damage = shot_damage
      self.collide_damage = collide_damage
      self.can_fire = can_fire
      self.exp = exp
      self.boss = False
      self.dx = 0
      self.dy = 0
    def move(self):
      angle = math.atan2(player.rect.y-self.y, player.rect.x-self.x)
      self.dx = math.cos(angle)*self.speed
      self.dy = math.sin(angle)*self.speed
      self.x = self.x + self.dx
      self.y = self.y + self.dy
      self.rect.x = int(self.x)
      self.rect.y = int(self.y)

  #global variables
  screen_width = 1024
  screen_height = 768
  screen = pygame.display.set_mode((screen_width, screen_height))
  pygame.display.set_caption("Night of the Living Nerds")
  clock = pygame.time.Clock()
  font = pygame.font.Font(None, 50)
  score = 0

  game_active = True
  bullets = []
  enemies = []
  enemy_bullets = []
  i_frame = 0
  is_hit = False
  enemies_killed = 0
  boss_spawned = False
  shot_cd = 0
  player = Entity("black", 100, 100, 20, 20, 5, 10 )
  difficulty = 1

  #Enemy spawning begins here
  def spawn_enemies():
      enemy_spawn = random.randint(0, 100)
      if enemy_spawn > 1 and enemy_spawn < (3 + difficulty):
        enemy_spawnx = 0
        enemy_spawny = 0
        spawn_wall = random.randint(1, 4)
        match spawn_wall:
          case 1:
            enemy_spawnx = 50
            enemy_spawny = random.randint(50, 568)
          case 2:
            enemy_spawnx = 984
            enemy_spawny = random.randint(50, 568)
          case 3:
            enemy_spawny = 50
            enemy_spawnx = random.randint(50, 984)
          case 4:
            enemy_spawny = 568
            enemy_spawnx = random.randint(50, 984)

        enemy_type = random.randint(1, 3)
        if enemies_killed <= 99:
          match enemy_type:
            case 1:
              e = Enemy("white", enemy_spawnx, enemy_spawny, 15, 15, 1, 3, 5, 1, 1, True, 1)
              enemies.append(e)
              return
            case 2:
              e = Enemy("red", enemy_spawnx, enemy_spawny, 15, 15, 3, 1, 5, 1, 1, False, 1)
              enemies.append(e)
              return
            case 3:
              e = Enemy("blue", enemy_spawnx, enemy_spawny, 15, 15, 2, 2, 5, 1, 1, True, 1)
              enemies.append(e)
              return

  def spawn_boss():
    while len(enemies) > 0:
      for e in enemies:
        enemies.remove(e)
    while len(enemy_bullets) > 0:
      for eb in enemy_bullets:
        enemy_bullets.remove(eb)
    enemy_spawnx = 0
    enemy_spawny = 0
    spawn_wall = random.randint(1, 4)
    match spawn_wall:
      case 1:
        enemy_spawnx = 50
        enemy_spawny = random.randint(50, 568)
      case 2:
        enemy_spawnx = 984
        enemy_spawny = random.randint(50, 568)
      case 3:
        enemy_spawny = 50
        enemy_spawnx = random.randint(50, 984)
      case 4:
        enemy_spawny = 568
        enemy_spawnx = random.randint(50, 984)
    e = Enemy("Green", enemy_spawnx, enemy_spawny, 40, 40, 4, 50, 10, 3, 3, True, 5)
    e.boss = True
    enemies.append(e)

  #main loop
  while True:
    pygame.event.set_grab(True)
    #event handling
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          exit()
      if event.type == pygame.KEYDOWN and game_active == False:
        if event.key == pygame.K_SPACE:
          game_active = True
          i_frame = 0
          is_hit = False
          enemies_killed = 0
          boss_spawned = False
          shot_cd = 0
          player = Entity("black", 100, 100, 20, 20, 5, 10 )
          difficulty = 1
          for e in reversed(range(len(enemies))):
            del enemies[e]
        for b in reversed(range(len(bullets))):
            del bullets[b]

      #Click detection for UI elements
      if event.type == pygame.MOUSEBUTTONDOWN:
        #box 1
        if ui_1.collidepoint(event.pos):
          if player.fire_rate <= 2 and player.skill_points >= 1:
            player.fire_rate += 1
            player.skill_points -= 1
          else:
            pass
        #box 2
        if ui_2.collidepoint(event.pos):
          if player.shot_size < 2 and player.skill_points >= 1:
            player.shot_size += 1
          else:
            pass
        #box 3
        if ui_3.collidepoint(event.pos):
          if player.damage <= 2 and player.skill_points >= 1:
            player.damage += 1
          else:
            pass
        #box 4
        if ui_4.collidepoint(event.pos):
          if player.skill_points >= 3 and player.skills["spray"] == False:
            player.skills["spray"] = True
            player.skill_points -= 3
        
    if game_active:
        #game loop drawing
        screen.fill("#c0e8ec")
        player.draw(screen)
        text_surface = font.render(f"Level: {player.level}, Skill Points: {player.skill_points}", False, (64,64,64)).convert()
        text_rectangle = text_surface.get_rect(center = (screen.get_width() /2, 50))
        ui_rectangle = pygame.Rect(0, 618, 1024, 150) 
        pygame.draw.rect(screen, "white", ui_rectangle)
        ui_1 = pygame.Rect(0, 618, 256, 150)
        pygame.draw.rect(screen, "Blue", ui_1)
        pygame.draw.rect(screen, "Black", ui_1, 1)
        ui_2 = pygame.Rect(256, 618, 256, 150)
        pygame.draw.rect(screen, "Blue", ui_2)
        pygame.draw.rect(screen, "Black", ui_2, 1)
        ui_3 = pygame.Rect(512, 618, 256, 150)
        pygame.draw.rect(screen, "Blue", ui_3)
        pygame.draw.rect(screen, "Black", ui_3, 1)
        ui_4 = pygame.Rect(768, 618, 256, 150)
        pygame.draw.rect(screen, "Blue", ui_4)
        pygame.draw.rect(screen, "Black", ui_4, 1)
        screen.blit(text_surface, text_rectangle)
        pygame.draw.line(screen, 'black', player.rect.center, pygame.mouse.get_pos())

        i_frame -= 1
        if i_frame <= 0:
          is_hit = False
        if shot_cd > 0:
          shot_cd -= player.fire_rate

        #movement handling, arrows and wasd
        keys = pygame.key.get_pressed()
        player.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player.speed
        player.rect.x += (keys[pygame.K_d] - keys[pygame.K_a]) * player.speed
        if player.rect.x <= 0:
          player.rect.x = 0
        if player.rect.x >= 1004:
          player.rect.x = 1004
        player.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player.speed
        player.rect.y += (keys[pygame.K_s] - keys[pygame.K_w]) * player.speed
        if player.rect.y <= 0:
          player.rect.y = 0
        if player.rect.y >= 598:
          player.rect.y = 598

        #left click shooting
        if pygame.mouse.get_pressed()[0] and shot_cd <= 0:
          shot_cd = 20
          x,y = pygame.mouse.get_pos()
          b = Bullet("black", player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x, y, player.damage)
          bullets.append(b)
          if player.skills["spray"] == True:
            b1 = Bullet("black", player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x + 30, y + 30, player.damage)
            b2 = Bullet("black", player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x - 30, y - 30, player.damage)
            bullets.append(b1)
            bullets.append(b2)
        
        #conditional enemy spawns, spawn boss every 20 kills
        if boss_spawned == False and enemies_killed <= 19:
          spawn_enemies()
        elif boss_spawned == False and enemies_killed >= 20:
          spawn_boss()
          enemies_killed = 0
          boss_spawned = True
        if len(enemies) == 0 and boss_spawned == True:
          boss_spawned = False
          difficulty += 1
        for b in reversed(range(len(bullets))):
          for e in reversed(range(len(enemies))):
            if bullets[b].collided(enemies[e].rect):
              enemies[e].hp -= bullets[b].damage
              del bullets[b]
              if enemies[e].hp <= 0:
                player.exp += enemies[e].exp
                print(player.exp)
                del enemies[e]
                enemies_killed += 1
              score += 10
              break

        #collision detection for all entities, draw enemies and bullets
        for e in reversed(range(len(enemies))):
          if player.collided(enemies[e].rect):
            if i_frame <= 0 and is_hit == False:
              player.hp -= enemies[e].collide_damage
              enemies[e].hp -= 1
              if enemies[e].hp <= 0:
                del enemies[e]
                enemies_killed += 1
              is_hit = True
              i_frame = 15
              if player.hp <= 0:
                game_active = False

        for b in enemy_bullets:
          if player.collided(b) and is_hit == False:
            player.hp -= b.damage
            enemy_bullets.remove(b)
            is_hit = True
            i_frame = 15
            if player.hp <= 0:
              game_active = False

        for b in reversed(range(len(bullets))):
          bullets[b].move()
          bullets[b].draw(screen)
          if bullets[b].x <= -50 or bullets[b].x >= 1074:
            del bullets[b]
          elif bullets[b].y <= -50 or bullets[b].rect.midbottom[1] >= 618:
            del bullets[b]

        for e in enemies:
          e.move()
          e.draw(screen)
          if e.boss == False:
            shoot = random.randint(1, 100)
            if shoot <=2 and e.can_fire == True:
              x,y = player.rect.centerx, player.rect.centery
              b = Bullet("Orange", e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx, player.rect.centery, e.shot_damage)
              enemy_bullets.append(b)
          elif e.boss == True:
            shoot = random.randint(1, 20)
            if shoot == 1:
              x,y = player.rect.centerx, player.rect.centery
              b = Bullet("Orange", e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx, player.rect.centery, e.shot_damage)
              b1 = Bullet("Orange", e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx + 30, player.rect.centery + 30, e.shot_damage)
              b2 = Bullet("Orange", e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx - 30, player.rect.centery - 30, e.shot_damage)
              enemy_bullets.append(b)
              enemy_bullets.append(b1)
              enemy_bullets.append(b2)

          

        for b in enemy_bullets:
          b.draw(screen)
          b.move()
          if b.x <= -50 or b.x >= 1074:
            enemy_bullets.remove(b)
          elif b.y <= -50 or b.rect.midbottom[1] >= 618:
            enemy_bullets.remove(b)
        while player.exp >= 10:
          player.level += 1
          player.exp -= 10
          player.skill_points += 1
          print("Level up! Got a skill point")

    else:
      screen.fill("#c0e8ec")
      text_surface = font.render(f"Level: {player.level}, Skill Points: {player.skill_points}", False, (64,64,64)).convert()
      text_rectangle = text_surface.get_rect(center = (screen.get_width() /2, 50))
      screen.blit(text_surface, text_rectangle)
      game_over_surface = font.render("Game over!", False, "red")
      game_over_rectangle = game_over_surface.get_rect(center = (screen.get_width() /2 , screen.get_height() /2))
      restart_prompt_surface = font.render("Press space to restart", False, "black")
      restart_prompt_rectangle = restart_prompt_surface.get_rect(center = (screen.get_width() / 2, screen.get_height() - 100))
      screen.blit(game_over_surface, game_over_rectangle)
      screen.blit(restart_prompt_surface, restart_prompt_rectangle)
      for e in enemies:
        enemies.remove(e)
      for b in bullets:
        bullets.remove(b)
      for eb in enemy_bullets:
        enemy_bullets.remove(eb)
    pygame.display.update()
    clock.tick(60)
  
if __name__ == "__main__":
  main()