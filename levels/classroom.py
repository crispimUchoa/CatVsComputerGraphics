import math
from entities.level import Level
# from levels.street import level_street
from pygame.image import load

from primitives.draw_functions import draw_polygon
from primitives.fill_functions import scanline_fill, scanline_fill_gradient
from primitives.transform_functions import create_transform, multiply_matrix, rotation, scale, transform, translation

def star_vertices(x, y):
    return [
        (x,     y - 16),   # topo
        (x + 4, y - 6),
        (x + 16, y - 6),
        (x + 6, y + 2),
        (x + 10, y + 16),
        (x,     y + 8),
        (x - 15, y + 16),
        (x - 6, y + 2),
        (x - 16, y - 6),
        (x - 4, y - 6),
    ]

def draw_details(surfaces):
    _, static_surface, gradient_surface, _ = surfaces

    static_surface.fill((0, 0, 0, 0))

    scanline_fill(static_surface, [
            (10*2, 10*2), (106*2, 10*2), (106*2, 18*2), (10*2, 18*2)
        ], (0, 0, 0))

    scanline_fill(static_surface, [
            (112*2, 10*2), (139*2, 10*2), (139*2, 18*2), (112*2, 18*2)
        ], (0, 0, 0))
    width = 400*2
    height = 320*2
    c1 = (127, 0, 127)
    c2 = (196, 32, 127)
    scanline_fill_gradient(gradient_surface, 
                        [
                            (0, 0), (width, 0), (width, height/2),(width, height), (0, height), (0, height/2)
                        ],
                        [
                            c1, c1, c2, c1, c1, c2,
                        ]

                        )

def dynamic(surface, angle, s):
    width = surface.get_width()
    professor_head_out_1 = [(width/2 - 32*2, 16*2), (width/2 + 32*2, 16*2), (width/2 + 32*2, 51*2), (width/2 - 32*2, 51*2) ]
    professor_head_out_2 = [(width/2 - 31*2, 17*2), (width/2 + 31*2, 17*2), (width/2 + 31*2, 50*2), (width/2 - 31*2, 50*2) ]
    professor_head_in = [(width/2 - 30*2, 18*2), (width/2 + 30*2, 18*2), (width/2 + 30*2, 50*2), (width/2 - 30*2, 50*2) ]
    professor_body = [(width/2 - 6*2, 30*2), (width/2 + 6*2, 30*2), (width/2 + 6*2, 100*2), (width/2 + 32*2, 108*2), (width/2 - 32*2, 108*2), (width/2 - 6*2, 100*2)]

    stars = [
        ( 80,  75),   (160,  75),   (240,  75),   (320,  75),
( 80, 225),   (160, 225),   (240, 225),   (320, 225)

    ]

    pcx = sum(p[0] for p in professor_head_out_1) / len(professor_head_out_1)
    pcy = sum(p[1] for p in professor_head_out_1) / len(professor_head_out_1)

    m = create_transform()
    m = multiply_matrix(translation(-pcx, -pcy), m)
    m = multiply_matrix(rotation(math.sin(angle)/4), m)
    m = multiply_matrix(scale(s, s), m)
    m = multiply_matrix(translation(pcx, pcy), m)
    pho1 = transform(m, professor_head_out_1)
    pho2 = transform(m, professor_head_out_2)
    phin = transform(m, professor_head_in)
    
    for star in stars:
        x, y = star
        x = 2*x
        y = 2*y
        star_s = 1.20 + 0.20*math.sin(angle*2)
        ms = create_transform()
        ms = multiply_matrix(translation(-x, -y), ms)
        ms = multiply_matrix(rotation(angle*2), ms)
        ms = multiply_matrix(scale(star_s, star_s), ms)
        ms = multiply_matrix(translation(x, y), ms)

        mstar = transform(ms, star_vertices(x, y))

        scanline_fill(surface, mstar, (255, 255, 0))


    scanline_fill(surface, professor_body, (32, 32, 32))
    scanline_fill(surface, pho1, (32, 32, 32))
    draw_polygon(surface, pho2, (32, 32, 32))
    scanline_fill(surface, phin, 'black')




level_classroom = Level([], dict(), (200*2, 2*300), [], details=draw_details, dynamic_details=dynamic, name='classroom',
                        obstacles=[(0, 0, 400*2, 64*2)],
                        actions=[
                            (200*2 - 32*2, 16*2, 200*2+32*2, 108*2,),
                        ]
                        )