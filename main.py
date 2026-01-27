import pygame
from entities.player import Player
from entities.skip_level import Skip_Level
from primitives.functions import scanline_texture, scanline_fill, draw_polygon
from entities.level_controller import Level_Controller


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
from levels.street import level_street

LEVELS = [level_home, level_street]

#
#PROPORÇÃO DE TEXTURA PADRÃO PARA RETANGULOS
#
uvs_default = [
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0)
]



#
#DEFINE PLAYER
#
static_surface = pygame.Surface((width, height))
level = Level_Controller(virtual_screen, static_surface)
player = Player((0, 0))
level.set_level(level_home, player)

#
#JOGO RODANDO
#
coliding = False
walls = level.WALLS






i = 1
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                level.isskip(player, LEVELS[level.skip_level.next_level])

    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        
        if keys[key] and not player.is_coliding(dir, level):
            player.move(dir)

        


    
    # screen.blit(static_surface, (0,0))
    # virtual_screen.fill((0, 0, 0))
    virtual_screen.blit(static_surface, (0, 0))
    
    player.show(virtual_screen, uvs_default)

    scaled = pygame.transform.scale(virtual_screen, (width*2, height*2))
    screen.blit(scaled, (0, 0))


    pygame.display.flip()

    player.status_after_tick()
    level.increse_timer()

pygame.quit()
