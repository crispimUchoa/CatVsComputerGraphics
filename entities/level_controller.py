from entities.level import Level
from entities.skip_level import Skip_Level
from primitives.fill_functions import scanline_fill, scanline_texture
from tile import Tile

class Level_Controller:
    def __init__(self, surface, static_surface):
        self.GROUND = 0
        self.level = None
        self.static_surface = static_surface
        self.surface = surface
        self.w = 16
        self.sw = self.surface.get_width()
        self.sh = self.surface.get_height()
        self.timer = 0
        self.total_time = 60*60*3 #3 horas do jogo -> 3 minutos da vida real
        default_repeat_x = self.sw / self.w
        default_repeat_y = self.sh / self.w
        self.uvs_default_tiling = [
                (0.0, 0.0),
                (default_repeat_x, 0.0),
                (default_repeat_x, default_repeat_y),
                (0.0, default_repeat_y)
        ]
        

    def set_level(self, level: Level, player):
        self.level = level
        self.skip_level = level.skip
        self.player_pos = level.player_pos

        self.WALLS: list[Tile] = []
        self.GROUND_DETAILS: list[Tile] = []
        if level.tile_map:
            self.GROUND = level.tile_code[0]
            for i in range(20):
                for j in range(25):
                    iw = i*self.w
                    jw = j*self.w
                    if 0 < level.tile_map[i][j] <=2 :
                        self.WALLS.append(Tile((jw, iw), self.w, self.w, sprite=level.tile_code[level.tile_map[i][j]]))
                    elif level.tile_map[i][j] > 2:
                        self.GROUND_DETAILS.append(Tile((jw, iw), self.w, self.w, sprite=level.tile_code[level.tile_map[i][j]]))
        
            self.set_tiles(self.static_surface)

        player.pos = level.player_pos

    def iswall(self, x, y):
        for wall in self.WALLS:
            if wall.position[0] <= x <= wall.position[0] + wall.width and wall.position[1] <= y <= wall.position[1] + wall.height:
                return True
        return False  
    
    def increse_timer(self):
        self.timer+=1
    
    def get_timer_in_hm(self):
        timer = self.timer// 60
        h = (timer // 60) + 5
        m = timer % 60
        return f'{h:02d}:{m:02d}'
    
    def set_tile(self, tile_list, static_surface):
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

    def set_tiles(self, static_surface):
        scanline_texture(static_surface, [(0, 0), (self.sw, 0), (self.sw, self.sh), (0, self.sh) ], self.uvs_default_tiling, self.GROUND)
        
        if self.WALLS:
            self.set_tile(self.WALLS, static_surface)
        if self.GROUND_DETAILS:
            self.set_tile(self.GROUND_DETAILS, static_surface)

    def isskip(self, player, next_level):
        if self.skip_level.check_player_colision(player.pos):
            self.set_level(next_level, player)

    def show_timer_bar(self):
        padding = 10
        bar_y = 8
        bar_total_x = 96
        bar_percent = (self.total_time - self.timer) / self.total_time
        bar_current_x = bar_total_x * bar_percent
        scanline_fill(self.surface,  [(padding, padding), (padding, padding + bar_y), (padding + bar_current_x, padding + bar_y), (padding + bar_current_x, padding)], (0, 255, 0))