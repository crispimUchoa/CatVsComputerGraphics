from entities.level import Level
from pygame.image import load
from entities.skip_level import Skip_Level
from primitives.fill_functions import scanline_fill, scanline_texture
# from levels.home import level_home
HOUSE_WALL_SPRITE = load('./sprites/tiles/HOUSE_WALL.png').convert()
HOUSE_WALL_FRONT_SPRITE = load('./sprites/tiles/HOUSE_WALL_FRONT.jpeg').convert()
STREET_GRAY_SPRITE = load('./sprites/tiles/STREET_GRAY.jpeg').convert()
STREET_YELLOW_SPRITE = load('./sprites/tiles/STREET_YELLOW.jpeg').convert()
GRASS_SPRITE = load('./sprites/tiles/GRASS.jpeg').convert()
PAVEMENT_SPRITE = load('./sprites/tiles/PAVEMENT.jpeg').convert()

BUS_SPRITE = load('./sprites/BUS.png').convert_alpha()



tile_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, ],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, ],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, ],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
            [3, 4, 4, 4, 3, 3, 4, 4, 4, 3, 3, 4, 4, 4, 3, 3, 4, 4, 4, 3, 3, 4, 4, 4, 3, ],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, ],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, ],
            [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ],
        ]

tile_code = {
    0: GRASS_SPRITE,
    1: HOUSE_WALL_SPRITE,
    2: HOUSE_WALL_FRONT_SPRITE,
    3: STREET_GRAY_SPRITE,
    4: STREET_YELLOW_SPRITE,
    5: PAVEMENT_SPRITE
}


def street_details(surfaces):
    _, static_surface, _, bus_surface = surfaces
    w = static_surface.get_width()
    h = static_surface.get_height()
    bw = 344
    bh = 120
    bot_size = 0.15
    uvs_bus_bottom = [
        (0, 1),
        (1, 1),
        (1, bot_size),
        (0, bot_size),
    ]

    uvs_bus_top = [
        (0, (1 - bot_size)),
        (1, 1 - bot_size),
        (1, 0),
        (0, 0),
    ]

    bus_vertices_bottom = [
        (w - bw, h - 7*16),
        (w, h - 7*16),
        (w, h - 7*16 - bh*(1 - bot_size)),
        (w - bw, h - 7*16 - bh*(1-bot_size)),
    ]

    bus_vertices_top = [
        (w - bw, h - 7*16 - bh*bot_size),
        (w, h - 7*16 - bh*bot_size),
        (w, h - 7*16 - bh),
        (w - bw, h - 7*16 - bh),
    ]

    scanline_texture(static_surface, bus_vertices_bottom, uvs_bus_bottom, BUS_SPRITE)
    scanline_texture(bus_surface, bus_vertices_top, uvs_bus_top, BUS_SPRITE)


level_street = Level(tile_map, tile_code, (32, 298), [Skip_Level( (1*16, 304), 0), Skip_Level( (328, 176), 2, h=48)], 
                     name='street', 
                     details=street_details,
                     obstacles=[
                         (400 - 332, 320 - 8*16, 400, 320 - 8*16 + 4)
                         
                     ])