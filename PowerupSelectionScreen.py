import pygame
from PowerupButton import PowerupButton
from constants import FONT, PRETO, VERMELHO
import math
import sys

class PowerupSelectionScreen:
    def __init__(self, screen, font, powerups, player):
        # Inicializa os atributos da classe
        self.screen = screen  # Superfície onde o ecrã de seleção de powerups será desenhado
        self.font = font  # Fonte usada para renderizar o texto
        self.powerups = powerups  # Lista de powerups disponíveis
        self.player = player  # Nome do jogador que está escolhendo o powerup
        self.selected_powerup = None  # Powerup selecionado pelo jogador
        self.buttons = []  # Lista para armazenar os botões de powerup
        
        try:
            # Tenta carregar a imagem de fundo do ecrã de seleção de powerups
            self.powerup_bg = pygame.image.load("assets/Classes/Background.png")
        except pygame.error:
            self.powerup_bg = None  # Caso a imagem não seja encontrada

        pygame.display.flip()  # Atualiza o ecrã

        # Configurações dos botões de powerup
        button_width = 300  # Largura do botão
        button_height = 150  # Altura do botão
        spacing = 30  # Espaçamento entre os botões
        total_width = 3 * button_width + 2 * spacing  # Largura total ocupada pelos botões
        start_x = (screen.get_width() - total_width) // 2  # Posição inicial no eixo X
        y = screen.get_height() // 2 - button_height // 2  # Posição no eixo Y

        # Cria os botões para cada powerup
        for i, powerup in enumerate(powerups):
            x = start_x + i * (button_width + spacing)
            btn = PowerupButton(x, y, button_width, button_height, powerup, self.select_powerup)
            self.buttons.append(btn)

        self.bg_y = 0

    def select_powerup(self, powerup):
        # Define o powerup selecionado
        self.selected_powerup = powerup

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        angulo = 0
        while self.running:
            self.screen.fill(PRETO)
            if self.powerup_bg:
                self.screen.blit(self.powerup_bg, (0, self.bg_y))
                self.bg_y -= 0.5
                if self.bg_y < -self.powerup_bg.get_height():
                    self.bg_y = 0

            # Calcula o movimento vertical usando a função seno
            amplitude = 10  # Altura do movimento em pixels
            velocidade = 0.05  # Velocidade da animação

            # Renderiza o texto do título com animação
            title_font = pygame.font.Font(FONT, 70)  # Fonte para o título
            title_text = title_font.render(f"{self.player.upper()} - Escolhe um Powerup:", True, VERMELHO)
            title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 100 + math.sin(angulo) * amplitude))
            self.screen.blit(title_text, title_rect)

            # Desenha os botões de powerup
            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()  # Atualiza o ecrã

            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Verifica se algum botão foi clicado
                    for btn in self.buttons:
                        if btn.rect.collidepoint(event.pos):
                            btn.on_click()  # Seleciona o powerup
                            return self.selected_powerup  # Retorna o powerup selecionado
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None  # Retorna None se o jogador pressionar ESC

            angulo += velocidade  # Atualiza o ângulo para a próxima iteração

            clock.tick(60)  # Controla a taxa de atualização para 60 FPS