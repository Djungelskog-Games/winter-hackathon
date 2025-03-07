import pygame
from constants import DOURADO
from constants import VERDE

# Classe que representa um botão com um ícone   
class BotaoIcone:
    # Inicializa o botão com a posição, imagem, nome da classe, callback, jogador e tamanho
    def __init__(self, x, y, image_path, class_name, callback, player, size=(150, 150)):
        # Carrega a imagem e redimensiona
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
        # Caso a imagem não seja encontrada, cria um retângulo preenchido de dourado
        except pygame.error:
            self.image = pygame.Surface((150, 150))
            self.image.fill(DOURADO)
        # Define a posição do botão
        self.rect = self.image.get_rect(center=(x, y))
        # Define os atributos da classe
        self.class_name = class_name
        self.callback = callback
        self.player = player
        self.selected = False

    # Desenha o botão na tela
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            pygame.draw.rect(surface, VERDE, self.rect.inflate(10, 10), 5)
    # Verifica se o botão foi clicado
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback(self.player, self.class_name)