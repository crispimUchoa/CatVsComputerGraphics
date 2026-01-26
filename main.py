import pygame
from entities.player import Player
from primitives.functions import scanline_texture
from level_controller import Level_Controller


#
# MAPEAMENTO DAS TECLAS
#

key_map = {
    #AÇÕES DO PLAYER
    pygame.K_w: "UP",
    pygame.K_a: "LEFT",
    pygame.K_s: "DOWN",
    pygame.K_d: "RIGHT"
}

#
#INICIALIZA O DISPLAY
#
DISPLAY_CAPTION = 'Cat Vs Computer Graphics - MENU'
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(DISPLAY_CAPTION)
clock = pygame.time.Clock()
running = True

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
player = Player((200, 200))
level = Level_Controller(screen)

#
#JOGO RODANDO
#
coliding = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        
        if keys[key] and not player.is_coliding(dir, level):
            player.move(dir)


    
    screen.fill((0, 0, 0))

    scanline_texture(screen, player.show(), uvs_default, player.get_texture())


    pygame.display.flip()

    clock.tick(60)
    player.after_tick_status()

pygame.quit()
