import pygame
import sys
from constants import PRETO, BRANCO, DOURADO, SOUNDS, FONT

class VictoryScreen:
    def __init__(self, screen, font, winner, p1_score, p2_score, final=False):
        # Toca o som de vitória
        SOUNDS['vencer'].play()
        
        # Inicializa os atributos da classe
        self.screen = screen  # Superfície onde o ecrã de vitória será desenhado
        self.font = font  # Fonte usada para renderizar o texto
        self.winner = winner  # Nome do jogador vencedor
        self.p1_score = p1_score  # Pontuação do jogador 1
        self.p2_score = p2_score  # Pontuação do jogador 2
        self.final = final  # Indica se é a vitória final do jogo, ou apenas de uma ronda
        self.largura = screen.get_width()  # Largura do ecrã
        self.altura = screen.get_height()  # Altura do ecrã
        
        try:
            # Carrega e toca a música de vitória apropriada
            if self.final:
                pygame.mixer.music.load("assets/Sounds/victory_sound.wav")
            else:
                pygame.mixer.music.load("assets/Sounds/round_victory.wav")
            pygame.mixer.music.play(-1)  # O -1 faz a música repetir indefinidamente
        except:
            pass  # Ignora erros

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            # Preenche a tela com a cor preta
            self.screen.fill(PRETO)
            
            # Define a fonte e renderiza o texto principal (vitória da rodada ou do jogo)
            text_font = pygame.font.Font(FONT, 50)
            if self.final:
                main_text = text_font.render(f"O JOGADOR {self.winner.upper()} VENCEU O JOGO!", True, DOURADO)
            else:
                main_text = text_font.render(f"O JOGADOR {self.winner.upper()} VENCEU A RONDA!", True, DOURADO)
            
            # Centraliza o texto no ecrã
            text_rect = main_text.get_rect(center=(self.largura//2, self.altura//2 - 50))
            self.screen.blit(main_text, text_rect)
            
            # Renderiza o placar dos jogadores
            score_text = self.font.render(
                f"PLACAR: {self.p1_score} | {self.p2_score}", 
                True, BRANCO
            )
            score_rect = score_text.get_rect(center=(self.largura//2, self.altura//2 + 20))
            self.screen.blit(score_text, score_rect)
            
            # Define a instrução com base no tipo de vitória (final ou ronda)
            if self.final:
                instruction = "Pressione Q para sair"
            else:
                instruction = "Pressione qualquer tecla para a proxima ronda"
            
            # Renderiza a instrução no ecrã
            instr_text = self.font.render(instruction, True, BRANCO)
            instr_rect = instr_text.get_rect(center=(self.largura//2, self.altura//2 + 100))
            self.screen.blit(instr_text, instr_rect)
            
            # Atualiza o ecrã
            pygame.display.flip()
            
            # Verifica os eventos do Pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.final:
                        # Se for a vitória final, pressionar 'Q' sai do jogo
                        if event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                    else:
                        # Se for uma vitória de ronda, pressionar qualquer tecla continua o jogo
                        return 'continue'
            
            # Controla a taxa de atualização do ecrã para 60 FPS
            clock.tick(60)