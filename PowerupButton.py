import pygame
from constants import SOUNDS, FONT, DOURADO, PRETO, BRANCO

class PowerupButton:
    def __init__(self, x, y, width, height, powerup, callback):
        SOUNDS['powerup'].play()
        self.rect = pygame.Rect(x, y, width, height)
        self.powerup = powerup
        self.callback = callback
        self.font = pygame.font.Font(FONT, 24)
        
        # Carrega e redimensiona a imagem
        self.image = pygame.image.load(powerup['image']).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))  # Ajuste o tamanho conforme necessário

    def draw(self, screen):
        pygame.draw.rect(screen, DOURADO, self.rect, border_radius=10)
        pygame.draw.rect(screen, PRETO, self.rect.inflate(-4, -4), border_radius=8)
        
        # Desenha a imagem
        img_rect = self.image.get_rect(center=(self.rect.centerx, self.rect.top + 40))
        screen.blit(self.image, img_rect)
        
        # Ajusta posição do título para abaixo da imagem
        title = self.font.render(self.powerup['name'], True, BRANCO)
        title_rect = title.get_rect(center=(self.rect.centerx, img_rect.bottom + 10))
        screen.blit(title, title_rect)
        
        # Descrição mantida no centro
        desc = self.font.render(self.powerup['description'], True, BRANCO)
        desc_rect = desc.get_rect(center=(self.rect.centerx, self.rect.centery + 50))
        screen.blit(desc, desc_rect)

    def on_click(self):
        self.callback(self.powerup)