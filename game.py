import pygame
import math
import random
from sys import exit
def main():
  pygame.init()

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
  i_frame = 0
  is_hit = False

  def spawn_enemies():
    enemy_spawn = random.randint(0, 100)
    if enemy_spawn > 1 and enemy_spawn < 5:
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
      match enemy_type:
        case 1:
          e = Enemy("white", enemy_spawnx, enemy_spawny, 15, 15, 1, 3)
          enemies.append(e)
          return
        case 2:
          e = Enemy("red", enemy_spawnx, enemy_spawny, 15, 15, 3, 1)
          enemies.append(e)
          return
        case 3:
          e = Enemy("blue", enemy_spawnx, enemy_spawny, 15, 15, 2, 2)
          enemies.append(e)
          return         
  

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
      self.spray = False

    def collided(self, rect):
      return self.rect.colliderect(rect)
    def draw(self, surface):
      pygame.draw.rect(surface, self.color, self.rect)
      

  class Bullet(Entity):
    def __init__(self, color, x, y, width, height, speed, hp, targetx, targety):
        super().__init__(color, x, y, width, height, speed, hp)
        self.rect = pygame.Rect(x, y, width, height)
        angle = math.atan2(targety-y, targetx-x)
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


  class Enemy(Entity):
    def __init__(self, color, x, y, width, height, speed, hp):
      super().__init__(color, x, y, width, height, speed, hp)
      self.rect = pygame.Rect(x, y, width, height)

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




  player = Entity("black", 100, 100, 20, 20, 5, 10 )
  shot_cd = 0
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.KEYDOWN and game_active == False:
        if event.key == pygame.K_SPACE:
          game_active = True
          player.hp = 10
          score = 0
          for e in reversed(range(len(enemies))):
            del enemies[e]
        for b in reversed(range(len(bullets))):
            del bullets[b]
      if event.type == pygame.MOUSEBUTTONDOWN:
        #box 1
        if ui_1.collidepoint(event.pos):
          if player.fire_rate <= 2:
            player.fire_rate += 1
          else:
            player.fire_rate = 1

        if ui_2.collidepoint(event.pos):
          if player.shot_size <= 2:
            player.shot_size += 1
          else:
            player.shot_size = 1

        if ui_3.collidepoint(event.pos):
          if player.damage <= 2:
            player.damage += 1
          else:
            player.damage = 1
        
        if ui_4.collidepoint(event.pos):
          player.spray = not player.spray
          print(player.spray)
        
        

    if game_active:

        screen.fill("#c0e8ec")
        player.draw(screen)
        text_surface = font.render(f"Score: {score}", False, (64,64,64)).convert()
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

        keys = pygame.key.get_pressed()
        player.rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player.speed
        if player.rect.x <= 0:
          player.rect.x = 0
        if player.rect.x >= 1004:
          player.rect.x = 1004
        player.rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player.speed
        if player.rect.y <= 0:
          player.rect.y = 0
        if player.rect.y >= 598:
          player.rect.y = 598

        if pygame.mouse.get_pressed()[0] and shot_cd <= 0:
          shot_cd = 20
          x,y = pygame.mouse.get_pos()
          b = Bullet("black", player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x, y)
          bullets.append(b)
          if player.spray == True:
            b1 = Bullet("black", player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x + 30, y + 30)
            b2 = Bullet("black", player.rect.centerx, player.rect.centery, (5 * player.shot_size), (5 * player.shot_size), 10, 1, x - 30, y - 30)
            bullets.append(b1)
            bullets.append(b2)
        


        spawn_enemies()
        for b in reversed(range(len(bullets))):
          for e in reversed(range(len(enemies))):
            if bullets[b].collided(enemies[e].rect):
              del bullets[b]
              enemies[e].hp -= 1 * player.damage
              if enemies[e].hp <= 0:
                del enemies[e]
              score += 10
              break

        for e in reversed(range(len(enemies))):
          if player.collided(enemies[e].rect):
            if i_frame <= 0 and is_hit == False:
              del enemies[e]
              player.hp -= 1
              is_hit = True
              i_frame = 15
              #print(f"Player HP remaining: {player.hp}")
              if player.hp <= 0:
                game_active = False

        for b in reversed(range(len(bullets))):
          bullets[b].move()
          if bullets[b].x <= -50 or bullets[b].x >= 1074:
            del bullets[b]
          elif bullets[b].y <= -50 or bullets[b].rect.midbottom[1] >= 618:
            del bullets[b]

        for e in enemies:
          e.move()

        for b in bullets:
          b.draw(screen)
        for e in enemies:
          e.draw(screen)

    else:
      screen.fill("#c0e8ec")
      text_surface = font.render(f"Score: {score}", False, (64,64,64)).convert()
      text_rectangle = text_surface.get_rect(center = (screen.get_width() /2, 50))
      screen.blit(text_surface, text_rectangle)
      game_over_surface = font.render("Game over!", False, "red")
      game_over_rectangle = game_over_surface.get_rect(center = (screen.get_width() /2 , screen.get_height() /2))
      restart_prompt_surface = font.render("Press space to restart", False, "black")
      restart_prompt_rectangle = restart_prompt_surface.get_rect(center = (screen.get_width() / 2, screen.get_height() - 100))
      screen.blit(game_over_surface, game_over_rectangle)
      screen.blit(restart_prompt_surface, restart_prompt_rectangle)

    pygame.display.update()
    clock.tick(60)
  
if __name__ == "__main__":
  main()