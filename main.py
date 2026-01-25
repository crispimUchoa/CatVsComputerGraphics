import math
import pygame
import functions


pygame.init()
width, height = 500, 400
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

cx = sum(p[0] for p in polygon) / len(polygon)
cy = sum(p[1] for p in polygon) / len(polygon)

angle = 0
time = 0

#viewports

viewport_minimap = (10, 10, 160, 120)
viewport_zoom = (330, 10, 490, 120)
window_world = (0, 0, width, height)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    functions.draw_elipse(screen, (200, 200), 100, 100, (255, 0, 0))
    functions.scanline_elipses(screen, (200, 200), 100, 100, (255, 0, 0))
    # functions.draw_circle(screen, (200, 200), 50, (255, 255, 255))
    # functions.flood_fill(screen, (200, 200), (255, 0, 0), (255, 255, 255))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
