import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Definições globais de cores e tamanhos
VERDE = (0, 255, 0)
AZUL = (0, 0, 255, 50)
CINZENTO = (128, 128, 128)
DOURADO = (218, 165, 32)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0, 50)
TILE_SIZE = 32
SIZE_X = 7
SIZE_Y = 7
SCALE = 2
FONT = "assets/Font/Pixeboy.ttf"
FONT2 = "assets/Font/BaiJamjuree-Bold.ttf"

# Código do Easter Egg
SECRET = (pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN, pygame.K_LEFT,
          pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_b, pygame.K_a, pygame.K_RETURN)

# PowerUps das Personagens
POWERUPS = [
    {'type': 'health', 'name': ' Queijada Especial', 'description': '+20 Vida Maxima', 'value': 20, 'image': 'assets/Powerups/Queijada.png'},
    {'type': 'attack', 'name': 'Travesseiro Magico', 'description': '+3 Ataque', 'value': 3, 'image': 'assets/Powerups/Travesseiro.png'},
    {'type': 'move_range', 'name': 'Faca da Chinada', 'description': '+1 Movimento', 'value': 1, 'image': 'assets/Powerups/Faca.png'},
    {'type': 'attack_range', 'name': 'Pedra da Calcada', 'description': '+1 Alcance de Ataque', 'value': 1, 'image': 'assets/Powerups/Pedra.png'},
    {'type': 'regeneration', 'name': 'Betty', 'description': 'Cura 5 de vida por turno', 'value': 5, 'image': 'assets/Powerups/Betty.png'},
    {'type': 'armor', 'name': 'Armadura de Mouro', 'description': '+40 Vida Maxima, -1 Movimento', 'value': {'health': 40, 'move_range': -1}, 'image': 'assets/Powerups/armor.png'},
    {'type': 'lifesteal', 'name': 'Bruxaria Lunar', 'description': 'Recupera 20% do dano causado em vida', 'value': 0.2, 'image': 'assets/Powerups/Vampire.png'}
]

pygame.mixer.init()
# Identificadores dos Sons
SOUNDS = {'vencer': pygame.mixer.Sound('assets/Sounds/vencer.wav'),
           'morrer': pygame.mixer.Sound('assets/Sounds/morrer.wav'),
           'botao': pygame.mixer.Sound('assets/Sounds/clicar_botao.wav'),
           'powerup': pygame.mixer.Sound('assets/Sounds/escolher_powerup.wav'),
           'Bufo': pygame.mixer.Sound('assets/Sounds/Bufo_ataque.wav'),
           'Raposa': pygame.mixer.Sound('assets/Sounds/raposa_ataque.wav'),
           'Lebre': pygame.mixer.Sound('assets/Sounds/lebre_ataque.wav'),
           'Urso': pygame.mixer.Sound('assets/Sounds/urso_ataque.wav'),
           'Arqueiro': pygame.mixer.Sound('assets/Sounds/arqueiro_ataque.wav'),
           'escolher': pygame.mixer.Sound('assets/Sounds/escolha_personagem.wav'),
           'djungelskog': pygame.mixer.Sound('assets/Sounds/Djungelskog.wav'),
           'menu': pygame.mixer.Sound('assets/Sounds/song_mainmenu.wav'),
           'batalha': pygame.mixer.Sound('assets/Sounds/song_batalha.wav'),
           'vida': pygame.mixer.Sound('assets/Sounds/vida.wav')}
