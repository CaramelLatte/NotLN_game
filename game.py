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

  game_active = True

  player_surf = pygame.Surface((20, 20))
  player_rect = player_surf.get_rect(center = (512, 374))
  bullets = []
  enemies = []

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




  player = Entity("black", 100, 100, 20, 20, 5, 100 )
  while True:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        x,y = pygame.mouse.get_pos()
        b = Bullet("black", player.rect.centerx, player.rect.centery, 5, 5, 10, 1, x, y)
        bullets.append(b)
        print(bullets)
    if game_active:
      screen.fill("#c0e8ec")
      player.draw(screen)

    pygame.draw.line(screen, 'black', player.rect.center, pygame.mouse.get_pos())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
      player.rect.y -= player.speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
      player.rect.y += player.speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      player.rect.x -= player.speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      player.rect.x += player.speed

    enemy_spawn = random.randint(0, 100)
    if enemy_spawn > 1 and enemy_spawn < 5:
      e = Enemy("white", 0, 0, 15, 15, 2, 1)
      enemies.append(e)


    for i in reversed(range(len(bullets))):
      for j in reversed(range(len(enemies))):
        if bullets[i].collided(enemies[j].rect):
          del enemies[j]
          del bullets[i]
          break
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


    
    for e in enemies:
      if e.collided(player.rect):
        print("Got hit!")
      
    pygame.display.update()
    clock.tick(60)
  
if __name__ == "__main__":
  main()