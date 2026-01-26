from pygame.image import load

from primitives.fill_functions import scanline_texture

class Player:
    def __init__(self, position, dir='DOWN'):
        self.pos = position
        self.sprites = self.load_convert_sprites()
        self.sx = 32
        self.sy = 32
        self.speed = 2
        self.dir = dir
        self.walking = False
        self.walking_sprite = 0
        self.tick_loading = 0

    def get_vertices(self):
        x, y = self.pos
        return [
            (x - self.sx/2, y - self.sy/2),
            (x + self.sx/2, y - self.sy/2),
            (x + self.sx/2, y + self.sy/2),
            (x - self.sx/2, y + self.sy/2)
        ]
    
    def show(self, surface, uvs_default):
        scanline_texture(surface, self.get_vertices(), uvs_default, self.get_texture())


    def left(self):
        x, y = self.pos
        if self.dir == 'LEFT':
            self.pos = (x - self.speed, y)

    def right(self):
        x, y = self.pos
        if self.dir == 'RIGHT':
            self.pos = (x + self.speed, y)

    def up(self):
        x, y = self.pos
        self.pos = (x, y - self.speed)

    def down(self):
        x, y = self.pos
        self.pos = (x, y + self.speed)

    def set_dir(self, dir:str):
        if dir in ['LEFT', 'UP', 'DOWN', 'RIGHT'] and self.walking == False:
            self.dir = dir

    def walk(self, dir):
        if dir != self.dir:
            return
        
        self.walking = True
        directions = {
            'LEFT': self.left,
            'RIGHT': self.right,
            'UP': self.up,
            'DOWN': self.down,
        }
        
        if self.dir in ['UP', 'LEFT', 'DOWN', 'RIGHT']:
            directions[self.dir]()

    def move(self, dir):
        self.set_dir(dir)
        self.walk(dir)

    def is_coliding(self, dir, level):
        x, y = self.pos
        if dir == 'LEFT':
            return ( x-self.sx/2 <= 0) or level.iswall(x - self.sx/2, y)
        if dir == 'RIGHT':
            return ( x+self.sx/2 > level.sw) or level.iswall(x + self.sx/2, y)
        if dir == 'UP':
            return ( y-self.sx/4 <= 0) or level.iswall(x - self.sx/4 , y - self.sy/4) or level.iswall(x + self.sx/4, y - self.sy/4)
        if dir == 'DOWN':
            return ( y+self.sx/2 > level.sh) or level.iswall(x - self.sx/4, y + self.sy/2) or level.iswall(x + self.sx/4, y + self.sy/2)
        return False

    def get_texture(self):
        if self.walking:
            if self.tick_loading % 3 == 0:
                self.walking_sprite = (self.walking_sprite + 1) % 3
            return self.sprites['WALKING'][self.dir][self.walking_sprite]
        
        return self.sprites['STAND'][self.dir]

    def status_after_tick(self):
        self.walking = False
        self.tick_loading +=1
        if self.tick_loading >=60:
            self.tick_loading = 0

    def load_convert_sprites(self):
        DIR = './sprites/player/'
        STAND_DIR = DIR + 'stand'
        MOVING_DIR = DIR + 'moving'
        PLAYER_DOWN_STAND_SPRITE = load(f'{STAND_DIR}/DOWN_STAND.png').convert_alpha()
        PLAYER_RIGHT_STAND_SPRITE = load(f'{STAND_DIR}/RIGHT_STAND.png').convert_alpha()
        PLAYER_LEFT_STAND_SPRITE = load(f'{STAND_DIR}/LEFT_STAND.png').convert_alpha()
        PLAYER_UP_STAND_SPRITE = load(f'{STAND_DIR}/UP_STAND.png').convert_alpha()

        PLAYER_DOWN_WALKING_0_SPRITE = load(f'{MOVING_DIR}/DOWN_WALKING_0.png').convert_alpha()
        PLAYER_DOWN_WALKING_1_SPRITE = load(f'{MOVING_DIR}/DOWN_WALKING_1.png').convert_alpha()
        PLAYER_DOWN_WALKING_2_SPRITE = load(f'{MOVING_DIR}/DOWN_WALKING_2.png').convert_alpha()
        PLAYER_UP_WALKING_0_SPRITE = load(f'{MOVING_DIR}/UP_WALKING_0.png').convert_alpha()
        PLAYER_UP_WALKING_1_SPRITE = load(f'{MOVING_DIR}/UP_WALKING_1.png').convert_alpha()
        PLAYER_UP_WALKING_2_SPRITE = load(f'{MOVING_DIR}/UP_WALKING_2.png').convert_alpha()
        PLAYER_LEFT_WALKING_0_SPRITE = load(f'{MOVING_DIR}/LEFT_WALKING_0.png').convert_alpha()
        PLAYER_LEFT_WALKING_1_SPRITE = load(f'{MOVING_DIR}/LEFT_WALKING_1.png').convert_alpha()
        PLAYER_LEFT_WALKING_2_SPRITE = load(f'{MOVING_DIR}/LEFT_WALKING_2.png').convert_alpha()
        PLAYER_RIGHT_WALKING_0_SPRITE = load(f'{MOVING_DIR}/RIGHT_WALKING_0.png').convert_alpha()
        PLAYER_RIGHT_WALKING_1_SPRITE = load(f'{MOVING_DIR}/RIGHT_WALKING_1.png').convert_alpha()
        PLAYER_RIGHT_WALKING_2_SPRITE = load(f'{MOVING_DIR}/RIGHT_WALKING_2.png').convert_alpha()


        return { 
            'STAND':{
                'DOWN': PLAYER_DOWN_STAND_SPRITE,
                'RIGHT': PLAYER_RIGHT_STAND_SPRITE,
                'LEFT': PLAYER_LEFT_STAND_SPRITE,
                'UP': PLAYER_UP_STAND_SPRITE,
            },
            'WALKING':{
                'DOWN': [PLAYER_DOWN_WALKING_0_SPRITE, PLAYER_DOWN_WALKING_1_SPRITE, PLAYER_DOWN_WALKING_2_SPRITE],
                'UP': [PLAYER_UP_WALKING_0_SPRITE, PLAYER_UP_WALKING_1_SPRITE, PLAYER_UP_WALKING_2_SPRITE],
                'RIGHT': [PLAYER_RIGHT_WALKING_0_SPRITE, PLAYER_RIGHT_WALKING_1_SPRITE, PLAYER_RIGHT_WALKING_2_SPRITE],
                'LEFT': [PLAYER_LEFT_WALKING_0_SPRITE, PLAYER_LEFT_WALKING_1_SPRITE, PLAYER_LEFT_WALKING_2_SPRITE],
            }
        }