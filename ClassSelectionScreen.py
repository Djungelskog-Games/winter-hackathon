import pygame
from constants import BRANCO, PRETO, SOUNDS, SECRET, VERMELHO
import sys
from BotaoIcone import BotaoIcone

# Classe que representa a tela de seleção de classes
class ClassSelectionScreen:
    # Inicializa a tela de seleção de classes
    def __init__(self, font):
        # Toca o som de escolha
        SOUNDS['escolher'].play()
        self.largura = 1000
        self.altura = 700
        self.font = font
        self.selected_p1 = None
        self.selected_p2 = None
        self.confirm_enabled = False
        self.secret_counter = 0
        # Inicializa a tela do pygame
        self.screen = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("")
        # Carrega a imagem de fundo
        try:
            self.bg_image = pygame.image.load("assets/Classes/Background.jpg").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.largura, self.altura))
        except pygame.error:
            self.bg_image = None
        # Inicializa os botões de seleção de classes
        self.icon_spacing = 250
        self.base_x = self.largura // 2
        self.player1_y = 200
        self.player2_y = 450
        # Inicializa os botões de seleção de classes
        self.buttons_p1 = [
            BotaoIcone(self.base_x - self.icon_spacing, self.player1_y, 
                       "assets/Classes/Lebre.png", "Lebre", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x, self.player1_y, 
                       "assets/Classes/Bufo.png", "Bufo", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player1_y, 
                       "assets/Classes/Raposa.png", "Raposa", self.handle_class_selection, "p1")    
        ]
        self.buttons_p2 = [
            BotaoIcone(self.base_x - self.icon_spacing, self.player2_y, 
                       "assets/Classes/Lebre.png", "Lebre", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x, self.player2_y, 
                       "assets/Classes/Bufo.png", "Bufo", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player2_y, 
                       "assets/Classes/Raposa.png", "Raposa", self.handle_class_selection, "p2")
        ]
        self.confirm_button = BotaoIcone(self.largura//2, self.altura - 100, 
                                         "assets/Classes/confirm_button.png", "Confirmar", 
                                         lambda p, c: self.confirm_selection(), "confirm", (700, 90))
        # Inicializa os atributos de estatísticas das classes
        self.stats = {
            "Lebre": {"Vida": 40, "Ataque": 8, "Movimento": 4, "Alcance": 1},
            "Bufo": {"Vida": 50, "Ataque": 10, "Movimento": 3, "Alcance": 2},
            "Raposa": {"Vida": 60, "Ataque": 12, "Movimento": 2, "Alcance": 3}
        }
        self.hovered_class = None
    # Atualiza o estado do botão de confirmação
    def update_confirm_status(self):
        self.confirm_enabled = (self.selected_p1 is not None) and (self.selected_p2 is not None)
    # Lida com a seleção de classe
    def handle_class_selection(self, player, class_name):
        if player == "p1":
            self.selected_p1 = class_name
        elif player == "p2":
            self.selected_p2 = class_name
        self.update_confirm_status()
    # Confirma a seleção
    def confirm_selection(self):
        if self.confirm_enabled:
            self.running = False
    # Desenha a dica de ferramenta
    def draw_tooltip(self):
        if self.hovered_class:
            stats = self.stats[self.hovered_class]
            tooltip_width = 200
            tooltip_height = 130

            x, y = pygame.mouse.get_pos()
            x += 20
            y += 20
            
            tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
            tooltip_surface.fill((0, 0, 0, 150))
            title = self.font.render(self.hovered_class, True, BRANCO)
            tooltip_surface.blit(title, (10, 5))
            
            y_offset = 30
            for key, value in stats.items():
                text = self.font.render(f"{key}: {value}", True, BRANCO)
                tooltip_surface.blit(text, (10, y_offset))
                y_offset += 25
            
            self.screen.blit(tooltip_surface, (x, y))
    # Executa a tela de seleção de classes
    def run(self):
        self.running = True
        # Inicializa o relógio
        clock = pygame.time.Clock()
        # Loop principal
        while self.running:
            self.screen.fill(PRETO)
            # Desenha a imagem de fundo
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            text_p1 = self.font.render("Jogador 1", True, VERMELHO)
            self.screen.blit(text_p1, text_p1.get_rect(center=(self.largura//2, 75)))
            text_p2 = self.font.render("Jogador 2", True, VERMELHO)
            self.screen.blit(text_p2, text_p2.get_rect(center=(self.largura//2, 325)))
            
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_class = None
            for btn in self.buttons_p1 + self.buttons_p2:
                if btn.rect.collidepoint(mouse_pos):
                    self.hovered_class = btn.class_name

            for btn in self.buttons_p1 + self.buttons_p2:
                btn.selected = ((self.selected_p1 == btn.class_name and btn.player == "p1") or 
                                (self.selected_p2 == btn.class_name and btn.player == "p2"))
                btn.draw(self.screen)
            
            self.confirm_button.image.set_alpha(255 if self.confirm_enabled else 128)
            self.confirm_button.draw(self.screen)
            
            self.draw_tooltip()

            # Lida com eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Lida com a seleção de classes
                elif self.secret_counter >= len(SECRET):
                    self.handle_class_selection("p1", "Urso")
                    self.handle_class_selection("p2", "Urso")
                    self.confirm_selection()
                    SOUNDS['djungelskog'].play()
                # Lida com eventos de botões
                elif event.type == pygame.KEYDOWN:
                    if event.key == SECRET[self.secret_counter]:
                        self.secret_counter += 1
                        SOUNDS['botao'].play()
                    else:
                        self.secret_counter = 0
                # Lida com eventos de botões
                for btn in self.buttons_p1 + self.buttons_p2 + [self.confirm_button]:
                    btn.handle_event(event)
            # Atualiza o ecrã             
            pygame.display.flip()
            clock.tick(60)
