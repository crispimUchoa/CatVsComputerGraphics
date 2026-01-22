import pygame
import primitives


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("TESTES")
clock = pygame.time.Clock()
running = True

y = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 255, 255))
    primitives.draw_polygon(screen, [(50, 50), (50, 100), (100, 80), (100, 70)], (0, 0, 0))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()