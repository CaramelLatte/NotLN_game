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
      self.x = x
      self.y = y
      self.hp = hp
      self.max_hp = hp
      self.i_frames = 0
      self.is_hit = False
      self.enemies_killed = 0
      self.shot_cd = 0
      self.under_potion = False
      self.potion_effect = ""
      self.potion_timer = 300
      self.fire_rate = 1
      self.shot_size = 1
      self.damage = 1
      self.exp = 0
      self.level = 1
      self.xp_to_level = 10
      self.skill_points = 0
      self.gun = {
        "spray" : False,
        "beam" : False,
        "flame" : False,
        "pierce" : False
      }
      self.skills = {
        "revive" : False,
        "freeze" : False,
        "reflect" : False,
      }

    def collided(self, rect):
      return self.rect.colliderect(rect)
    def draw(self, surface):
      pygame.draw.rect(surface, self.color, self.rect)
      

  class Bullet(Entity):
    def __init__(self, color, x, y, width, height, speed, hp, targetx, targety, damage):
        super().__init__(color, x, y, width, height, speed, hp)
        #self.rect = pygame.Rect(x, y, width, height)
        angle = math.atan2(targety-y, targetx-x)
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y
        self.damage = damage
        self.pierce = 0

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


  class Enemy(Entity):
    def __init__(self, color, x, y, width, height, speed, hp, bullet_speed, shot_damage, collide_damage, can_fire, exp, behavior):
      super().__init__(color, x, y, width, height, speed, hp)
      self.rect = pygame.Rect(x, y, width, height)
      self.bullet_speed = bullet_speed
      self.shot_damage = shot_damage
      self.collide_damage = collide_damage
      self.can_fire = can_fire
      self.behavior = behavior
      self.direction = ""
      self.exp = exp
      self.boss = False
      self.dx = 0
      self.dy = 0
      self.dist = 0
      self.hit = []

    def force_onscreen(self):
      if self.rect.x <= 0:
        self.rect.x = 0
      if self.rect.x >= 1004:
        self.rect.x = 1004
      if self.rect.y <= 0:
        self.rect.y = 0
      if self.rect.y >= 598:
        self.rect.y = 598

        
    def move(self):
        angle = math.atan2(player.rect.y-self.y, player.rect.x-self.x)
        self.dx = math.cos(angle)*self.speed
        self.dy = math.sin(angle)*self.speed
        self.dist = math.hypot(self.x-player.rect.x, self.y-player.rect.y)
        if self.behavior == "rush":
          self.x = self.x + self.dx
          self.y = self.y + self.dy
          self.rect.x = int(self.x)
          self.rect.y = int(self.y)
        elif self.behavior == "snipe":
          if int(self.dist) <= 400:
            self.x = self.x - self.dx
            self.y = self.y - self.dy
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
          else:
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
        elif self.behavior == "flank":
          if self.direction == "":
            pick_dir = random.randint(0, 1)
            if pick_dir == 0:
              self.direction = "left"
            else:
              self.direction = "right"
            print(self.direction)
          if self.direction == "left":
            flank_angle = math.atan2(player.rect.y-self.y, player.rect.x-self.x) + 5
            self.dx = math.cos(flank_angle)*self.speed
            self.dy = math.sin(flank_angle)*self.speed
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
          else:
            flank_angle = math.atan2(player.rect.y-self.y, player.rect.x-self.x) - 5
            self.dx = math.cos(flank_angle)*self.speed
            self.dy = math.sin(flank_angle)*self.speed
            self.x = self.x + self.dx
            self.y = self.y + self.dy
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
        self.force_onscreen()

    def hit_by(self, bullet):
      self.hit.append(bullet)
      return self.hit


  class Loot(Entity):
    def __init__(self, color, x, y, width, height, speed, hp, type) -> None:
      super().__init__(color, x, y, width, height, speed, hp)
      self.type = type

  class Toast:
      def __init__(self, text, x, y) -> None:
          self.text = text
          self.duration = 720
          self.x = x
          self.y = y
          self.surface = stat_font.render(self.text, False, (236, 236, 236), (108, 132, 137))
          self.rectangle = self.surface.get_rect(midright=(self.x, self.y))
          self.done = False
          self.hover = 240

      def move(self):
        if self.rectangle.midtop[1] < 0 and self.hover > 0:
          self.rectangle.y += 1
        else:
          self.hover -= 1
          if self.hover <= 0:
            self.rectangle.y -= 1
            if self.rectangle.midbottom[1] <= (0 - self.rectangle.height):
              self.done = True
        
      def draw(self):
        screen.blit(self.surface, self.rectangle)

  #global variables
  screen_width = 1024
  screen_height = 768
  screen = pygame.display.set_mode((screen_width, screen_height))
  pygame.display.set_caption("Night of the Living Nerds")
  clock = pygame.time.Clock()
  font = pygame.font.SysFont("Arial", 50)
  stat_font = pygame.font.SysFont("Arial", 20)

  game_active = True
  bullets = []
  enemies = []
  enemy_bullets = []
  loot = []
  boss_spawned = False
  player = Entity((0,0,0), 100, 100, 20, 20, 5, 10000 )
  difficulty = 1
  toast_list = []

  pygame.mouse.set_pos([int(screen_width / 2), int(screen_height / 2)])

  #Enemy spawning begins here
  def spawn_enemies():
      enemy_spawn = random.randint(0, 100)
      if enemy_spawn > 1 and enemy_spawn < (1 + (difficulty * 2)):
        enemy_spawnx = 0
        enemy_spawny = 0
        spawn_wall = random.randint(1, 4)
        if spawn_wall == 1:
          enemy_spawnx = 50
          enemy_spawny = random.randint(50, 568)
        elif spawn_wall == 2:
          enemy_spawnx = 984
          enemy_spawny = random.randint(50, 568)
        elif spawn_wall == 3:
          enemy_spawny = 50
          enemy_spawnx = random.randint(50, 984)
        else:
          enemy_spawny = 568
          enemy_spawnx = random.randint(50, 984)

        enemy_type = random.randint(1, 100)
        if player.enemies_killed <= 99:
          if enemy_type <= 20:
            e = Enemy((255, 255 ,255), enemy_spawnx, enemy_spawny, 15, 15, 1, 3, 5, 1, 1, True, 1, "snipe")
          elif enemy_type > 20 and enemy_type <= 50:
            e = Enemy((255,0,0), enemy_spawnx, enemy_spawny, 15, 15, 3, 1, 5, 1, 1, False, 1, "rush")
          elif enemy_type >  50 and enemy_type <= 80:
            e = Enemy((0, 0,255), enemy_spawnx, enemy_spawny, 15, 15, 2, 2, 5, 1, 1, True, 1, "flank")
          elif enemy_type > 80:
            e = Enemy((0,0,0), enemy_spawnx, enemy_spawny, 15, 15, 2, 5, 1, 1, 1, False, 1, "rush")
          enemies.append(e)

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
    if spawn_wall == 1:
      enemy_spawnx = 50
      enemy_spawny = random.randint(50, 568)
    elif spawn_wall == 2:
      enemy_spawnx = 984
      enemy_spawny = random.randint(50, 568)
    elif spawn_wall == 3:
      enemy_spawny = 50
      enemy_spawnx = random.randint(50, 984)
    else:
      enemy_spawny = 568
      enemy_spawnx = random.randint(50, 984)

    e = Enemy((0,128,0), enemy_spawnx, enemy_spawny, 40, 40, 4, 50, 10, 2, 3, True, 5, "rush")
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
          player.i_frames = 0
          player.is_hit = False
          player.enemies_killed = 0
          boss_spawned = False
          player.shot_cd = 0
          player = Entity((0,0,0), 100, 100, 20, 20, 5, 10)
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
            player.skill_points -= 1
          else:
            pass
        #box 3
        if ui_3.collidepoint(event.pos):
          if player.damage <= 2 and player.skill_points >= 1:
            player.damage += 1
            player.skill_points -= 1
          else:
            pass
        #box 4
        if ui_4.collidepoint(event.pos):
          if player.skill_points >= 3 and player.gun["spray"] == False:
            player.gun["spray"] = True
            player.skill_points -= 3
        
    if game_active:
        #game loop drawing
        screen.fill((192, 232, 236))
        player.draw(screen)
        ui_rectangle = pygame.Rect(0, 618, 1024, 150) 
        pygame.draw.rect(screen, (255, 255 ,255), ui_rectangle)
        ui_1 = pygame.Rect(0, 618, 256, 150)
        pygame.draw.rect(screen, (0, 0,255), ui_1)
        pygame.draw.rect(screen, (0,0,0), ui_1, 1)


        ui_2 = pygame.Rect(256, 618, 256, 150)
        hp_surface = stat_font.render(f"HP: {player.hp}/{player.max_hp}", False, (0, 0, 0))
        hp_rectangle = hp_surface.get_rect(midleft = (10, 640))
        level_surface = stat_font.render(f"Lvl: {player.level}", False, (0, 0, 0))
        level_rectangle = level_surface.get_rect(midleft = (10, 670))
        sp_surface = stat_font.render(f"SP: {player.skill_points}", False, (0, 0, 0))
        sp_rectangle = sp_surface.get_rect(midleft = (10, 700))
        pygame.draw.rect(screen, (0, 0,255), ui_2)
        pygame.draw.rect(screen, (0,0,0), ui_2, 1)
        screen.blit(hp_surface, hp_rectangle)
        screen.blit(level_surface, level_rectangle)
        screen.blit(sp_surface, sp_rectangle)

        ui_3 = pygame.Rect(512, 618, 256, 150)
        pygame.draw.rect(screen, (0, 0,255), ui_3)
        pygame.draw.rect(screen, (0,0,0), ui_3, 1)

        ui_4 = pygame.Rect(768, 618, 256, 150)
        pygame.draw.rect(screen, (0, 0,255), ui_4)
        pygame.draw.rect(screen, (0,0,0), ui_4, 1)

        # screen.blit(text_surface, text_rectangle)
        pygame.draw.line(screen, (0,0,0), player.rect.center, pygame.mouse.get_pos())
        
        if len(toast_list) >= 1:
          toast_list[0].move()
          toast_list[0].draw()
          if toast_list[0].done == True:
            toast_list.pop(0)


        player.i_frames -= 1
        if player.i_frames <= 0:
          player.is_hit = False
        if player.shot_cd > 0:
          player.shot_cd -= player.fire_rate
        if player.under_potion == True:
          player.potion_timer -= 1
          if player.potion_timer == 0:
            if player.potion_effect == "speed":
              player.speed -= 4
            player.potion_effect = ""
            player.under_potion = False
            player.potion_timer = 300

        #movement handling, arrows and wasd
        keys = pygame.key.get_pressed()
        if player.potion_effect == "speed":
          player.rect.x += 2*(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player.speed
          player.rect.x += 2*(keys[pygame.K_d] - keys[pygame.K_a]) * player.speed
        else:
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
        if pygame.mouse.get_pressed()[0] and player.shot_cd <= 0:
          player.shot_cd = 20
          x,y = pygame.mouse.get_pos()
          b = Bullet((0,0,0), player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x, y, player.damage)
          if player.gun["pierce"] == True:
            b.pierce += 1
          bullets.append(b)
          if player.gun["spray"] == True:
            b1 = Bullet((0,0,0), player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x + 30, y + 30, player.damage)
            b2 = Bullet((0,0,0), player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x - 30, y - 30, player.damage)
            if player.gun["pierce"] == True:
              b1.pierce = 1
              b2.pierce = 1
            bullets.extend([b1, b2])
        
        #conditional enemy spawns, spawn boss every 20 kills
        if player.skills["freeze"] == False:
          if boss_spawned == False and player.enemies_killed <= 19:
            spawn_enemies()
          elif boss_spawned == False and player.enemies_killed >= 20:
            spawn_boss()
            player.enemies_killed = 0
            boss_spawned = True
        #boss killed
        if len(enemies) == 0 and boss_spawned == True:
          boss_spawned = False
          difficulty += 1
          if player.max_hp - player.hp <= 3:
            player.hp = player.max_hp
          else: 
            player.hp += 3

        #enemy hit check, loot drop test
        for b in reversed(range(len(bullets))):
          for e in reversed(range(len(enemies))):
            if bullets[b].collided(enemies[e].rect):
              if bullets[b] in enemies[e].hit:
                break
              else:
                enemies[e].hit.append(bullets[b])
              enemies[e].hp -= bullets[b].damage
              if bullets[b].pierce < 1:
                del bullets[b]
              else:
                bullets[b].pierce -= 1
              if enemies[e].hp <= 0:
                player.exp += enemies[e].exp
                loot_chance = random.randint(1, 10)
                if loot_chance == 1:
                  drop_type = random.randint(1, 2)
                  if drop_type == 1:
                    drop = Loot((255,0,255), enemies[e].x, enemies[e].y, 10, 10, 0, 0, "hp")
                  elif drop_type == 2:
                    drop = Loot((0,128,0), enemies[e].x, enemies[e].y, 10, 10, 0, 0, "speed")
                  
                  loot.append(drop)
                player.enemies_killed += 1
                del enemies[e]
              break

        #collision detection for all entities, draw enemies and bullets
        for e in reversed(range(len(enemies))):
          if player.collided(enemies[e].rect):
            if player.i_frames <= 0 and player.is_hit == False:
              player.hp -= enemies[e].collide_damage
              enemies[e].hp -= 1
              if enemies[e].hp <= 0:
                del enemies[e]
                player.enemies_killed += 1
              player.is_hit = True
              player.i_frames = 15
              if player.hp <= 0:
                game_active = False

        for b in enemy_bullets:
          if player.collided(b) and player.is_hit == False:
            player.hp -= b.damage
            enemy_bullets.remove(b)
            player.is_hit = True
            player.i_frames = 15
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
          e.draw(screen)
          if player.skills["freeze"] == False:
            e.move()

            if e.boss == False:
              shoot = random.randint(1, 100)
              if shoot <=1 and e.can_fire == True:
                x,y = player.rect.centerx, player.rect.centery
                b = Bullet((255,165,0), e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx, player.rect.centery, e.shot_damage)
                enemy_bullets.append(b)
            elif e.boss == True:
              shoot = random.randint(1, 60)
              if shoot == 1:
                x,y = player.rect.centerx, player.rect.centery
                b = Bullet((255,165,0), e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx, player.rect.centery, e.shot_damage)
                b1 = Bullet((255,165,0), e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx + 30, player.rect.centery + 30, e.shot_damage)
                b2 = Bullet((255,165,0), e.rect.centerx, e.rect.centery, 5, 5, e.bullet_speed, 1, player.rect.centerx - 30, player.rect.centery - 30, e.shot_damage)
                enemy_bullets.extend([b, b1, b2])

          

        for b in enemy_bullets:
          b.draw(screen)
          b.move()
          if b.x <= -50 or b.x >= 1074:
            enemy_bullets.remove(b)
          elif b.y <= -50 or b.rect.midbottom[1] >= 618:
            enemy_bullets.remove(b)

        while player.exp >= player.xp_to_level:
          player.level += 1
          player.max_hp += 1
          player.exp -= player.xp_to_level
          player.skill_points += 1
          player.xp_to_level = int(player.xp_to_level * 1.3)
          toast = Toast(f"Leveled up! You are level {player.level} with {player.skill_points} SP.", 1024, -50)
          toast_list.append(toast)

        for drop in loot:
          drop.draw(screen)
          if player.collided(drop):
            if drop.type == "hp":
              if player.max_hp - player.hp < 2:
                player.hp = player.max_hp
              else:
                player.hp += 2
            if drop.type == "speed" and not player.under_potion:
              player.under_potion = True
              player.speed += 4
              player.potion_effect = drop.type
            loot.remove(drop)

    else:
      screen.fill("#c0e8ec")
      text_surface = font.render(f"Level: {player.level}/{player.max_hp}, Skill Points: {player.skill_points}", False, (64,64,64)).convert()
      text_rectangle = text_surface.get_rect(center = (screen.get_width() /2, 50))
      screen.blit(text_surface, text_rectangle)
      game_over_surface = font.render("Game over!", False, (255,0,0))
      game_over_rectangle = game_over_surface.get_rect(center = (screen.get_width() /2 , screen.get_height() /2))
      restart_prompt_surface = font.render("Press space to restart", False, (0,0,0))
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
    