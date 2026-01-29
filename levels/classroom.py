import math
from entities.level import Level
# from levels.street import level_street
from pygame.image import load

from primitives.draw_functions import draw_polygon
from primitives.fill_functions import scanline_fill, scanline_fill_gradient
from primitives.transform_functions import create_transform, multiply_matrix, rotation, scale, transform, translation


def draw_details(surfaces):
    _, _, gradient_surface, _ = surfaces
    width = 400
    height = 320
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
    professor_head_out_1 = [(width/2 - 32, 16), (width/2 + 32, 16), (width/2 + 32, 51), (width/2 - 32, 51) ]
    professor_head_out_2 = [(width/2 - 31, 17), (width/2 + 31, 17), (width/2 + 31, 50), (width/2 - 31, 50) ]
    professor_head_in = [(width/2 - 30, 18), (width/2 + 30, 18), (width/2 + 30, 50), (width/2 - 30, 50) ]
    professor_body = [(width/2 - 6, 30), (width/2 + 6, 30), (width/2 + 6, 100), (width/2 + 32, 108), (width/2 - 32, 108), (width/2 - 6, 100)]

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

    scanline_fill(surface, professor_body, (32, 32, 32))
    scanline_fill(surface, pho1, (32, 32, 32))
    draw_polygon(surface, pho2, (32, 32, 32))
    scanline_fill(surface, phin, 'black')



level_classroom = Level([], dict(), (200, 300), [], details=draw_details, dynamic_details=dynamic, name='classroom',
                        obstacles=[(0, 0, 400, 64)],
                        actions=[
                            (200 - 32, 16, 200+32, 108,),
                        ]
                        )