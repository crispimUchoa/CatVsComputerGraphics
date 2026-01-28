import math
import pygame
from entities.player import Player
from entities.skip_level import Skip_Level
from primitives.fill_functions import scanline_fill_gradient
from primitives.functions import scanline_texture, scanline_fill, draw_polygon
from entities.level_controller import Level_Controller
from primitives.transform_functions import create_transform, multiply_matrix, rotation, scale, transform, translation


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
static_surface = pygame.Surface((width, height))
bus_surface = pygame.Surface((width, height), pygame.SRCALPHA)

level = Level_Controller(virtual_screen, static_surface, gradient_surface, bus_surface)
player = Player((0, 0))
level.set_level(level_street, player)
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

offset = 0
while running:
    clock.tick(60)

    angle +=0.02
    time += 0.05
    s = 1 + 0.15 * math.sin(angle)
    
    y+=1
    if y>=height*1.5:
        y=-height*1.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                level.isskip(player)

    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        
        if keys[key] and not player.is_coliding(dir, level):
            player.move(dir)

    virtual_screen.blit(static_surface, (0, 0))
        
    if level.level == level_classroom:
        offset = (offset - 4) % height
        virtual_screen.blit(gradient_surface, (0, offset - height))
        virtual_screen.blit(gradient_surface, (0, offset))
        level.level.draw_dynamic_details(virtual_screen, angle, s) 
    



    player.show(virtual_screen, uvs_default)
    level.show_timer_bar()

    scaled = pygame.transform.scale(virtual_screen, (width*2, height*2))
    scaled_bus = pygame.transform.scale(bus_surface, (width*2, height*2))
    screen.blit(scaled, (0, 0))
    if level.level == level_street:
        screen.blit(scaled_bus, (0, 0))

    pygame.display.flip()

    player.status_after_tick()
    level.increse_timer()

pygame.quit()
