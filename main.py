import math
import pygame
import functions


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TESTES")
clock = pygame.time.Clock()
running = True

polygon = [(50, 50), (50, 100), (100, 80), (100, 70)]

cx = sum(p[0] for p in polygon) / len(polygon)
cy = sum(p[1] for p in polygon) / len(polygon)

angle = 0
time = 0

y = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 255, 255))

    angle += 0.02
    time += 0.05

    s = 2.0 + 0.3*math.sin(time)

    m = functions.create_transform()
    m = functions.multiply_matrix(functions.translation(-cx, -cy), m)
    m = functions.multiply_matrix(functions.rotation(angle), m)
    m = functions.multiply_matrix(functions.scale(s, s), m)
    m = functions.multiply_matrix(functions.translation(cx, cy), m)

    transformed_polygon = functions.transform(m, polygon)

    functions.scanline_fill(screen, transformed_polygon, (255, 0, 0))
    functions.draw_polygon(screen, transformed_polygon, (0, 0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
