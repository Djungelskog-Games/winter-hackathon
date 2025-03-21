import pygame
from constants import PRETO, FONT2, SOUNDS, BRANCO
import math
import sys

class SplashScreen:
    def __init__(self, screen, font, largura, altura):
        # Inicializa os atributos da classe
        self.screen = screen  # Superfície onde o ecrã de splash será desenhado
        self.font = font  # Fonte usada para renderizar o texto
        self.largura = largura  # Largura do ecrã
        self.altura = altura  # Altura do ecrã

        # Carrega e toca a música de fundo em loop
        SOUNDS['menu'].play(-1)

    def run(self):
        try:
            # Tenta carregar a imagem de fundo do ecrã de splash
            splash_image = pygame.image.load("assets/Starting/Starting_Screen.png").convert()
            new_size = (self.largura, self.altura)  # Redimensiona a imagem
            splash_image = pygame.transform.smoothscale(splash_image, new_size)
            image_rect = splash_image.get_rect(center=(self.largura // 2, self.altura // 2))  # Centraliza a imagem
        except pygame.error:
            # Caso a imagem não seja encontrada, cria um fundo preto
            splash_image = pygame.Surface((self.largura, self.altura))
            splash_image.fill(PRETO)
            image_rect = splash_image.get_rect(topleft=(0, 0))

        try:
            # Tenta carregar a imagem de sobreposição (texto animado)
            overlay_image = pygame.image.load("assets/Starting/faunabellum.png").convert_alpha()
            overlay_image = pygame.transform.smoothscale(overlay_image, (350, 167))
            overlay_rect = overlay_image.get_rect(center = (self.largura // 4, 150))
        except pygame.error:
            # Caso a imagem não seja encontrada, cria uma superfície semi-transparente
            overlay_image = pygame.Surface((600, 100), pygame.SRCALPHA)
            overlay_image.fill((0, 0, 0, 180))
            overlay_rect = overlay_image.get_rect(center=(self.largura // 2, 150))

        try:
            overlay_image2 = pygame.image.load("assets/Starting/Starting_Text.png").convert_alpha()
            overlay_image2 = pygame.transform.smoothscale(overlay_image2, (495, 123))
            overlay_rect2 = overlay_image2.get_rect(center=(self.largura - 300, 500))  # Centraliza o texto
        except pygame.error:
            # Caso ocorra um erro, cria uma superfície semi-transparente
            overlay_text = pygame.Surface((600, 100), pygame.SRCALPHA)
            overlay_text.fill((0, 0, 0, 180))
            overlay_rect2 = overlay_text.get_rect(center=(self.largura // 2, 250))

        font2 = pygame.font.Font(FONT2, 15)
        overlay_credit = font2.render("©Djungelskog Games 2025", True, BRANCO)
        overlay_credit_rect = overlay_credit.get_rect(center=(self.largura - 115, self.altura - 20))

        # Configurações da animação
        amplitude = 5  # Altura do movimento em pixels
        velocidade = 0.04  # Velocidade da animação
        angulo = 0  # Ângulo inicial para a função seno
        clock = pygame.time.Clock()  # Relógio para controlar a taxa de atualização

        while True:
            # Calcula o movimento vertical usando a função seno
            deslocamento_y = math.sin(angulo) * amplitude
            overlay_rect.centery = 150 + deslocamento_y  # Aplica o deslocamento à posição vertical
            angulo += velocidade  # Atualiza o ângulo para a próxima iteração

            # Redesenha todos os elementos no ecrã
            self.screen.blit(splash_image, image_rect)  # Fundo
            self.screen.blit(overlay_image, (self.largura // 4 - 175, overlay_rect.centery - 100))  # Texto animado
            self.screen.blit(overlay_image2, overlay_rect2)  # Instrução para continuar
            self.screen.blit(overlay_credit, overlay_credit_rect)
            pygame.display.flip()  # Atualiza o ecrã

            # Controla a taxa de atualização para 60 FPS
            clock.tick(60)

            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    SOUNDS['menu'].stop()  # Para a música de fundo
                    return  # Sai da função e encerra o ecrã de splash
