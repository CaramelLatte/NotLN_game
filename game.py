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

  def spawn():
    enemy_spawn = random.randint(0, 100)
    if enemy_spawn > 1 and enemy_spawn < 5:
      enemy_spawnx = 0
      enemy_spawny = 0
      spawn_wall = random.randint(1, 4)
      match spawn_wall:
        case 1:
          enemy_spawnx = 50
          enemy_spawny = random.randint(50, 718)
        case 2:
          enemy_spawnx = 984
          enemy_spawny = random.randint(50, 718)
        case 3:
          enemy_spawny = 50
          enemy_spawnx = random.randint(50, 984)
        case 4:
          enemy_spawny = 718
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
          e = Enemy("Blue", enemy_spawnx, enemy_spawny, 15, 15, 2, 2)
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

    def move(self):
      pass
    def moveDirection(self):
      pass
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
  while game_active:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        x,y = pygame.mouse.get_pos()
        b = Bullet("black", player.rect.centerx, player.rect.centery, 10, 10, 10, 1, x, y)
        bullets.append(b)
    if game_active:
      screen.fill("#c0e8ec")
      player.draw(screen)
      text_surface = font.render(f"Score: {score}", False, (64,64,64)).convert()
      text_rectangle = text_surface.get_rect(center = (400, 50))
      screen.blit(text_surface, text_rectangle)
      pygame.draw.line(screen, 'black', player.rect.center, pygame.mouse.get_pos())


    if is_hit == True:
      i_frame -= 1
      if i_frame <= 0:
        is_hit = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
      player.rect.y -= player.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
      player.rect.y += player.speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      player.rect.x -= player.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      player.rect.x += player.speed

    spawn()
    #Check for bullet collision with enemies
    for b in reversed(range(len(bullets))):
      for e in reversed(range(len(enemies))):
        if bullets[b].collided(enemies[e].rect):
          del bullets[b]
          enemies[e].hp -= 1
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
          print(f"Player HP remaining: {player.hp}")
          if player.hp <= 0:
            game_active = False


    for b in bullets:
      b.move()
      if b.x < 0 or b.x > 1024:
        bullets.remove(b)
      if b.y < 0 or b.y > 768:
        bullets.remove(b)

    for e in enemies:
      e.move()

    for b in bullets:
      b.draw(screen)
    for e in enemies:
      e.draw(screen)

      
    pygame.display.update()
    clock.tick(60)
  
if __name__ == "__main__":
  main()