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

    angle += 0.02
    time += 0.05

    s = 1.0 + 0.3*math.sin(time)

    m = functions.create_transform()
    m = functions.multiply_matrix(functions.translation(-cx, -cy), m)
    m = functions.multiply_matrix(functions.rotation(angle), m)
    m = functions.multiply_matrix(functions.scale(s, s), m)
    m = functions.multiply_matrix(functions.translation(cx, cy), m)

    transformed_polygon = functions.transform(m, polygon)

    functions.draw_polygon(screen, transformed_polygon, (255, 255, 255))
    functions.scanline_fill(screen, transformed_polygon, (0, 200, 0))

    xs = [p[0] for p in transformed_polygon]
    ys = [p[1] for p in transformed_polygon]
    margin = 20
    window_zoom = (min(xs)- margin, min(ys)-margin, max(xs)+margin, max(ys)+margin)
    
    #MINIMAPA
    mmini = functions.window_viewport(window_world, viewport_minimap)
    polimini = functions.transform(mmini, transformed_polygon)
    functions.draw_polygon(screen, polimini, (200, 200, 200))
    functions.scanline_fill(screen, polimini, (0, 120, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(10, 10, 150, 110), 1)

    #Zoom
    mzoom = functions.window_viewport(window_zoom, viewport_zoom)
    polzoom = functions.transform(mzoom, transformed_polygon)
    functions.draw_polygon(screen, polzoom, (255, 255, 0))
    functions.scanline_fill(screen, polzoom, (200, 200, 0))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(330, 10, 160, 110), 1)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
