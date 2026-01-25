
class Player:
    def __init__(self, position, texture):
        self.pos = position
        self.texture = texture
        self.sx = 50
        self.sy = 100
        self.speed = 10

    def show(self):
        x, y = self.pos
        return [
            (x - self.sx/2, y - self.sy),
            (x + self.sx/2, y - self.sy),
            (x + self.sx/2, y),
            (x - self.sx/2, y)
        ]
    
    def left(self):
        x, y = self.pos
        self.pos = (x - self.speed, y)

    def right(self):
        x, y = self.pos
        self.pos = (x + self.speed, y)

    def up(self):
        x, y = self.pos
        self.pos = (x, y - self.speed)

    def down(self):
        x, y = self.pos
        self.pos = (x, y + self.speed)

    def walk(self, dir):
        x, y = self.pos

        directions = {
            'A': self.left,
            'D': self.right,
            'W': self.up,
            'S': self.down,
        }

        if dir in ['W', 'A', 'S', 'D']:
            directions[dir]()

