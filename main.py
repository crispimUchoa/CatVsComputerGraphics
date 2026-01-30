import math
import pygame
from entities.level_controller import Level_Controller
from entities.player import Player
from primitives.draw_functions import draw_circle, draw_elipse, draw_polygon
from primitives.fill_functions import flood_fill, scanline_fill, scanline_texture
from primitives.transform_functions import transform
from primitives.viewport_clipping_functions import window_viewport

# Define se vai ser renderizado o MENU ou os mapas jogaveis
MENU = True

#
# MAPEAMENTO DAS TECLAS de movimento
#

key_map = {
    #AÇÕES DO PLAYER
    pygame.K_w: "UP",
    pygame.K_a: "LEFT",
    pygame.K_s: "DOWN",
    pygame.K_d: "RIGHT",
}

#
#INICIALIZA O DISPLAY ------------------------------------------------------
#
DISPLAY_CAPTION = 'Cat Vs Computer Graphics'
pygame.init()
width, height = 800, 640
virtual_screen = pygame.Surface((width, height))
screen = pygame.display.set_mode((width, height), pygame.SRCALPHA)
pygame.display.set_caption(DISPLAY_CAPTION)   
clock = pygame.time.Clock()

running = True

pygame.init()
pygame.mixer.init()


pygame.mixer.music.load("sounds/song.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)



# Definição dos renderizadores de texto -------------------------------------
font = pygame.font.SysFont(None, 24) #Texto do timer
message_font = pygame.font.SysFont(None, 24) #Textos das mensagens exibidas na tela
menu_font = pygame.font.SysFont(None, 48) #Titulo do MENU

MENU_TEXT = 'Cat Vs Computer Graphics'

#Superficies auxiliares --------------------------------------------
MENU_TEXT_RENDER = menu_font.render(MENU_TEXT, False, (255, 255, 255))

text_surface = pygame.Surface((width, height)).convert_alpha()  #Texto
message_surface = pygame.Surface((width, height)).convert_alpha()   #Texto
message_surface.fill((0, 0, 0, 0))

gradient_surface = pygame.Surface((width, height)) # Mapa de gradiente
static_surface = pygame.Surface((width, height)).convert_alpha() #Mapas gerais em tiles
bus_surface = pygame.Surface((width, height), pygame.SRCALPHA) #ônibus

# Inicializa Mapas----------------------------------------------------------------

from levels.home import level_home
from levels.classroom import level_classroom
from levels.street import level_street


# Inicializa elementos de transição de mapas -> player + skip -> próximo mapa ------------------------------
level_home.skip[0].next_level = level_street
level_street.skip[0].next_level = level_home
level_street.skip[1].next_level = level_classroom

#
#PROPORÇÃO DE TEXTURA PADRÃO PARA RETANGULOS -----------------------

uvs_default = [
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0)
]





#   Define player e level controller -------------------------------------------------------------------------

level = Level_Controller(virtual_screen, static_surface, gradient_surface, bus_surface, message_surface, message_font)
player = Player((0, 0))
level.set_level(level_home, player)



# Variaveis de transformação ---------------------------------------------------------
angle = 0
time = 0

s = 1
s_item = 1.1
var_tx = -8
offset = 0

zoom = 0.2

# Configurações iniciais para viewport do minimapa ----------------
world = 0, 0, width, height
viewport = width-width*zoom, 0, width, height*zoom
center = (width/2, height/2)
m_vp = window_viewport(world, viewport)

# Loop do jogo rodando -----------------------------
while running:
    clock.tick(60)

    # Renderização do MENU -------------------------------------------------
    if MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Checa se o clique foi no botão de play (nariz do gato) -> Inicia o jogo ------
                if cx - 10 <= mx <= cx + 32 and cy-10 <= cy + 30:
                    MENU = False

        flood_fill(screen, center, (155,55,200), (255, 0, 255))


        # Desenha gato na tela ------------------------------------------
        draw_elipse(screen, center, 192, 128, (0, 0, 0))
        flood_fill(screen, center, (225, 255, 255), (0, 0, 0))

        cx, cy = center


        # Nariz do gato / botão de play ----------------------------------
        nose = [
        (cx - 10, cy - 10),   
        (cx - 10, cy + 30),  
        (cx + 32, cy + 10),       
    ]


        draw_polygon(screen, nose, (0, 0, 0))


        flood_fill(screen, (cx - 2, cy), (0, 255, 0), (0, 0, 0))    


        # Orelhas ----------------------------------------------------------

        left_ear = [
        (cx - 90, cy - 120),
        (cx - 40, cy - 200),
        (cx - 10, cy - 110),
    ]

        draw_polygon(screen, left_ear, (0, 0, 0))
        flood_fill(screen, (cx - 45, cy - 150), (255, 255, 255), (0, 0, 0))

        right_ear = [
            (cx + 90, cy - 120),
            (cx + 40, cy - 200),
            (cx + 10, cy - 110),
        ]

        draw_polygon(screen, right_ear, (0, 0, 0))
        flood_fill(screen, (cx + 45, cy - 150), (255, 255, 255), (0, 0, 0))

        # Olhos ------------------------------------------------

        eye_left_center = (cx - 40, cy - 20)

        draw_elipse(screen, eye_left_center, 30, 18, (0, 0, 0))   # borda
        flood_fill(screen, eye_left_center, (255, 255, 255), (0, 0, 0))

        draw_circle(screen, eye_left_center, 6, (0, 0, 0))        # pupila
        flood_fill(screen, eye_left_center, (0, 0, 0), (0, 0, 0))

        eye_right_center = (cx + 40, cy - 20)

        draw_elipse(screen, eye_right_center, 30, 18, (0, 0, 0))
        flood_fill(screen, eye_right_center, (255, 255, 255), (0, 0, 0))

        draw_circle(screen, eye_right_center, 6, (0, 0, 0))
        flood_fill(screen, eye_right_center, (0, 0, 0), (0, 0, 0))

        

        # Renderiza o titulo na tela ---------------------------------------------------------------
        screen.blit(MENU_TEXT_RENDER, (width/2 - len(MENU_TEXT)*8,height/2 - len(MENU_TEXT)*12))
        pygame.display.flip()
        continue


    # Incrementa as variaveis de transformação se não estiver pausado -----------------------------
    if not level.pause:
        angle +=0.02
        time += 0.05
        s = 1 + 0.15 * math.sin(angle)
        s_item = 1.10 + 0.05*math.sin(angle)
        var_tx = (-1 - math.sin(angle))*8

    # ---------------------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Checa se o player consegue interagir com o cenario em sua coordenada ----------------------------
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_RETURN and not level.pause:
                level.isskip(player)
                level.player_in_items_range(player)
                level.is_player_meeting_professor(player)

    # Pause e Resume ------------------------------------------------------------------------------
            if event.key == pygame.K_ESCAPE:
                level.toggle_pause()

    # Checa o mapeamento de teclas para setar a direção e mover o player ------------------------
    keys = pygame.key.get_pressed()
    for key, dir in key_map.items():
        
        if keys[key] and not level.is_player_coliding(dir, player) and not level.pause:
            player.move(dir)

        
    # Renderiza o mapa 'classroom' movendo o gradiente ------------------------------
    if level.level == level_classroom:
        offset = (offset - 4) % height
        virtual_screen.blit(gradient_surface, (0, offset - height))
        virtual_screen.blit(gradient_surface, (0, offset))
        level.level.draw_dynamic_details(virtual_screen, angle, s) 
    
    # Renderiza os tiles ----------------------------------------------------------------------

    virtual_screen.blit(static_surface, (0, 0))

    # --------------------------------------------------------------------------------------

    player.show(virtual_screen, uvs_default)
    
    #Faz viewport da posição do player e dos items para o mini-mapa/radar --------------------------

    # ---------------- Renderiza fundo preto ---------------------------
    black_background_fullscreen = [(0, 0), (width, 0), (width, height), (0, height), ]
    black_background_minimap = transform(m_vp, black_background_fullscreen)
    scanline_fill(virtual_screen, black_background_minimap, (0,0,0))

    # ---------------- Renderiza mini-player -------------------------
    player_minimap = transform(m_vp, player.get_vertices())
    scanline_texture(virtual_screen, player_minimap,uvs_default, player.get_texture())

    # ---------------- Renderiza mini-itens -----------------------
    for item in level.level.items:
        ix, iy = item.position
        item_vertices = [
            (ix, iy), (ix + item.w, iy), (ix + item.w, iy + item.h), (ix, iy + item.h),
        ]

        item_minimap = transform(m_vp, item_vertices)
        if not item.is_in_inventory:
            scanline_texture(virtual_screen, item_minimap,uvs_default, item.texture)


    # desenha e renderiza items no mapa ----------------------------------------------
    level.draw_items(virtual_screen, s_item, var_tx, player, uvs_default)
    # -------------------------------------------------------------------------------
    level.show_timer_bar()

    # Exibe a virtal_screen na janela do display ------------------------------
    screen.blit(virtual_screen, (0, 0))
    
    # Exibe a parte superior do onibus -------------------------------------------
    if level.level == level_street:
        screen.blit(bus_surface, (0, 0))


    screen.blit(text_surface, (0, 0))

    # Exibe mensagem que estiver no tempo de atividade, se estiver ---------------- 
    if level.text_tick >= 0:
        screen.blit(message_surface, (0, 0))

    


    pygame.display.flip()

    # Atualiza status de operações que dependem do tempo --------------------------
    if not level.pause:
        level.after_tick_status(text_surface, font)
        player.status_after_tick()
        level.increase_timer()
    # ----------------------------------------------------------------------------------
    
pygame.quit()
