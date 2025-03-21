import pygame
import sys
import random
import time
import math
from constants import TILE_SIZE, SCALE, PRETO, DOURADO, BRANCO, VERMELHO, FONT, FONT2, SOUNDS, VERDE, AZUL
from Player import Player, attack

VERDE = (0, 255, 0)

class World:
    def __init__(self, x, y, tilepack, tilesize, display, scale, player1_class, player2_class, font, p1_powerups=None, p2_powerups=None):
        # Toca o som de botão ao iniciar
        SOUNDS['botao'].play()
        time.sleep(0.3)

        # Inicializa os atributos da classe
        self.x = x  # Largura do mapa em tiles
        self.y = y  # Altura do mapa em tiles
        self.tilesize = tilesize  # Tamanho de cada tile
        self.display = display  # Superfície onde o ecrã será desenhado
        self.scale = scale  # Escala dos tiles
        self.mapa = []  # Lista para armazenar o mapa de tiles
        self.coor_pedras = []  # Lista para armazenar as coordenadas das pedras
        self.pedras_usadas = []  # Lista para armazenar as imagens das pedras
        self.screen_width = display.get_width()  # Largura do ecrã
        self.screen_height = display.get_height()  # Altura do ecrã
        self.key = None  # Tecla pressionada
        self.pedras = (
            pygame.image.load("assets/Tiles/Pedra1.png").convert_alpha(),
            pygame.image.load("assets/Tiles/Pedra2.png").convert_alpha(),
            pygame.image.load("assets/Tiles/Pedra3.png").convert_alpha(),
            pygame.image.load("assets/Tiles/Pedra4.png").convert_alpha()
        )  # Carrega as imagens das pedras

        try:
            # Tenta carregar a imagem de fundo
            self.bg_image = pygame.image.load("assets/World/Background.jpg").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, self.display.get_size())
        except pygame.error:
            self.bg_image = None  # Caso a imagem não seja encontrada

        # Gera pedras aleatórias no mapa
        for i in range(random.randint(5, 9)):
            pedra_x = random.randint(1, 5)
            pedra_y = random.randint(1, 5)
            pedra_escolhida = random.choice(self.pedras)
            self.coor_pedras.append((pedra_x, pedra_y))
            self.pedras_usadas.append(pedra_escolhida)

        # Gera o mapa com tiles aleatórios
        for i in range(y):
            linha = []
            for j in range(x):
                tile = random.choice(tilepack)
                tile = pygame.transform.scale_by(tile, scale)
                linha.append(tile)
            self.mapa.append(linha)

        # Dicionário com as imagens dos jogadores
        self.player_images = {
            "Lebre": "assets/Classes/Lebre.png",
            "Bufo": "assets/Classes/Bufo.png",
            "Raposa": "assets/Classes/Raposa.png",
            "Urso": "assets/Classes/Urso.png",
            "Salamandra": "assets/Classes/Salamandra.png"
        }

        # Define as posições iniciais dos jogadores
        pos1 = (0, 0)
        pos2 = (self.x - 1, self.y - 1)

        # Inicializa os jogadores
        self.player1 = Player(self.player_images.get(player1_class),
                             pos1, speed=0.3, scale=self.scale,
                             class_name=player1_class, font=font, powerups=p1_powerups)
        self.player2 = Player(self.player_images.get(player2_class),
                             pos2, speed=0.3, scale=self.scale,
                             class_name=player2_class, font=font, powerups=p2_powerups)

        # Define o turno inicial e os movimentos restantes
        self.current_turn = "p1"
        self.player1.moves_remaining = self.player1.move_range
        self.player2.moves_remaining = self.player2.move_range

        # Carrega e toca a música de batalha em loop
        SOUNDS['batalha'].play(-1)

    def draw_attack_range(self, offset_x, offset_y):
        # Cria uma superfície para desenhar o alcance de ataque
        overlay = pygame.Surface((self.x * TILE_SIZE * SCALE, self.y * TILE_SIZE * SCALE), pygame.SRCALPHA)

        # Obtém o jogador atual e seu alcance de ataque
        current_player = self.player1 if self.current_turn == "p1" else self.player2
        attack_range = current_player.attack_range
        px, py = current_player.grid_x, current_player.grid_y

        # Define a cor para o alcance de ataque, dependendo do jogador atual
        attack_color = VERMELHO if self.current_turn == "p1" else AZUL

        # Desenha o alcance de ataque
        for dx in range(-attack_range, attack_range + 1):
            for dy in range(-attack_range, attack_range + 1):
                if (dx == 0 and abs(dy) <= attack_range) or (dy == 0 and abs(dx) <= attack_range):
                    x = px + dx
                    y = py + dy
                    if 0 <= x < self.x and 0 <= y < self.y:
                        path_clear = True
                        # Verifica se o caminho está livre (sem pedras)
                        if dx == 0:
                            for intermediate_y in range(min(py, y), max(py, y) + 1):
                                if (px, intermediate_y) in self.coor_pedras:
                                    path_clear = False
                                    break
                        elif dy == 0:
                            for intermediate_x in range(min(px, x), max(px, x) + 1):
                                if (intermediate_x, py) in self.coor_pedras:
                                    path_clear = False
                                    break

                        # Se a classe escolhida for o Salamandra, este não desenha o alcance de ataque nos 4 blocos mais perto
                        if current_player.class_name == "Salamandra" and abs(dx) + abs(dy) <= 3:
                            continue

                        if path_clear:
                            pos_x = x * TILE_SIZE * SCALE
                            pos_y = y * TILE_SIZE * SCALE
                            pygame.draw.rect(overlay, attack_color, (pos_x, pos_y, TILE_SIZE * SCALE, TILE_SIZE * SCALE))

        # Desenha a superfície no ecrã
        self.display.blit(overlay, (offset_x, offset_y))

    def draw_player_stats(self, display, offset_x, offset_y, player, side):
        # Configurações do painel de stats
        panel_width = 200
        panel_height = 250
        spacing = 20

        # Define a posição do painel (esquerda ou direita)
        if side == "left":
            panel_x = offset_x - panel_width - spacing
        else:
            panel_x = offset_x + (self.x * self.tilesize * self.scale) + spacing

        panel_y = offset_y + 50

        # Desenha o fundo do painel
        pygame.draw.rect(display, DOURADO, (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(display, PRETO, (panel_x+2, panel_y+2, panel_width-4, panel_height-4), border_radius=8)

        # Desenha o sprite do jogador
        sprite = pygame.transform.smoothscale(player.stats_image, (100, 100))
        display.blit(sprite, (panel_x + (panel_width-100)//2, panel_y + 10))

        # Configurações da fonte para os stats
        stats_font = pygame.font.Font(FONT, 24)
        y_offset = 120

        # Desenha o ataque
        attack_text = stats_font.render(f"Ataque: {player.attack_damage}", True, BRANCO)
        display.blit(attack_text, (panel_x + 20, panel_y + y_offset))
        y_offset += 30

        # Desenha o movimento
        move_text = stats_font.render(f"Movimento: {player.move_range}", True, BRANCO)
        display.blit(move_text, (panel_x + 20, panel_y + y_offset))
        y_offset += 30

        if player.class_name == "Salamandra":    # Desenha o alcance
            range_text = stats_font.render(f"Alcance: {player.min_attack_range} - {player.attack_range}", True, BRANCO)
            display.blit(range_text, (panel_x + 20, panel_y + y_offset))
            y_offset += 30
        else:
            range_text = stats_font.render(f"Alcance: {player.attack_range}", True, BRANCO)
            display.blit(range_text, (panel_x + 20, panel_y + y_offset))
            y_offset += 30

        # Desenha a barra de vida
        health_width = 160
        health_height = 20
        health_x = panel_x + (panel_width - health_width)//2
        health_y = panel_y + y_offset

        # Fundo da barra de vida
        pygame.draw.rect(display, VERMELHO, (health_x, health_y, health_width, health_height))
        # Vida atual
        fill_width = (player.health / player.max_health) * health_width
        pygame.draw.rect(display, VERDE, (health_x, health_y, fill_width, health_height))

        # Texto da vida
        health_text = stats_font.render(f"{player.health}/{player.max_health}", True, BRANCO)
        text_rect = health_text.get_rect(center=(health_x + health_width//2, health_y + health_height//2))
        display.blit(health_text, text_rect)

    def draw_map(self):
        winner = None
        running = True
        angulo = 0
        clock = pygame.time.Clock()

        # Controls dos jogadores
        player1_controls = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0), pygame.K_s: (0, 1), pygame.K_d: (1, 0)}
        player2_controls = {pygame.K_UP: (0, -1), pygame.K_LEFT: (-1, 0), pygame.K_DOWN: (0, 1), pygame.K_RIGHT: (1, 0)}

        # Configurações da fonte
        font = pygame.font.Font(FONT, 40)
        font2 = pygame.font.Font(FONT2, 30)
        controls_font = pygame.font.Font(FONT, 28)

        while running:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Finaliza o turno do jogador atual
                        if self.current_turn == "p1":
                            self.player1.moves_remaining = 0
                        else:
                            self.player2.moves_remaining = 0
                    elif event.key == pygame.K_SPACE:
                        # Realiza um ataque
                        if self.current_turn == "p1":
                            if self.player1.stamina:
                                attack(self.player1, self.player2, self.coor_pedras)
                                self.player1.stamina = False
                        else:
                            if self.player2.stamina:
                                attack(self.player2, self.player1, self.coor_pedras)
                                self.player2.stamina = False
                    else:
                        # Armazena a tecla pressionada
                        self.key = event.key
                        SOUNDS['botao'].play()

            # Processa o movimento do jogador atual
            if self.current_turn == "p1":
                other_pos = (self.player2.grid_x, self.player2.grid_y)
                self.player1.handle_input(self.key, player1_controls, self.x, self.y, other_pos, self.coor_pedras)
            else:
                other_pos = (self.player1.grid_x, self.player1.grid_y)
                self.player2.handle_input(self.key, player2_controls, self.x, self.y, other_pos, self.coor_pedras)

            # Atualiza os jogadores
            self.player1.update(dt)
            self.player2.update(dt)

            self.key = None

            # Verifica se o turno acabou
            if self.current_turn == "p1" and not self.player1.moving:
                if self.player1.moves_remaining == 0:
                    # Regenera a vida do jogador 1 e passa o turno para o jogador 2
                    self.player1.health = min(self.player1.health + self.player1.regeneration, self.player1.max_health)
                    if self.player1.regeneration > 0 and self.player1.health < self.player1.max_health:
                        SOUNDS['vida'].play()
                        self.player1.regeneration_display_time = 2000
                    self.current_turn = "p2"
                    self.player2.moves_remaining = self.player2.move_range
            elif self.current_turn == "p2" and not self.player2.moving:
                if self.player2.moves_remaining == 0:
                    # Regenera a vida do jogador 2 e passa o turno para o jogador 1
                    self.player2.health = min(self.player2.health + self.player2.regeneration, self.player2.max_health)
                    if self.player2.regeneration > 0 and self.player2.health < self.player2.max_health:
                        SOUNDS['vida'].play()
                        self.player2.regeneration_display_time = 2000
                    self.current_turn = "p1"
                    self.player1.moves_remaining = self.player1.move_range

            # Verifica se algum jogador morreu
            if self.player1.health <= 0:
                SOUNDS['batalha'].stop()
                SOUNDS['morrer'].play()
                self.draw_player_stats(self.display, offset_x, offset_y, self.player1, "left")
                self.draw_player_stats(self.display, offset_x, offset_y, self.player2, "right")
                pygame.display.flip()
                time.sleep(0.7)
                winner = "p2"
                running = False
            elif self.player2.health <= 0:
                SOUNDS['batalha'].stop()
                SOUNDS['morrer'].play()
                self.draw_player_stats(self.display, offset_x, offset_y, self.player1, "left")
                self.draw_player_stats(self.display, offset_x, offset_y, self.player2, "right")
                pygame.display.flip()
                time.sleep(0.7)
                winner = "p1"
                running = False

            # Desenha o fundo
            if self.bg_image:
                self.display.blit(self.bg_image, (0, 0))
            else:
                self.display.fill(PRETO)

            # Calcula o offset para centralizar o mapa no ecrã
            display_width, display_height = self.display.get_size()
            map_width = self.x * self.tilesize * self.scale
            map_height = self.y * self.tilesize * self.scale
            offset_x = (display_width - map_width) // 2
            offset_y = (display_height - map_height) // 2

            # Desenha o mapa
            i = 0
            for y_idx, row in enumerate(self.mapa):
                for x_idx, tile in enumerate(row):
                    pos_x_tile = offset_x + x_idx * self.tilesize * self.scale
                    pos_y_tile = offset_y + y_idx * self.tilesize * self.scale
                    self.display.blit(tile, (pos_x_tile, pos_y_tile))

                    # Desenha as pedras
                    if (x_idx, y_idx) in self.coor_pedras:
                        stone_img = pygame.transform.scale(self.pedras_usadas[i], (TILE_SIZE * self.scale, TILE_SIZE * self.scale))
                        self.display.blit(stone_img, (pos_x_tile, pos_y_tile))
                        i += 1

            # Desenha o alcance de ataque
            self.draw_attack_range(offset_x, offset_y)

            # Desenha os stats dos jogadores
            self.draw_player_stats(self.display, offset_x, offset_y, self.player1, "left")
            self.draw_player_stats(self.display, offset_x, offset_y, self.player2, "right")

            # Desenha os jogadores
            self.player1.draw(self.display, offset_x, offset_y)
            self.player2.draw(self.display, offset_x, offset_y)

            # Desenha a imagem do turno atual
            amplitude = 5  # Altura do movimento em pixels
            velocidade = 0.025  # Velocidade da animação
            turn_image = pygame.image.load("assets/Starting/turnodojogadorp1.png" if self.current_turn == "p1" else "assets/Starting/turnodojogadorp2.png")
            image_rect = turn_image.get_rect(center=(self.screen_width // 2, 50 + math.sin(angulo) * amplitude))
            self.display.blit(turn_image, image_rect)

            angulo += velocidade

            # Desenha os controls na parte inferior do ecrã
            controls_y = self.screen_height - 80
            controls = [
                "WASD - Movimentar Jogador 1                            SETAS - Movimentar Jogador 2",
                "SPACE - Atacar                                 ENTER - Finalizar Turno",
                ""
                "Nota: Apenas e possivel atacar uma vez por movimento."
            ]

            for i, text in enumerate(controls):
                control_text = controls_font.render(text, True, DOURADO)
                text_rect = control_text.get_rect(center=(self.screen_width//2, controls_y + i*30))
                self.display.blit(control_text, text_rect)

            # Atualiza o ecrã
            pygame.display.flip()

        # Para a música de batalha
        pygame.mixer.music.stop()
        return winner
