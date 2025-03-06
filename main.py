import pygame
import sys
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Definições globais de cores e tamanhos
VERDE = (0, 255, 0)
CINZENTO = (128, 128, 128)
DOURADO = (218, 165, 32)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
TILE_SIZE = 32
SIZE_X = 7
SIZE_Y = 7
SCALE = 2

# -------------------- Classes de Interface --------------------
class BotaoIcone:
    def __init__(self, x, y, image_path, class_name, callback, player, size = (150, 150)):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, size)
        except pygame.error:
            self.image = pygame.Surface((150, 150))
            self.image.fill(DOURADO)
        self.rect = self.image.get_rect(center=(x, y))
        self.class_name = class_name
        self.callback = callback
        self.player = player
        self.selected = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.selected:
            pygame.draw.rect(surface, VERDE, self.rect.inflate(10, 10), 5)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback(self.player, self.class_name)

class SplashScreen:
    def __init__(self, screen, font, largura, altura):
        self.screen = screen
        self.font = font
        self.largura = largura
        self.altura = altura
        pygame.mixer.music.load("assets/Sounds/song_mainmenu.wav")
        pygame.mixer.music.play(-1)

    def run(self):
        try:
            splash_image = pygame.image.load("assets/Starting/Starting_Screen.png").convert()
            original_size = splash_image.get_size()
            new_size = (int(original_size[0] * 0.8), int(original_size[1] * 0.8))
            splash_image = pygame.transform.scale(splash_image, new_size)
            image_rect = splash_image.get_rect(center=(self.largura // 2, self.altura // 2))
        except pygame.error:
            splash_image = pygame.Surface((self.largura, self.altura))
            splash_image.fill(PRETO)
            error_text = self.font.render("Imagem não encontrada!", True, BRANCO)
            splash_image.blit(error_text, (self.largura//2 - 100, self.altura//2))
            image_rect = splash_image.get_rect(topleft=(0, 0))
        
        try:
            overlay_image = pygame.image.load("assets/Starting/Starting_Text.png").convert_alpha()
            overlay_rect = overlay_image.get_rect(center=(self.largura // 2, 150))
        except pygame.error:
            overlay_image = pygame.Surface((600, 100), pygame.SRCALPHA)
            overlay_image.fill((0, 0, 0, 180))
            overlay_rect = overlay_image.get_rect(center=(self.largura // 2, 150))
        
        try:
            overlay_image2 = pygame.image.load("assets/Starting/Starting_Subtext.png").convert_alpha()
            overlay_rect2 = overlay_image2.get_rect(center=(self.largura // 2, 250))
        except pygame.error:
            overlay_image2 = pygame.Surface((600, 100), pygame.SRCALPHA)
            overlay_image2.fill((0, 0, 0, 180))
            overlay_rect2 = overlay_image2.get_rect(center=(self.largura // 2, 250))

        self.screen.blit(splash_image, image_rect)
        self.screen.blit(overlay_image, overlay_rect)
        self.screen.blit(overlay_image2, overlay_rect2)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return

class ClassSelectionScreen:
    def __init__(self, font):
        self.largura = 800
        self.altura = 700
        self.font = font
        self.selected_p1 = None
        self.selected_p2 = None
        self.confirm_enabled = False

        self.screen = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("")

        try:
            self.bg_image = pygame.image.load("assets/Classes/Background.jpg").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.largura, self.altura))
        except pygame.error:
            self.bg_image = None

        self.icon_spacing = 250
        self.base_x = self.largura // 2
        self.player1_y = 200
        self.player2_y = 450

        self.buttons_p1 = [
            BotaoIcone(self.base_x - self.icon_spacing, self.player1_y, 
                       "assets/Classes/lebre_icon.png", "Lebre", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x, self.player1_y, 
                       "assets/Classes/raposa_icon.png", "Raposa", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player1_y, 
                       "assets/Classes/veado_icon.png", "Veado", self.handle_class_selection, "p1")
        ]
        self.buttons_p2 = [
            BotaoIcone(self.base_x - self.icon_spacing, self.player2_y, 
                       "assets/Classes/lebre_icon.png", "Lebre", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x, self.player2_y, 
                       "assets/Classes/raposa_icon.png", "Raposa", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player2_y, 
                       "assets/Classes/veado_icon.png", "Veado", self.handle_class_selection, "p2")
        ]
        self.confirm_button = BotaoIcone(self.largura//2, self.altura - 100, 
                                         "assets/Classes/confirm_button.png", "Confirmar", 
                                         lambda p, c: self.confirm_selection(), "confirm", (700, 90))

        # Stats para tooltip
        self.stats = {
            "Lebre": {"Vida": 80, "Ataque": 8, "Movimento": 4},
            "Raposa": {"Vida": 100, "Ataque": 10, "Movimento": 3},
            "Veado": {"Vida": 120, "Ataque": 12, "Movimento": 2}
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
            tooltip_width = 200
            tooltip_height = 110
            x, y = pygame.mouse.get_pos()
            x += 20
            y += 20
            
            # Fundo do tooltip
            tooltip_surface = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
            tooltip_surface.fill((0, 0, 0, 150))
            
            # Texto
            title = self.font.render(self.hovered_class, True, BRANCO)
            tooltip_surface.blit(title, (10, 5))
            
            y_offset = 30
            for key, value in stats.items():
                text = self.font.render(f"{key}: {value}", True, BRANCO)
                tooltip_surface.blit(text, (10, y_offset))
                y_offset += 25
            
            self.screen.blit(tooltip_surface, (x, y))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill(PRETO)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            text_p1 = self.font.render("Player 1", True, BRANCO)
            self.screen.blit(text_p1, text_p1.get_rect(center=(self.largura//2, 75)))
            text_p2 = self.font.render("Player 2", True, BRANCO)
            self.screen.blit(text_p2, text_p2.get_rect(center=(self.largura//2, 325)))
            
            # Verificar hover
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
                for btn in self.buttons_p1 + self.buttons_p2 + [self.confirm_button]:
                    btn.handle_event(event)
                if event.type == pygame.MOUSEMOTION:
                    pass  # Atualizado no loop principal
                    
            pygame.display.flip()
            clock.tick(60)

# -------------------- Classes de Jogo --------------------
class Player:
    def __init__(self, image_path, start_grid_pos, speed, scale=1, class_name="Lebre", font=None):
        try:
            full_image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            full_image = pygame.Surface((TILE_SIZE * scale, TILE_SIZE * scale))
            full_image.fill(VERDE)
        self.sprite_scale_factor = scale * 0.45
        sprite_size = int(TILE_SIZE * scale * self.sprite_scale_factor)
        self.image = pygame.transform.scale(full_image, (sprite_size, sprite_size))
        self.sprite_width = sprite_size
        self.sprite_height = sprite_size

        self.grid_x, self.grid_y = start_grid_pos
        self.pixel_x = self.grid_x * TILE_SIZE * scale
        self.pixel_y = self.grid_y * TILE_SIZE * scale
        self.dest_grid_x = self.grid_x
        self.dest_grid_y = self.grid_y
        self.moving = False
        self.speed = speed  # velocidade em pixels por ms

        # Configurações baseadas na classe
        health_dict = {"Lebre": 80, "Raposa": 100, "Veado": 120}
        attack_dict = {"Lebre": 8, "Raposa": 10, "Veado": 12}
        move_range_dict = {"Lebre": 3, "Raposa": 2, "Veado": 1}
        
        self.health = health_dict.get(class_name, 1000)
        self.attack_damage = attack_dict.get(class_name, 50)
        self.move_range = move_range_dict.get(class_name, 1)
        self.moves_remaining = self.move_range
        self.class_name = class_name

        # Sistema de dano
        self.font = font if font else pygame.font.Font(None, 24)
        self.last_damage = 0
        self.damage_display_time = 0

    def handle_input(self, key, controls, grid_width, grid_height, other_player_pos):
        if not self.moving and self.moves_remaining > 0:
            if key in controls:
                new_grid_x = self.grid_x + controls.get(key)[0]
                new_grid_y = self.grid_y + controls.get(key)[1]
                if (0 <= new_grid_x < grid_width and 0 <= new_grid_y < grid_height
                    and (new_grid_x, new_grid_y) != other_player_pos):
                    self.dest_grid_x = new_grid_x
                    self.dest_grid_y = new_grid_y
                    self.moving = True
                return

    def update(self, dt):
        if self.moving:
            target_x = self.dest_grid_x * TILE_SIZE * SCALE
            target_y = self.dest_grid_y * TILE_SIZE * SCALE
            diff_x = target_x - self.pixel_x
            diff_y = target_y - self.pixel_y
            move_x = self.speed * dt if diff_x > 0 else -self.speed * dt if diff_x < 0 else 0
            move_y = self.speed * dt if diff_y > 0 else -self.speed * dt if diff_y < 0 else 0
            if abs(diff_x) <= abs(move_x):
                self.pixel_x = target_x
            else:
                self.pixel_x += move_x
            if abs(diff_y) <= abs(move_y):
                self.pixel_y = target_y
            else:
                self.pixel_y += move_y
            if self.pixel_x == target_x and self.pixel_y == target_y:
                self.grid_x = self.dest_grid_x
                self.grid_y = self.dest_grid_y
                self.moving = False
                if self.moves_remaining > 0:
                    self.moves_remaining -= 1
        
        # Atualizar tempo de exibição de dano
        if self.damage_display_time > 0:
            self.damage_display_time = max(0, self.damage_display_time - dt)

    def draw(self, display, offset_x, offset_y):
        tile_pixel_size = TILE_SIZE * SCALE
        tile_top_left_x = offset_x + self.pixel_x
        tile_top_left_y = offset_y + self.pixel_y
        tile_center_x = tile_top_left_x + tile_pixel_size / 2
        tile_center_y = tile_top_left_y + tile_pixel_size / 2
        sprite_draw_x = tile_center_x - self.sprite_width / 2
        sprite_draw_y = tile_center_y - self.sprite_height / 2
        display.blit(self.image, (sprite_draw_x, sprite_draw_y))
        
        # Exibir dano
        if self.damage_display_time > 0:
            damage_text = self.font.render(f"-{self.last_damage}", True, (255, 0, 0))
            text_rect = damage_text.get_rect(center=(tile_center_x, sprite_draw_y - 20))
            display.blit(damage_text, text_rect)
        
        self.draw_health_bar(display, tile_center_x, sprite_draw_y + self.sprite_height)

    def draw_health_bar(self, display, center_x, sprite_bottom_y):
        bar_width = 50
        bar_height = 5
        margin = 5
        fill = (self.health / 100) * bar_width
        x = center_x - bar_width / 2
        y = sprite_bottom_y + margin
        pygame.draw.rect(display, CINZENTO, (x, y, bar_width, bar_height))
        pygame.draw.rect(display, VERDE, (x, y, fill, bar_height))

def attack(attacker, defender, reach=1):
    if abs(attacker.grid_x - defender.grid_x) <= reach and abs(attacker.grid_y - defender.grid_y) <= reach:
        damage = attacker.attack_damage
        defender.health -= damage
        defender.last_damage = damage
        defender.damage_display_time = 2000  # 2 segundos
        
        if defender.health < 0:
            defender.health = 0

        # Knockback
        delta_x = defender.grid_x - attacker.grid_x
        delta_y = defender.grid_y - attacker.grid_y

        knockback_x = 0
        knockback_y = 0
        if delta_x != 0:
            knockback_x = 1 if delta_x > 0 else -1
        if delta_y != 0:
            knockback_y = 1 if delta_y > 0 else -1

        new_x = defender.grid_x + knockback_x
        new_y = defender.grid_y + knockback_y

        if 0 <= new_x < SIZE_X and 0 <= new_y < SIZE_Y:
            if (new_x, new_y) != (attacker.grid_x, attacker.grid_y):
                defender.grid_x = new_x
                defender.grid_y = new_y
                defender.dest_grid_x = new_x
                defender.dest_grid_y = new_y
                defender.pixel_x = new_x * TILE_SIZE * SCALE
                defender.pixel_y = new_y * TILE_SIZE * SCALE
                defender.moving = False

class World:
    def __init__(self, x, y, tilepack, tilesize, display, scale, player1_class, player2_class, font):
        self.x = x
        self.y = y
        self.tilesize = tilesize
        self.display = display
        self.scale = scale
        self.mapa = []
        self.screen_width = display.get_width()
        self.screen_height = display.get_height()
        self.key = None
        try:
            self.bg_image = pygame.image.load("assets/World/Background.jpg").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, self.display.get_size())
        except pygame.error:
            self.bg_image = None
        for i in range(y):
            linha = []
            for j in range(x):
                tile = random.choice(tilepack)
                tile = pygame.transform.scale_by(tile, scale)
                linha.append(tile)
            self.mapa.append(linha)
        
        self.player_images = {
            "Lebre": "assets/Classes/lebre_icon.png",
            "Raposa": "assets/Classes/raposa_icon.png",
            "Veado": "assets/Classes/veado_icon.png"
        }
        pos1 = (0, 0)
        pos2 = (self.x - 1, self.y - 1)
        self.player1 = Player(self.player_images.get(player1_class, "assets/Classes/lebre_icon.png"), 
                             pos1, speed=0.5, scale= self.scale, 
                             class_name=player1_class, font=font)
        self.player2 = Player(self.player_images.get(player2_class, "assets/Classes/lebre_icon.png"), 
                             pos2, speed=0.5, scale= self.scale, 
                             class_name=player2_class, font=font)
        self.current_turn = "p1"
        self.player1.moves_remaining = self.player1.move_range
        self.player2.moves_remaining = self.player2.move_range
        
        # Efeitos sonoros
        try:
            self.attack_sound = pygame.mixer.Sound("assets/Sounds/attack.wav")
        except:
            self.attack_sound = None
        
        pygame.mixer.music.load("assets/Sounds/song_batalha.wav")
        pygame.mixer.music.play(-1)

    def draw_map(self):
        winner = None
        running = True
        clock = pygame.time.Clock()
        player1_controls = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0), pygame.K_s: (0, 1), pygame.K_d: (1, 0)}
        player2_controls = {pygame.K_UP: (0, -1), pygame.K_LEFT: (-1, 0), pygame.K_DOWN: (0, 1), pygame.K_RIGHT: (1, 0)}
        font = pygame.font.Font(None, 36)
        controls_font = pygame.font.Font(None, 24)

        while running:
            dt = clock.tick(60)  # dt em ms
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.current_turn == "p1":
                            self.player1.moves_remaining = 0
                        else:
                            self.player2.moves_remaining = 0
                    elif event.key == pygame.K_SPACE:
                        if self.current_turn == "p1":
                            attack(self.player1, self.player2)
                        else:
                            attack(self.player2, self.player1)
                        if self.attack_sound:
                            self.attack_sound.play()
                    elif event.type == pygame.KEYDOWN:
                        self.key = event.key
                    else:
                        self.key = None

            if self.current_turn == "p1":
                other_pos = (self.player2.grid_x, self.player2.grid_y)
                self.player1.handle_input(self.key, player1_controls, self.x, self.y, other_pos)
            else:
                other_pos = (self.player1.grid_x, self.player1.grid_y)
                self.player2.handle_input(self.key, player2_controls, self.x, self.y, other_pos)

            self.player1.update(dt)
            self.player2.update(dt)

            self.key = None

            if self.current_turn == "p1" and not self.player1.moving:
                if self.player1.moves_remaining == 0:
                    self.current_turn = "p2"
                    self.player2.moves_remaining = self.player2.move_range
            elif self.current_turn == "p2" and not self.player2.moving:
                if self.player2.moves_remaining == 0:
                    self.current_turn = "p1"
                    self.player1.moves_remaining = self.player1.move_range

            # Verificar vitória
            if self.player1.health <= 0:
                winner = "p2"
                running = False
            elif self.player2.health <= 0:
                winner = "p1"
                running = False

            if self.bg_image:
                self.display.blit(self.bg_image, (0, 0))
            else:
                self.display.fill(PRETO)

            display_width, display_height = self.display.get_size()
            map_width = self.x * self.tilesize * self.scale
            map_height = self.y * self.tilesize * self.scale
            offset_x = (display_width - map_width) // 2
            offset_y = (display_height - map_height) // 2

            for y_idx, row in enumerate(self.mapa):
                for x_idx, tile in enumerate(row):
                    pos_x_tile = offset_x + x_idx * self.tilesize * self.scale
                    pos_y_tile = offset_y + y_idx * self.tilesize * self.scale
                    self.display.blit(tile, (pos_x_tile, pos_y_tile))

            self.player1.draw(self.display, offset_x, offset_y)
            self.player2.draw(self.display, offset_x, offset_y)

            turn_text = font.render(f"Turn: {self.current_turn}", True, BRANCO)
            self.display.blit(turn_text, (10, 10))

            # Legenda de controles
            space_text = controls_font.render("Espaço para atacar", True, BRANCO)
            enter_text = controls_font.render("Enter para passar turno", True, BRANCO)
            self.display.blit(space_text, (10, self.screen_height - 60))
            self.display.blit(enter_text, (10, self.screen_height - 30))

            pygame.display.flip()
        
        pygame.mixer.music.stop()
        return winner

class VictoryScreen:
    def __init__(self, screen, font, winner, p1_score, p2_score, final=False):
        self.screen = screen
        self.font = font
        self.winner = winner
        self.p1_score = p1_score
        self.p2_score = p2_score
        self.final = final
        self.largura = screen.get_width()
        self.altura = screen.get_height()
        
        try:
            if self.final:
                pygame.mixer.music.load("assets/Sounds/victory_sound.wav")
            else:
                pygame.mixer.music.load("assets/Sounds/round_victory.wav")
            pygame.mixer.music.play(-1)
        except:
            pass

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.screen.fill(PRETO)
            
            # Texto principal
            if self.final:
                main_text = f"JOGADOR {self.winner.upper()} VENCEU O JOGO!"
            else:
                main_text = f"JOGADOR {self.winner.upper()} VENCEU A RODADA!"
            
            text = self.font.render(main_text, True, DOURADO)
            text_rect = text.get_rect(center=(self.largura//2, self.altura//2 - 50))
            self.screen.blit(text, text_rect)
            
            # Placar
            score_text = self.font.render(
                f"PLACAR: Jogador 1 - {self.p1_score}  |  Jogador 2 - {self.p2_score}", 
                True, BRANCO
            )
            score_rect = score_text.get_rect(center=(self.largura//2, self.altura//2 + 20))
            self.screen.blit(score_text, score_rect)
            
            # Instruções
            if self.final:
                instruction = "Pressione R para recomeçar ou Q para sair"
            else:
                instruction = "Pressione qualquer tecla para a próxima rodada..."
            
            instr_text = self.font.render(instruction, True, BRANCO)
            instr_rect = instr_text.get_rect(center=(self.largura//2, self.altura//2 + 100))
            self.screen.blit(instr_text, instr_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.final:
                        if event.key == pygame.K_r:
                            return 'restart'
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                    else:
                        return 'continue'
            
            clock.tick(60)

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1300
        self.screen_height = 638
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.key.set_repeat()
        pygame.display.set_caption("Guerra por Sintra")
        self.font = pygame.font.Font(None, 36)
        self.p1_score = 0
        self.p2_score = 0

    def run(self):
        while True:
            # Tela inicial e seleção de classe
            splash = SplashScreen(self.screen, self.font, self.screen_width, self.screen_height)
            splash.run()
            class_selection = ClassSelectionScreen(self.font)
            class_selection.run()
            
            # Resetar pontuações a cada novo jogo
            self.p1_score = 0
            self.p2_score = 0
            
            while True:  # Loop principal de rodadas
                # Criar novo mundo para cada rodada
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
                             class_selection.selected_p1, class_selection.selected_p2, self.font)
                
                # Executar batalha e verificar vencedor
                winner = world.draw_map()
                
                # Atualizar pontuação
                if winner == "p1":
                    self.p1_score += 1
                else:
                    self.p2_score += 1
                
                # Verificar vitória final
                final_victory = self.p1_score >= 2 or self.p2_score >= 2
                
                # Mostrar tela de vitória
                victory_screen = VictoryScreen(self.screen, self.font, winner, 
                                              self.p1_score, self.p2_score, final_victory)
                result = victory_screen.run()
                
                # Reiniciar ou sair
                if final_victory:
                    if result == 'restart':
                        break  # Volta para o menu inicial
                    else:
                        pygame.quit()
                        sys.exit()

if __name__ == "__main__":
    jogo = Game()
    jogo.run()