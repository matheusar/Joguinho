"""Very basic example of using a sprite image to draw a shape more similar 
how you would do it in a real game instead of the simple line drawings used 
by the other examples. 
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math, random

import pygame
from pygame.locals import *
from pygame.color import *
from os import path
import pymunk
from pymunk import Vec2d

WHITE = (255, 255, 255)
FPS = 60

img_dir = path.join(path.dirname(__file__), 'imags')

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

def main():
            
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True
    
    ### Physics stuff
    space = pymunk.Space()
    space.gravity = Vec2d(0.0, -3000.0)
    
    ## logo
    logo = pygame.image.load(path.join(img_dir, "motinha.png")).convert()
    logos = []
    logo_img = pygame.transform.scale(logo, (200, 160))
    logo_img.set_colorkey(WHITE)
    ### Static line
    static_lines = [pymunk.Segment(space.static_body, (11.0, 280.0), (407.0, 246.0), 0.0)
                    ,pymunk.Segment(space.static_body, (407.0, 246.0), (407.0, 343.0), 0.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

    ticks_to_next_spawn = 10
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            
        
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn == 1:
            ticks_to_next_spawn = 0
            x = 20
            y = 500
            angle = math.pi
            vs = [(-50,40), (50,40), (40,-75)]
            mass = 10
            moment = pymunk.moment_for_poly(mass, vs)
            body = pymunk.Body(mass, moment)
            shape = pymunk.Poly(body, vs)
            shape.friction = 0.5
            body.position = x, y
            body.angle = angle
            
            space.add(body, shape)
            logos.append(shape)
       
        ### Update physics
        dt = 1.0/60.0
        for x in range(1):
            space.step(dt)
            
        ### Draw stuff
        screen.fill(THECOLORS["white"])
        background = pygame.image.load(path.join(img_dir, 'fundo.png')).convert()
        background_rect = background.get_rect()
        screen.blit(background, background_rect)

        for logo_shape in logos:
            # image draw
            p = logo_shape.body.position
            p = Vec2d(p.x, flipy(p.y))
            
            # we need to rotate 180 degrees because of the y coordinate flip
            angle_degrees = math.degrees(logo_shape.body.angle) + 180 
            rotated_logo_img = pygame.transform.rotate(logo_img, angle_degrees)
            
            offset = Vec2d(rotated_logo_img.get_size()) / 2.
            p = p - offset
            
            screen.blit(rotated_logo_img, p)
            
            # debug draw
            ps = [p.rotated(logo_shape.body.angle) + logo_shape.body.position for p in logo_shape.get_vertices()]
            ps = [(p.x, flipy(p.y)) for p in ps]
            ps += [ps[0]]
            pygame.draw.lines(screen, THECOLORS["red"], False, ps, 1)
           

        for line in static_lines:
            body = line.body
            
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = pv1.x, flipy(pv1.y)
            p2 = pv2.x, flipy(pv2.y)
            pygame.draw.lines(screen, THECOLORS["lightgray"], False, [p1,p2], 2)

        ### Flip screen
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                running = False
            
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = -8
                if event.key == pygame.K_RIGHT:
                    player.speedx = 8
                    
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    player.speedx = 0
                if event.key == pygame.K_RIGHT:
                    player.speedx = 0
                    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))
        
if __name__ == '__main__':
    main()