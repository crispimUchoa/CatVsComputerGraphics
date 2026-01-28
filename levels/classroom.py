from entities.level import Level
# from levels.street import level_street
from pygame.image import load

from primitives.fill_functions import scanline_fill_gradient


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


level_classroom = Level([], dict(), (12*16, 32), [], details=draw_details, name='classroom')