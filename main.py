import math
import pygame
from entities.player import Player
import functions


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TESTES")
clock = pygame.time.Clock()
running = True



polygon = [
    (200, 150),
    (300, 170),
    (320, 240),
    (250, 290),
    (190, 230)
]

uvs_polygon = [
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0)
]

cx = sum(p[0] for p in polygon) / len(polygon)
cy = sum(p[1] for p in polygon) / len(polygon)

angle = 0
time = 0

#viewports

viewport_minimap = (10, 10, 160, 120)
viewport_zoom = (330, 10, 490, 120)
window_world = (0, 0, width, height)
angle = 0
time = 0
player = Player((200, 200))

key_map = {
    pygame.K_w: "UP",
    pygame.K_a: "LEFT",
    pygame.K_s: "DOWN",
    pygame.K_d: "RIGHT"
}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        if keys[key]:
            player.move(dir)
    
    screen.fill((0, 0, 0))

    functions.scanline_texture(screen, player.show(), uvs_polygon, player.get_texture())


    pygame.display.flip()

    clock.tick(60)
    player.tick_loading += 1
    player.walking = False

pygame.quit()
