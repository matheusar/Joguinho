"""Very basic example of using a sprite image to draw a shape more similar 
how you would do it in a real game instead of the simple line drawings used 
by the other examples. 
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math, random
from os import path

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d

WHITE = (255, 255, 255)
FPS = 60

img_dir = path.join(path.dirname(__file__), 'imags')

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600


def main():
    ### Physics stuff
    space = pymunk.Space()
    space.gravity = Vec2d(0.0, -3000.0)
    
    ### Static line
    static_lines = [
            pymunk.Segment(space.static_body, (200.0, 0.0), (407.0, 100.0), 0.0),
            pymunk.Segment(space.static_body, (407.0, 100.0), (1200.0, 0.0), 0.0),
            pymunk.Segment(space.static_body, (0.0, 0.0), (1300.0, 0.0), 0.0),
            pymunk.Segment(space.static_body, (0.0, 0.0), (0.0, 600.0), 0.0),
            pymunk.Segment(space.static_body, (1300.0, 0.0), (1300.0, 600.0), 0.0)
    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

    # Adiciona vaca.
    x = 20
    y = 500
    angle = math.pi
    vs = [(-60,50), (60,50), (40,-75)]
    mass = 10
    moment = pymunk.moment_for_poly(mass, vs)
    body = pymunk.Body(mass, moment)
    shape = pymunk.Poly(body, vs)
    shape.friction = 0.5
    body.position = x, y
    body.angle = angle
    
    space.add(body, shape)

    logos = []
    logos.append(shape)
    # Inicia pygame.
    pygame.init()
    screen = pygame.display.set_mode((1300, 600))

    clock = pygame.time.Clock()
    
    ## logo da vaca
    logo = pygame.image.load(path.join(img_dir, "motinha.png")).convert()
    logo_img = pygame.transform.scale(logo, (200, 160))
    logo_img.set_colorkey(WHITE)
    

    px += shape.body.position.x
        
    # Mantem dentro da tela
    if px >= 1300:
        px = 1300 - 1
    if px < 0:
        px = 0

    camera.x = px + camera_offset_x
    camera.y = py + camera_offset_y
        
            
    # Centraliza embaixo da tela.
    rect.centerx = px - camera.x
    rect.centery = py - camera.y
        
    running = True
    while running:
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        pygame.display.set_caption("fps: {0}, debug: {1}".format(clock.get_fps(), shape.body.position))
        print(shape.body.position.x)
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                print('oi')
            # Verifica se apertou alguma tecla.
            elif event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    space.gravity = Vec2d(-5000.0, -3000.0)
                if event.key == pygame.K_RIGHT:
                    space.gravity = Vec2d(5000.0, -3000.0)
                    
            # Verifica se soltou alguma tecla.
            elif event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    space.gravity = Vec2d(0.0, -3000.0)
                if event.key == pygame.K_RIGHT:
                    space.gravity = Vec2d(0.0, -3000.0)
       
        ### Update physics
        dt = 1.0 / FPS
        space.step(dt)
            
        ### Draw stuff
        screen.fill(THECOLORS["white"])
        background = pygame.image.load(path.join(img_dir, 'fundo.png')).convert()
        background_rect = background.get_rect()
        background_rect.x = -camera.x
        background_rect.y = -camera.y        
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
        pygame.display.flip()
        
if __name__ == '__main__':
    main()