# -*- coding: utf-8 -*-

# Importando as bibliotecas necessárias.
import pygame
from os import path
import pymunk
import random
# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'imags')

# Dados gerais do jogo.
WIDTH = 600 # Largura da tela
HEIGHT = 600 # Altura da tela
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
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        player_img = pygame.image.load(path.join(img_dir, "motinha.png")).convert()
        self.image = player_img
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(player_img, (200, 160))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        self.rect.centerx = -100
        self.rect.bottom = HEIGHT
    def add_ball(space):
        """Add a ball to the given space at a random position"""
        mass = 1
        radius = 14
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(120,380)
        body.position = (x, 550)
        shape = pymunk.Circle(body, radius, (0,0))
        space.add(body, shape)
        return shape


# Classe Jogador que representa a nave
class Background(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, n):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        background = pygame.image.load(path.join(img_dir, 'fundo.png')).convert()
       
        # Carrega o fundo do jogo
        background_rect = background.get_rect()
        self.image = background
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Centraliza embaixo da tela.
        if(n==1):
            self.rect.centerx = 0
        else:
            self.rect.centerx = -WIDTH
            
        self.rect.bottom = HEIGHT
        
        # Velocidade da nave
        self.back_speedx = 0
    
    # Metodo que atualiza a posição da navinha
    def update(self):
        self.rect.x += self.back_speedx
        if(self.rect.x == WIDTH):
            self.rect.x = -WIDTH
        screen.fill(WHITE)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)


# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Nome do jogo
pygame.display.set_caption("Navinha")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Cria uma nave. O construtor será chamado automaticamente.
back1 = Background(1)
back2 = Background(2)
player = Player()

# Cria um grupo de todos os sprites e adiciona a nave.
all_sprites = pygame.sprite.Group()
all_sprites.add(player)




# Comando para evitar travamentos.
try:
    
    # Loop principal.
    running = True
    while running:
        
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
                    back1.back_speedx = -8
                    back2.back_speedx = -8
                if event.key == pygame.K_RIGHT:
                    back1.back_speedx = 8
                    back2.back_speedx = 8                    
            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    back1.back_speedx = 0
                    back2.back_speedx = 0
                if event.key == pygame.K_RIGHT:
                    back1.back_speedx = 0
                    back2.back_speedx = 0
                    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
            
        # A cada loop, redesenha o fundo e os sprites
        #
       
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
finally:
    pygame.quit()
