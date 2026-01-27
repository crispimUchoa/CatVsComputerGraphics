class Skip_Level:
    def __init__(self, pos, next_level):
        self.pos = pos
        self.next_level = next_level
        self.w = 16*3
        self.h = 16

    def check_player_colision(self, player_pos):
        px, py = player_pos
        x, y = self.pos
        
        
        if x <= px <= x + self.w and y <= py <= y +self.h:
            return True


        return False
