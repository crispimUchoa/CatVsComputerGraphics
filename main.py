import pygame
from entities.player import Player
from primitives.functions import scanline_texture, scanline_fill, draw_polygon
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
width, height = 400, 320
virtual_screen = pygame.Surface((width, height))
screen = pygame.display.set_mode((width*2, 2*height), pygame.SRCALPHA, pygame.SCALED)
pygame.display.set_caption(DISPLAY_CAPTION)
clock = pygame.time.Clock()
running = True

HOUSE_WALL_SPRITE = pygame.image.load('./sprites/tiles/HOUSE_WALL.png').convert()
HOUSE_WALL_FRONT_SPRITE = pygame.image.load('./sprites/tiles/HOUSE_WALL_FRONT.jpeg').convert()
HOUSE_GROUND_SPRITE = pygame.image.load('./sprites/tiles/HOUSE_GROUND.png').convert()

HOUSE_WALL_SPRITES = [HOUSE_WALL_SPRITE, HOUSE_WALL_FRONT_SPRITE]

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
player = Player((200, 150))
level = Level_Controller(virtual_screen)

#
#JOGO RODANDO
#
coliding = False
walls = level.WALLS

default_repeat_x = width / 32
default_repeat_y = height / 32

uvs_default_tiling = [
    (0.0, 0.0),
    (default_repeat_x, 0.0),
    (default_repeat_x, default_repeat_y),
    (0.0, default_repeat_y)
]

static_surface = pygame.Surface((width, height))

scanline_texture(static_surface, [(0, 0), (width, 0), (width, height), (0, height) ], uvs_default_tiling, HOUSE_GROUND_SPRITE)

for wall in walls:
    repeat_x = wall.width / 32
    repeat_y = wall.height / 32
    
    uvs_tiling = [
    (0.0, 0.0),
    (repeat_x, 0.0),
    (repeat_x, repeat_y),
    (0.0, repeat_y)
]
    print(wall.sprite)
    scanline_texture(static_surface, [(wall.position[0], wall.position[1]), (wall.position[0] + wall.width, wall.position[1]), (wall.position[0] + wall.width, wall.position[1] + wall.height), (wall.position[0], wall.position[1] + wall.height)], uvs_tiling, HOUSE_WALL_SPRITES[wall.sprite-1])

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        
        if keys[key] and not player.is_coliding(dir, level):
            player.move(dir)


    
    # screen.blit(static_surface, (0,0))
    # virtual_screen.fill((0, 0, 0))
    virtual_screen.blit(static_surface, (0, 0))
    

    scanline_texture(virtual_screen, player.show(), uvs_default, player.get_texture())

    scaled = pygame.transform.scale(virtual_screen, (width*2, height*2))
    screen.blit(scaled, (0, 0))


    pygame.display.flip()

    player.status_after_tick()
    level.increse_timer()

pygame.quit()
