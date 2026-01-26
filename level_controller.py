class Level_Controller:
    def __init__(self, surface, level=None):
        self.WALL = {
                'position': (0,0),
                'height': surface.get_height(),
                'width': 50
            }


    def iswall(self, x, y):
        if self.WALL['position'][0] <= x <= self.WALL['position'][0] + self.WALL['width'] and self.WALL['position'][1] <= y <= self.WALL['position'][1] + self.WALL['height']:
            return True
        return False  