from entities.skip_level import Skip_Level
from tile import Tile


class Level:
    def __init__(self, tile_map: list[Tile], tile_code: Tile, player_pos, skip: Skip_Level | int):
        self.tile_map = tile_map
        self.tile_code = tile_code
        self.player_pos = player_pos
        self.skip = skip