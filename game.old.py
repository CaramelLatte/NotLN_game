import pygame
import math
from sys import exit

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

while True:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse = pygame.mouse.get_pos()
      angle = math.atan2(mouse[1]-player_rect.centery, mouse[0]-player_rect.centerx)
      print(angle*180/math.pi)

  if game_active:
    screen.fill("#c0e8ec")
    screen.blit(player_surf, player_rect)

  pygame.draw.line(screen, 'black', player_rect.center, pygame.mouse.get_pos())

  keys = pygame.key.get_pressed()
  if keys[pygame.K_UP] or keys[pygame.K_w]:
    player_rect.y -= 4
  if keys[pygame.K_DOWN] or keys[pygame.K_s]:
    player_rect.y += 4
  if keys[pygame.K_LEFT] or keys[pygame.K_a]:
    player_rect.x -= 4
  if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
    player_rect.x += 4

  pygame.display.update()
  clock.tick(60)