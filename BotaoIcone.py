import pygame
import math
from constants import VERMELHO, AZUL

class BotaoIcone:
    def __init__(self, x, y, image_path, class_name, callback, player, size=(125, 125)):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(self.image, size)
        self.base_x = x  # Store original x
        self.base_y = y  # Store original y
        self.rect = self.image.get_rect(center=(x, y))
        self.class_name = class_name
        self.callback = callback
        self.player = player
        self.selected = False
        self.phase = 0  # Phase offset for animation

    def update_animation(self, animation_offset, amplitude):
        """Update position based on sine wave"""
        dy = amplitude * math.sin(animation_offset + self.phase)
        self.rect.center = (self.base_x, self.base_y + dy)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self.player, self.class_name)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.selected:
            if self.player == "p1":
                pygame.draw.rect(screen, VERMELHO, self.rect, 5)
            if self.player == "p2":
                pygame.draw.rect(screen, AZUL, self.rect, 5)