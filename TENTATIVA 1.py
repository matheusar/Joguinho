# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:38:24 2019

@author: DELL
"""

# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import pymunk
import random
import math
from pygame.locals import *
from pygame.color import *
from pymunk import Vec2d

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'imags')

# Dados gerais do jogo.
WIDTH = 1300 # Largura da tela
HEIGHT = 380 # Altura da tela
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Criar classe background
#Criar duas imagens juntas excedendo o width mesmo (0-width)(0)
#Quando uma imagem passar inteira pela tela reposicionar ela pro começo (x0-width)

# Classe Jogador que representa a nave

class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, camera):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        self.camera = camera
        
        # Carregando a imagem de fundo.
        player_img = pygame.image.load(path.join(img_dir, "motinha.png")).convert()
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (200, 160))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        self.px = 100
        self.py = HEIGHT - 100

        self.camera_offset_x = -self.px
        self.camera_offset_y = -self.py
        
        self.camera.cx = self.px + self.camera_offset_x
        self.camera.cy = self.py + self.camera_offset_y
            
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = self.px - self.camera.cx
        self.rect.centery = self.py - self.camera.cy
        
        # Velocidade da nave
        self.speedx = 0
        
    
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.px += self.speedx
        
        # Mantem dentro da tela
        if self.px >= WIDTH:
            self.px = WIDTH - 1
        if self.px < 0:
            self.px = 0

        self.camera.cx = self.px + self.camera_offset_x
        self.camera.cy = self.py + self.camera_offset_y
            
        # Centraliza embaixo da tela.
        self.rect.centerx = self.px - self.camera.cx
        self.rect.centery = self.py - self.camera.cy

class Camera:
    def __init__(self):
        self.cx = 0
        self.cy = 0

# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Nome do jogo
pygame.display.set_caption("Motinha")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

background = pygame.image.load(path.join(img_dir, 'fundo.png')).convert()
background_rect = background.get_rect()

camera = Camera()

# Cria uma nave. O construtor será chamado automaticamente.
logo = Player(camera)
# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(logo)

# Comando para evitar travamentos.
def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y+600

def main():
            
    pygame.init()
    screen = pygame.display.set_mode((1300, 380))
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
    static_lines = [pymunk.Segment(space.static_body, (200.0, 0.0), (407.0, 246.0), 0.0)
                    ,pymunk.Segment(space.static_body, (407.0, 246.0), (1200.0, 0.0), 0.0)
                    ,pymunk.Segment(space.static_body, (0.0, 0.0), (1300.0, 0.0), 0.0)
                    ,pymunk.Segment(space.static_body, (0.0, 0.0), (0.0, 600.0), 0.0)
                    ,pymunk.Segment(space.static_body, (1300.0, 0.0), (1300.0, 600.0), 0.0)
                    ]
    for l in static_lines:
        l.friction = 0.5
    space.add(static_lines)

    ticks_to_next_spawn = 10

    # Loop principal.
    running = True
    while running:
        ticks_to_next_spawn -= 1
        if ticks_to_next_spawn == 1:
            ticks_to_next_spawn = 0
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
                    space.gravity = Vec2d(-5000.0, -3000.0)
                if event.key == pygame.K_RIGHT:
                    space.gravity = Vec2d(5000.0, -3000.0)
                    
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    space.gravity = Vec2d(0.0, -3000.0)
                if event.key == pygame.K_RIGHT:
                    space.gravity = Vec2d(0.0, -3000.0)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False             
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite
        pygame.display.flip()
        clock.tick(50)
        pygame.display.set_caption("fps: " + str(clock.get_fps()))            
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
            
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        background_rect.x = -camera.cx
        background_rect.y = -camera.cy        
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
if __name__ == '__main__':
    main()
