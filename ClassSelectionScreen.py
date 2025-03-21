import pygame
import math  # Add math import for sine function
from constants import BRANCO, PRETO, SOUNDS, SECRET, VERMELHO, AZUL, FONT2
import sys
import time
from Player import Player
from BotaoIcone import BotaoIcone

class ClassSelectionScreen:
    def __init__(self, font):
        SOUNDS['escolher'].play()
        self.largura = 960
        self.altura = 640
        self.font = font
        self.selected_p1 = None
        self.selected_p2 = None
        self.confirm_enabled = False
        self.secret_counter = 0
        self.animation_offset = 0
        self.animation_speed = 0.05
        self.amplitude = 10  # Amplitude of the sine wave

        self.screen = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Fauna Bellum")
        try:
            self.bg_image = pygame.image.load("assets/Classes/Background.png")
        except pygame.error:
            self.bg_image = None

        self.icon_spacing = 200
        self.base_x = self.largura // 2 + 120
        self.player1_y = 150
        self.player2_y = 400

        # Initialize buttons with phases
        self.buttons_p1 = [
            BotaoIcone(self.base_x - 2 * self.icon_spacing, self.player1_y,
               "assets/Classes/Salamandra.png", "Salamandra", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x - self.icon_spacing, self.player1_y,
               "assets/Classes/Lebre.png", "Lebre", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x, self.player1_y,
               "assets/Classes/Bufo.png", "Bufo", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player1_y,
               "assets/Classes/Raposa.png", "Raposa", self.handle_class_selection, "p1")
        ]
        # Assign phases to player 1 buttons
        for i, btn in enumerate(self.buttons_p1):
            btn.phase = i * (math.pi / 2)  # Stagger phases by 90 degrees

        self.buttons_p2 = [
            BotaoIcone(self.base_x - 2 * self.icon_spacing, self.player2_y,
                "assets/Classes/Salamandra.png", "Salamandra", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x - self.icon_spacing, self.player2_y,
                "assets/Classes/Lebre.png", "Lebre", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x, self.player2_y,
                "assets/Classes/Bufo.png", "Bufo", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player2_y,
                "assets/Classes/Raposa.png", "Raposa", self.handle_class_selection, "p2")
        ]
        # Assign phases to player 2 buttons (offset by pi for opposite movement)
        for i, btn in enumerate(self.buttons_p2):
            btn.phase = i * (math.pi / 2) + math.pi

        self.confirm_button = BotaoIcone(self.largura//2, self.altura - 75,
                                         "assets/Classes/confirm_button.png", "Confirmar",
                                         lambda p, c: self.confirm_selection(), "confirm", (314, 98))

        self.stats = {
            "Lebre": {"Vida": 40, "Ataque": 8, "Movimento": 4, "Alcance": 1},
            "Bufo": {"Vida": 50, "Ataque": 10, "Movimento": 3, "Alcance": 2},
            "Raposa": {"Vida": 60, "Ataque": 12, "Movimento": 2, "Alcance": 3},
            "Salamandra": {"Vida": 30, "Ataque": 10, "Movimento": 5, "Alcance": 5, "Alcance Minimo": 4}
        }
        self.hovered_class = None

    def update_confirm_status(self):
        self.confirm_enabled = (self.selected_p1 is not None) and (self.selected_p2 is not None)

    def handle_class_selection(self, player, class_name):
        if player == "p1":
            self.selected_p1 = class_name
        elif player == "p2":
            self.selected_p2 = class_name
        self.update_confirm_status()

    def confirm_selection(self):
        if self.confirm_enabled:
            self.running = False

    def draw_tooltip(self):
        if self.hovered_class:
            stats = self.stats[self.hovered_class]
            tooltip_width = 170
            if self.stats[self.hovered_class].get("Alcance Minimo"):
                tooltip_width = 230
                tooltip_height = 155
            else:
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

            if self.hovered_class == "Raposa":
                self.screen.blit(tooltip_surface, (x - 200, y))
            else:
                self.screen.blit(tooltip_surface, (x, y))

    def run(self):
        self.bg_y = 0  # initialize bg_y to 0
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill(PRETO)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, self.bg_y))
                self.screen.blit(self.bg_image, (0, self.bg_y + self.bg_image.get_height()))
                self.bg_y -= 0.5 # move the background up
                if self.bg_y < -self.bg_image.get_height():
                    self.bg_y = 0  # reset the background position

            # Update animation offset
            self.animation_offset += self.animation_speed

            # Update button positions with sine wave
            for btn in self.buttons_p1 + self.buttons_p2:
                btn.update_animation(self.animation_offset, self.amplitude)

            image_p1 = pygame.image.load("assets/Starting/jogador1.png")
            self.screen.blit(image_p1, image_p1.get_rect(center=(self.largura//2, 50)))
            image_p2 = pygame.image.load("assets/Starting/jogador2.png")
            self.screen.blit(image_p2, image_p2.get_rect(center=(self.largura//2, 300)))

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif self.secret_counter >= len(SECRET):
                    self.handle_class_selection("p1", "Urso")
                    self.handle_class_selection("p2", "Urso")
                    self.confirm_selection()
                    SOUNDS['djungelskog'].play()
                    time.sleep(2)
                elif event.type == pygame.KEYDOWN:
                    if event.key == SECRET[self.secret_counter]:
                        self.secret_counter += 1
                        SOUNDS['botao'].play()
                    else:
                        self.secret_counter = 0
                for btn in self.buttons_p1 + self.buttons_p2 + [self.confirm_button]:
                    btn.handle_event(event)

            pygame.display.flip()
            clock.tick(60)
