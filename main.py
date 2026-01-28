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

BUS_SPRITE = pygame.image.load('./sprites/bus.png').convert_alpha()



from levels.home import level_home
from levels.classroom import level_classroom
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

gradient_surface = pygame.Surface((width, height))


#
#DEFINE PLAYER
#
static_surface = pygame.Surface((width, height))
level = Level_Controller(virtual_screen, static_surface)
player = Player((0, 0))
level.set_level(level_classroom, player)
# scanline_texture(static_surface, [ (width - 22*16, height - 15*16),(width, height - 15*16),(width, height - 7*16),(width - 22*16, height - 7*16) ], uvs_default, BUS_SPRITE)
#
#JOGO RODANDO
#
coliding = False
walls = level.WALLS

def draw_details(surface):
    width = 400
    height = 320
    c1 = (127, 0, 127)
    c2 = (196, 32, 127)
    scanline_fill_gradient(surface, 
                        [
                            (0, 0), (width, 0), (width, height/2),(width, height), (0, height), (0, height/2)
                        ],
                        [
                            c1, c1, c2, c1, c1, c2,
                        ]

                        )

draw_details(gradient_surface)

professor_head_out_1 = [(width/2 - 32, 16), (width/2 + 32, 16), (width/2 + 32, 51), (width/2 - 32, 51) ]
professor_head_out_2 = [(width/2 - 31, 17), (width/2 + 31, 17), (width/2 + 31, 50), (width/2 - 31, 50) ]
professor_head_in = [(width/2 - 30, 18), (width/2 + 30, 18), (width/2 + 30, 50), (width/2 - 30, 50) ]
professor_body = [(width/2 - 6, 30), (width/2 + 6, 30), (width/2 + 6, 100), (width/2 + 32, 108), (width/2 - 32, 108), (width/2 - 6, 100)]

pcx = sum(p[0] for p in professor_head_out_1) / len(professor_head_out_1)
pcy = sum(p[1] for p in professor_head_out_1) / len(professor_head_out_1)

i = 1
y = 0

angle = 0
time = 0

offset = 0
while running:
    clock.tick(60)
    y+=1
    if y>=height*1.5:
        y=-height*1.5
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and level.skip_level and level.skip_level.next_level:
                level.isskip(player, LEVELS[level.skip_level.next_level])

    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        
        if keys[key] and not player.is_coliding(dir, level):
            player.move(dir)

    virtual_screen.blit(static_surface, (0, 0))
        
    offset = (offset - 4) % height
    virtual_screen.blit(gradient_surface, (0, offset - height))
    virtual_screen.blit(gradient_surface, (0, offset))
    
    angle +=0.02
    time += 0.05
    s = 1 + 0.15 * math.sin(angle)

    m = create_transform()
    m = multiply_matrix(translation(-pcx, -pcy), m)
    m = multiply_matrix(rotation(math.sin(angle)/4), m)
    m = multiply_matrix(scale(s, s), m)
    m = multiply_matrix(translation(pcx, pcy), m)
    pho1 = transform(m, professor_head_out_1)
    # pho2 = transform(m, professor_head_out_2)
    phin = transform(m, professor_head_in)

    scanline_fill(virtual_screen, professor_body, (32, 32, 32))
    scanline_fill(virtual_screen, pho1, (32, 32, 32))
    # draw_polygon(virtual_screen, pho2, (32, 32, 32))
    scanline_fill(virtual_screen, phin, 'black')


    player.show(virtual_screen, uvs_default)
    level.show_timer_bar()

    scaled = pygame.transform.scale(virtual_screen, (width*2, height*2))
    screen.blit(scaled, (0, 0))

    pygame.display.flip()

    player.status_after_tick()
    level.increse_timer()

pygame.quit()
