import pygame
from constants import PRETO, BRANCO, FONT, VERMELHO 
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
        pygame.mixer.music.load("assets/Sounds/song_mainmenu.wav")
        pygame.mixer.music.play(-1)

    def run(self):
        try:
            # Tenta carregar a imagem de fundo do ecrã de splash
            splash_image = pygame.image.load("assets/Starting/Starting_Screen.png").convert()
            original_size = splash_image.get_size()
            new_size = (int(original_size[0] * 0.8), int(original_size[1] * 0.8))  # Redimensiona a imagem
            splash_image = pygame.transform.scale(splash_image, new_size)
            image_rect = splash_image.get_rect(center=(self.largura // 2, self.altura // 2))  # Centraliza a imagem
        except pygame.error:
            # Caso a imagem não seja encontrada, cria um fundo preto
            splash_image = pygame.Surface((self.largura, self.altura))
            splash_image.fill(PRETO)
            image_rect = splash_image.get_rect(topleft=(0, 0))
        
        try:
            # Tenta carregar a imagem de sobreposição (texto animado)
            overlay_image = pygame.image.load("assets/Starting/Starting_Text.png").convert_alpha()
            overlay_rect = overlay_image.get_rect(center=(self.largura // 2, 150))  # Centraliza a imagem
        except pygame.error:
            # Caso a imagem não seja encontrada, cria uma superfície semi-transparente
            overlay_image = pygame.Surface((600, 100), pygame.SRCALPHA)
            overlay_image.fill((0, 0, 0, 180))
            overlay_rect = overlay_image.get_rect(center=(self.largura // 2, 150))
        
        try:
            # Tenta renderizar o texto "Pressione qualquer tecla para continuar"
            text_font = pygame.font.Font(FONT, 60)
            overlay_text = text_font.render("Pressione qualquer tecla para continuar", True, VERMELHO)
            overlay_rect2 = overlay_text.get_rect(center=(self.largura // 2, 550))  # Centraliza o texto
        except pygame.error:
            # Caso ocorra um erro, cria uma superfície semi-transparente
            overlay_text = pygame.Surface((600, 100), pygame.SRCALPHA)
            overlay_text.fill((0, 0, 0, 180))
            overlay_rect2 = overlay_text.get_rect(center=(self.largura // 2, 250))

        # Configurações da animação
        amplitude = 10  # Altura do movimento em pixels
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
            self.screen.blit(overlay_image, overlay_rect)  # Texto animado
            self.screen.blit(overlay_text, overlay_rect2)  # Instrução para continuar
            pygame.display.flip()  # Atualiza o ecrã

            # Controla a taxa de atualização para 60 FPS
            clock.tick(60)

            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()  # Para a música de fundo
                    return  # Sai da função e encerra o ecrã de splash