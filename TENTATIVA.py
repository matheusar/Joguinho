"""Very basic example of using a sprite image to draw a shape more similar 
how you would do it in a real game instead of the simple line drawings used 
by the other examples. 
"""

__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import math, random
from os import path, environ

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk import Vec2d

WHITE = (255, 255, 255)
FPS = 60

img_dir = path.join(path.dirname(__file__), 'imags')
snd_dir = path.join(path.dirname(__file__), 'sons')


environ['SDL_VIDEO_CENTERED'] = '1'
fonte_nome = pygame.font.match_font('sans serif')
width = 1300
height = 600
pygame.init()
screen = pygame.display.set_mode((1300, 600))

clock = pygame.time.Clock()

pygame.mixer.music.load(path.join(snd_dir, 'musica.ogg'))
pygame.mixer.music.set_volume(0.4)
acelera = pygame.mixer.Sound(path.join(snd_dir, 'ferrari-f1.ogg'))
freio = pygame.mixer.Sound(path.join(snd_dir, 'freio.ogg'))
perdeu = pygame.mixer.Sound(path.join(snd_dir, 'perdeu.ogg'))
venceu = pygame.mixer.Sound(path.join(snd_dir, 'venceu.ogg'))
perdeu.set_volume(1)

def texto_tela(surf, text, size, x, y):
    fonte = pygame.font.Font(fonte_nome, size)
    text_surface = fonte.render(text, True, THECOLORS["red"])
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



def initial_screen():
    screen.fill(THECOLORS["black"])
    texto_tela(screen, "BIKE RACE", 64, width / 2, height / 4)
    texto_tela(screen, "Use as setas para se locomover", 22, width / 2, height / 2)
    texto_tela(screen, "Aperte qualquer tecla para iniciar", 19, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                
def final_screen():
    screen.fill(THECOLORS["white"])
    background1 = pygame.image.load(path.join(img_dir, 'tela_azul.jpg')).convert()
    background_rect1 = background1.get_rect()        
    screen.blit(background1, background_rect1)
    texto_tela(screen, "VOCÊ PERDEU!", 64, width / 2, height / 4)
    pygame.display.flip()
    wait = True
    perdeu.play()
    freio.stop()
    acelera.stop()
    while wait:
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                wait = False
    
                
def final_screen2():
    screen.fill(THECOLORS["white"])
    texto_tela(screen, "VOCÊ VENCEU!", 64, width / 2, height / 4)
    pygame.display.flip()
    wait = True
    venceu.play()
    freio.stop()
    acelera.stop()
    while wait:
        clock.tick(60) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                wait = False
        
                

def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600


def main():
    ### Physics stuff
    space = pymunk.Space()
    space.gravity = Vec2d(0.0, -3000.0)
    
    ### Static line
    static_lines = [
            pymunk.Segment(space.static_body, (0.0, 200.0), (200.0, 200.0), 0.0),
            pymunk.Segment(space.static_body, (200.0, 200.0), (300.0, 250.0), 0.0),
            pymunk.Segment(space.static_body, (500.0, 250.0), (600.0, 250.0), 0.0),
            pymunk.Segment(space.static_body, (700.0, 200.0), (800.0, 250.0), 0.0),
            pymunk.Segment(space.static_body, (1000.0, 200.0), (1300.0, 200.0), 0.0),
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
    vs = [(-30,32), (30,32), (25,-37)]
    mass = 1000
    moment = pymunk.moment_for_poly(mass, vs)
    body = pymunk.Body(mass, moment)
    shape = pymunk.Poly(body, vs)
    shape.friction = 0.5
    body.position = x, y
    body.angle = angle
    space.add(body, shape)

    logos = []
    logos.append(shape)
    
    mass = 100
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel1_b = pymunk.Body(mass, moment)
    wheel1_s = pymunk.Circle(wheel1_b, radius)
    wheel1_s.friction = 1.5
    wheel1_s.color = THECOLORS["red"]
    space.add(wheel1_b, wheel1_s)

    mass = 100
    radius = 25
    moment = pymunk.moment_for_circle(mass, 20, radius)
    wheel2_b = pymunk.Body(mass, moment)
    wheel2_s = pymunk.Circle(wheel2_b, radius)
    wheel2_s.friction = 1.5
    wheel2_s.color = THECOLORS['red']
    space.add(wheel2_b, wheel2_s)
    
    speed = 0
    space.add(
        pymunk.SimpleMotor(wheel1_b, body, speed),
        pymunk.SimpleMotor(wheel2_b, body, speed)
    )
    
    space.add(
        pymunk.PinJoint(wheel1_b, body, (0,0), (-30,32)),
        pymunk.PinJoint(wheel1_b, body, (0,0), (-30, -32)),
        pymunk.PinJoint(wheel2_b, body, (0,0), (25,-15)),
        pymunk.PinJoint(wheel2_b, body, (0,0), (25, 15))
        )
    # Inicia pygame.

    ## logo da vaca
    logo = pygame.image.load(path.join(img_dir, "motinha.png")).convert()
    logo_img = pygame.transform.scale(logo, (100, 80))
    logo_img.set_colorkey(WHITE)
    

    #py = 280
    #px = 100
    #px += shape.body.position.x
        
    # Mantem dentro da tela
    #if px >= 1300:
     #   px = 1300 - 1
    #if px < 0:
        #px = 0
    #camera_offset_x = -px
    #camera_offset_y = -py
    #camera = [0, 0]
    #camera[0] = px + camera_offset_x
    #camera[1] = py + camera_offset_y
    
            
    # Centraliza embaixo da tela.
    #centerx = px - camera[0]
    #centery = py - camera[1]
    
    pygame.mixer.music.play(loops=-1)
    
    lol = True
    running = True
    LOLO = True
    while running:
        if lol:     
            initial_screen()
            lol = False
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        pygame.display.set_caption("fps: {0}, debug: {1}".format(clock.get_fps(), shape.body.position))
        #print(shape.body.position.x)
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
                #print('oi')
            # Verifica se apertou alguma tecla.
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    space.gravity = Vec2d(-3000.0, -3000.0)
                    freio.play()
                    acelera.stop()

                if event.key == pygame.K_RIGHT:
                    space.gravity = Vec2d(3000.0, -3000.0)
                    acelera.play()
                    freio.stop()
            
                    
            # Verifica se soltou alguma tecla.
            elif event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    space.gravity = Vec2d(0.0, -1000.0)
                    
                    
                if event.key == pygame.K_RIGHT:
                    space.gravity = Vec2d(0.0, -1000.0)
                    acelera.stop()
                    freio.play()
                    
        if shape.body.position.y <= 100:
            final_screen()
        if shape.body.position.x >= 1200:
            final_screen2()
        ### Update physics
        dt = 1.0 / FPS
        space.step(dt)
            
        ### Draw stuff
        screen.fill(THECOLORS["white"])
        background = pygame.image.load(path.join(img_dir, 'fundo.png')).convert()
        background_rect = background.get_rect()
        #background_rect.x = -camera[0]
        #background_rect.y = -camera[1]        
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
            
            
           

        for line in static_lines:
            body = line.body
            
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = pv1.x, flipy(pv1.y)
            p2 = pv2.x, flipy(pv2.y)
            pygame.draw.lines(screen, THECOLORS["red"], False, [p1,p2], 2)
            
        
        ### Flip screen
        pygame.display.flip()
    pygame.quit()

pygame.mixer.music.stop()
        
if __name__ == '__main__':
    main()