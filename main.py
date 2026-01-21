import pygame
import math

def set_pixel(surface, x, y, color):
    surface.set_at((x,y), color)

def read_pixel(surface, x, y):
    return surface.get_at((x, y))

def dda(surface, x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0

    steps = max(abs(dx), abs(dy))

    if steps > 0:
        x_inc = dx / steps
        y_inc = dy / steps

        x = x0
        y = y0

        for _ in range(steps + 1):
            set_pixel(surface, round(x), round(y), color)
            x += x_inc
            y += y_inc

def bressenham(surface, x0, y0, x1, y1, color):
    steep = abs(y1 - y0) > (x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    ystep = 1
    if dy < 0:
        ystep = -1
        dy = -dy

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x0
    y = y0

    while x <= x1:
        if steep:
            set_pixel(surface, y, x, color)
        else:
            set_pixel(surface, x, y, color)

        if d <= 0:
            d += incE
        else:
            d += incNE
            y += ystep

        x += 1

def naive_line(surface, x0, y0, x1, y1, color):
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0

    if dx == 0:
        return
    
    m = (y1 - y0) / dx
    b = y0 - m*x0

    for x in range(x0, x1 + 1):
        y = m*x + b
        set_pixel(surface, x, y, color)
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

    bressenham(screen, screen.get_width(), screen.get_height(), 250, 0, (255, 0, 0))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()