import math
import pygame
from entities.level_controller import Level_Controller
from entities.player import Player

#
# MAPEAMENTO DAS TECLAS
#

key_map = {
    #AÇÕES DO PLAYER
    pygame.K_w: "UP",
    pygame.K_a: "LEFT",
    pygame.K_s: "DOWN",
    pygame.K_d: "RIGHT",
}

#
#INICIALIZA O DISPLAY
#
DISPLAY_CAPTION = 'Cat Vs Computer Graphics - MENU'
pygame.init()
width, height = 400, 320
virtual_screen = pygame.Surface((width, height))
screen = pygame.display.set_mode((width*2, 2*height), pygame.SRCALPHA, pygame.SCALED)
pygame.display.set_caption(DISPLAY_CAPTION)
clock = pygame.time.Clock()
running = True

font = pygame.font.SysFont(None, 12)
message_font = pygame.font.SysFont(None, 24)

text_surface = pygame.Surface((width, height)).convert_alpha()
message_surface = pygame.Surface((width, height)).convert_alpha()
message_surface.fill((0, 0, 0, 0))



from levels.home import level_home
from levels.classroom import level_classroom
from levels.street import level_street

level_home.skip[0].next_level = level_street
level_street.skip[0].next_level = level_home
level_street.skip[1].next_level = level_classroom


#
#PROPORÇÃO DE TEXTURA PADRÃO PARA RETANGULOS
#
uvs_default = [
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0)
]

gradient_surface = pygame.Surface((width, height))


#
#DEFINE PLAYER
#
static_surface = pygame.Surface((width, height)).convert_alpha()
bus_surface = pygame.Surface((width, height), pygame.SRCALPHA)

level = Level_Controller(virtual_screen, static_surface, gradient_surface, bus_surface, message_surface, message_font)
player = Player((0, 0))
level.set_level(level_home, player)
# scanline_texture(static_surface, [ (width - 22*16, height - 15*16),(width, height - 15*16),(width, height - 7*16),(width - 22*16, height - 7*16) ], uvs_default, BUS_SPRITE)
#
#JOGO RODANDO
#
coliding = False
walls = level.level.walls


i = 1
y = 0

angle = 0
time = 0

s = 1
s_item = 1.1
var_tx = -8
offset = 0

while running:
    clock.tick(60)

    if not level.pause:
        angle +=0.02
        time += 0.05
        s = 1 + 0.15 * math.sin(angle)
        s_item = 1.10 + 0.05*math.sin(angle)
        var_tx = (-1 - math.sin(angle))*8
    
    y+=1
    if y>=height*1.5:
        y=-height*1.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RETURN and not level.pause:
                level.isskip(player)
                level.player_in_items_range(player)
                level.is_player_meeting_professor(player)

            if event.key == pygame.K_ESCAPE:
                level.toggle_pause()

    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        
        if keys[key] and not level.is_player_coliding(dir, player) and not level.pause:
            player.move(dir)

        
    if level.level == level_classroom:
        offset = (offset - 4) % height
        virtual_screen.blit(gradient_surface, (0, offset - height))
        virtual_screen.blit(gradient_surface, (0, offset))
        level.level.draw_dynamic_details(virtual_screen, angle, s) 
    

    virtual_screen.blit(static_surface, (0, 0))


    level.draw_items(virtual_screen, s_item, var_tx, player)
    player.show(virtual_screen, uvs_default)
    level.show_timer_bar()
    scaled = pygame.transform.scale(virtual_screen, (width*2, height*2))
    scaled_bus = pygame.transform.scale(bus_surface, (width*2, height*2))
    screen.blit(scaled, (0, 0))
    
    if level.level == level_street:
        screen.blit(scaled_bus, (0, 0))


    scaled_text = pygame.transform.scale(text_surface, (width*2, height*2))
    screen.blit(scaled_text, (0, 0))

    scaled_message = pygame.transform.scale(message_surface, (width*2, height*2))

    if level.text_tick >= 0:
        screen.blit(scaled_message, (0, 0))
    pygame.display.flip()

    if not level.pause:
        level.after_tick_status(text_surface, font)
        player.status_after_tick()
        level.increase_timer()

pygame.quit()
