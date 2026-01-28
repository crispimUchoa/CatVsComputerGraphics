from entities.skip_level import Skip_Level
from primitives.fill_functions import scanline_texture
from tile import Tile


class Level:
    def __init__(self, tile_map: list[Tile], tile_code: Tile, player_pos, skip: list[Skip_Level], details = None, name='', w=16):
        self.tile_map = tile_map
        self.tile_code = tile_code
        self.player_pos = player_pos
        self.skip = skip
        self.details = details
        self.name = name
        self.walls: list[Tile] = []
        self.ground_details: list[Tile] = []
        self.ground = self.tile_code[0] if tile_map else None
        self.w = w

        if self.tile_map:
            for i in range(20):
                for j in range(25):
                    iw = i*w
                    jw = j*w
                    if 0 < self.tile_map[i][j] <=2 :
                        self.walls.append(Tile((jw, iw), self.w, self.w, sprite=self.tile_code[self.tile_map[i][j]]))
                    elif self.tile_map[i][j] > 2:
                        self.ground_details.append(Tile((jw, iw), self.w, self.w, sprite=self.tile_code[self.tile_map[i][j]]))



    def draw_tile(self, tile_list, static_surface):
        for tile in tile_list:
            repeat_x = tile.width / self.w
            repeat_y = tile.height / self.w
            
            uvs_tiling = [
            (0.0, 0.0),
            (repeat_x, 0.0),
            (repeat_x, repeat_y),
            (0.0, repeat_y)
        ]
            scanline_texture(static_surface, [(tile.position[0], tile.position[1]), (tile.position[0] + tile.width, tile.position[1]), (tile.position[0] + tile.width, tile.position[1] + tile.height), (tile.position[0], tile.position[1] + tile.height)], uvs_tiling, tile.sprite)

    def draw_tiles(self, static_surface, uvs):
        if not self.tile_map: return

        sw = static_surface.get_width()
        sh = static_surface.get_height()
        scanline_texture(static_surface, [(0, 0), (sw, 0), (sw, sh), (0, sh) ], uvs, self.ground)
        
        if self.walls:
            self.draw_tile(self.walls, static_surface)
        if self.ground_details:
            self.draw_tile(self.ground_details, static_surface)


    def draw_details(self, static_surface):
        self.details(static_surface)

    def draw_level(self, surfaces, uvs):
        _, static_surface, _, _ = surfaces

        if self.name != 'classroom':
            self.draw_tiles(static_surface, uvs)
        if self.details:
            self.draw_details(surfaces)