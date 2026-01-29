from entities.level import Level
from entities.player import Player
from entities.skip_level import Skip_Level
from primitives.fill_functions import scanline_fill, scanline_texture
from tile import Tile
import asyncio

class Level_Controller:
    def __init__(self, surface, static_surface, gradient_surface, bus_surface, message_surface, font):
        self.font = font
        self.message_surface = message_surface
        self.text_tick = -1
        self.end = False
        self.win = False
        self.pause = False
        self.bus_surface = bus_surface
        self.gradient_surface = gradient_surface
        self.GROUND = 0
        self.level = None
        self.static_surface = static_surface
        self.surface = surface
        self.w = 16
        self.sw = self.surface.get_width()
        self.sh = self.surface.get_height()
        self.timer = 0
        self.total_time = 60*60 #1 horas do jogo -> 1 minutos da vida real
        default_repeat_x = self.sw / self.w
        default_repeat_y = self.sh / self.w
        self.uvs_default_tiling = [
                (0.0, 0.0),
                (default_repeat_x, 0.0),
                (default_repeat_x, default_repeat_y),
                (0.0, default_repeat_y)
        ]
        

    def set_level(self, level: Level, player):
        if level.name == 'home':
            self.show_message(self.font, 'Ache seus itens e vá para a aula')

        if level.name == 'classroom':
            self.show_message(self.font, 'Vá até o professor')

        self.level = level
        self.skip_level = level.skip
        self.player_pos = level.player_pos
        surface = [ self.surface, self.static_surface, self.gradient_surface, self.bus_surface] 
        level.draw_level(surface, self.uvs_default_tiling)

        player.pos = level.player_pos

    def iswall(self, x, y):
        for wall in self.level.walls:
            if wall.position[0] <= x <= wall.position[0] + wall.width and wall.position[1] <= y <= wall.position[1] + wall.height:
                return True
        return False  
    
    def isobstacle(self, x, y):
        for obstacle in self.level.obstacles:
            xmin, ymin, xmax, ymax = obstacle
            if xmin <= x <= xmax and ymin <= y <= ymax:
                return True
        return False  

    def iscolisor(self, x, y):
        return self.iswall(x, y) or self.isobstacle(x, y)

    def increase_timer(self):
        if self.timer < self.total_time:
            self.timer+=1
    
    def get_timer_in_hm(self):
        timer = self.timer// 60
        h = (timer // 60) + 7
        m = (timer + 30) % 60
        return f'{h:02d}:{m:02d}'


    def isskip(self, player):
        for skip in self.level.skip:
            if skip.check_player_colision(player.pos):
                if skip.next_level.name == 'classroom':
                    if player.items['student_card'] < 2:
                        self.show_message(self.font, 'Pegue sua carteirinha de estudante')
                        return
                self.set_level(skip.next_level, player)

    def draw_items(self, surface, s, var_tx, player):
        px, py = player.pos
        for item in self.level.items:
            ix, iy = item.position
            if px - player.vision_range <= ix <= px + player.vision_range and py - player.vision_range/2 <= iy <= py + player.vision_range/2:
                item.draw_sprite(surface, s, var_tx)

    def toggle_pause(self):
        if not self.end:
            self.pause = not self.pause

    def show_timer_bar(self):
        padding = 10*2
        bar_y = 8*2
        bar_total_x = 96*2
        bar_percent = (self.total_time - self.timer) / self.total_time
        bar_current_x = bar_total_x * bar_percent
        scanline_fill(self.surface,  [(padding, padding), (padding, padding + bar_y), (padding + bar_current_x, padding + bar_y), (padding + bar_current_x, padding)], (0, 255, 0))

    def after_tick_status(self, surface, font):
        if self.text_tick > 0:
            self.text_tick -=1
        elif self.text_tick == 0:
            self.show_text = False
            self.show_text -=1
            self.message_surface.fill((0, 0, 0, 0))
        else:
            surface.fill((0, 0,0, 0))
            
        surface.fill((0, 0,0, 0))
        self.update(surface, font, self.get_timer_in_hm())

        if not self.end:
            if self.timer >= self.total_time:
                self.end = True
        if self.end:
            message = 'Parabéns! Aguarde sua nota!' if self.win else 'Você perdeu!'
            if not self.win:
                message += ' Seu tempo acabou!' if self.timer >= self.total_time else ' Esqueceu notebook em casa!'
            self.show_message(self.font, message, position=(200*2, 144*2))
            self.pause = True

    def is_player_coliding(self, dir, player: Player):
        x, y = player.pos
        if dir == 'LEFT':
            return ( x-player.sx/2 <= 0) or self.iscolisor(x - player.sx/2, y) or self.iscolisor(x - player.sx/2, y + player.sy/4)
        if dir == 'RIGHT':
            return ( x+player.sx/2 > self.sw) or self.iscolisor(x + player.sx/2, y) or self.iscolisor(x + player.sx/2, y + player.sy/4)
        if dir == 'UP':
            return ( y-player.sx/4 <= 0) or self.iscolisor(x - player.sx/4 , y - player.sy/4) or self.iscolisor(x + player.sx/4, y - player.sy/4)
        if dir == 'DOWN':
            return ( y+player.sx/2 > self.sh) or self.iscolisor(x - player.sx/4, y + player.sy/2) or self.iscolisor(x + player.sx/4, y + player.sy/2)
        return False
    
    def player_in_items_range(self, player: Player):
        for item in self.level.items:
            if player.can_get_item(item):
                player.get_item(item)

    def is_player_meeting_professor(self, player):
        for action in self.level.actions:
            xmin, ymin, xmax, ymax = action
            x, y = player.pos

            if xmin - 4 <= x <= xmax + 4 and ymin - 4 <= y <= ymax + 4:
                self.end = True
                if self.level.name == 'classroom':
                    if player.items['laptop'] == 1 and player.items['student_card'] == 2:
                        self.win = True
            
    def update(self, surface, font, text):
        text_surface = font.render(text, False, (255, 255, 255))
            
        surface.blit(text_surface, (116*2, 10*2))

    def show_message(self, font, text, position=(200*2, 304*2)):
        self.message_surface.fill((0,0, 0, 0))
        text_surface = font.render(text, False, (255, 255, 255))
        self.text_tick = 180
        x, y = position
        margin_x = len(text)*16/4
        self.message_surface.blit(text_surface, (x - margin_x, y))