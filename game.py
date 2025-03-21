import pygame
import random
from SplashScreen import SplashScreen
from ClassSelectionScreen import ClassSelectionScreen
from constants import FONT
from World import World
from VictoryScreen import VictoryScreen
from PowerupSelectionScreen import PowerupSelectionScreen
from constants import POWERUPS, SIZE_X, SIZE_Y, TILE_SIZE, SCALE
import sys

# Classe principal do jogo
class Game:
    # Inicializa a classe
    def __init__(self):
        pygame.init()
        self.screen_width = 960
        self.screen_height = 640
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.key.set_repeat()
        pygame.display.set_caption("Fauna Bellum")
        self.font = pygame.font.Font(FONT, 30)
        self.p1_score = 0
        self.p2_score = 0
        self.p1_powerups = []
        self.p2_powerups = []

    # Executa o jogo
    def run(self):
        while True:
            # Executa a tela de splash
            splash = SplashScreen(self.screen, self.font, self.screen_width, self.screen_height)
            splash.run()
            class_selection = ClassSelectionScreen(self.font)
            class_selection.run()
            
            self.p1_score = 0
            self.p2_score = 0
            self.p1_powerups = []
            self.p2_powerups = []
            # Loop principal do jogo
            while True:
                TILES = (
                    pygame.image.load("assets/Tiles/tile0.png").convert_alpha(),
                    pygame.image.load("assets/Tiles/tile1.png").convert_alpha(),
                    pygame.image.load("assets/Tiles/tile2.png").convert_alpha(),
                    pygame.image.load("assets/Tiles/tile3.png").convert_alpha(),
                    pygame.image.load("assets/Tiles/tile4.png").convert_alpha(),
                    pygame.image.load("assets/Tiles/tile5.png").convert_alpha(),
                    pygame.image.load("assets/Tiles/tile6.png").convert_alpha()
                )
                world = World(SIZE_X, SIZE_Y, TILES, TILE_SIZE, self.screen, SCALE, 
                             class_selection.selected_p1, class_selection.selected_p2, self.font,
                             self.p1_powerups, self.p2_powerups)
                
                winner = world.draw_map()
                
                if winner == "p1":
                    self.p1_score += 1
                    loser = "p2"
                else:
                    self.p2_score += 1
                    loser = "p1"
                
                final_victory = self.p1_score >= 3 or self.p2_score >= 3
                
                victory_screen = VictoryScreen(self.screen, self.font, winner, 
                                              self.p1_score, self.p2_score, final_victory)
                result = victory_screen.run()
                
                if not final_victory:
                    selected = random.sample(POWERUPS, 3)
                    powerup_screen = PowerupSelectionScreen(self.screen, self.font, selected, loser)
                    chosen = powerup_screen.run()
                    if chosen:
                        if loser == "p1":
                            self.p1_powerups.append(chosen)
                        else:
                            self.p2_powerups.append(chosen)
                
                if final_victory:
                    if result == 'restart':
                        break
                    else:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    jogo = Game()
    jogo.run()