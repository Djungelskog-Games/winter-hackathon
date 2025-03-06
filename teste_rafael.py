import pygame
import sys
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Definições globais de cores e tamanhos
VERDE    = (0, 255, 0)
CINZENTO = (128, 128, 128)
DOURADO  = (218, 165, 32)
PRETO    = (0, 0, 0)
BRANCO   = (255, 255, 255)
TILE_SIZE = 32
SIZE_X    = 7
SIZE_Y    = 7
SCALE     = 2

# -------------------- Classes de Interface --------------------
class BotaoIcone:
    def __init__(self, x, y, image_path, class_name, callback, player):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
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
        pygame.display.set_caption("Seleção de Classes")

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
                                         lambda p, c: self.confirm_selection(), "confirm")

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
            print(f"Jogador 1: {self.selected_p1}, Jogador 2: {self.selected_p2}")
            self.running = False

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
            for btn in self.buttons_p1 + self.buttons_p2:
                btn.selected = ((self.selected_p1 == btn.class_name and btn.player == "p1") or 
                                (self.selected_p2 == btn.class_name and btn.player == "p2"))
                btn.draw(self.screen)
            self.confirm_button.image.set_alpha(255 if self.confirm_enabled else 128)
            self.confirm_button.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for btn in self.buttons_p1 + self.buttons_p2 + [self.confirm_button]:
                    btn.handle_event(event)
            pygame.display.flip()
            clock.tick(60)

# -------------------- Classes de Jogo --------------------
# A classe Player agora possui atributos para alcance (move_range) e pontos de movimento (moves_remaining),
# e o movimento é opcional. Além disso, há uma opção de ataque que, quando acionada, ataca todos os inimigos
# num raio de 1 tile.
class Player:
    def __init__(self, image_path, start_grid_pos, speed, scale=1, class_name="Lebre"):
        try:
            full_image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            full_image = pygame.Surface((TILE_SIZE * scale, TILE_SIZE * scale))
            full_image.fill(VERDE)
        self.sprite_scale_factor = scale
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
        self.health = 100

        move_range_dict = {"Lebre": 3, "Raposa": 2, "Veado": 1}
        self.move_range = move_range_dict.get(class_name, 1)
        self.moves_remaining = self.move_range
        self.class_name = class_name

    def handle_input(self, keys, controls, grid_width, grid_height):
        # Permite movimento somente se houver pontos de movimento
        if not self.moving and self.moves_remaining > 0:
            for key, (dx, dy) in controls.items():
                if keys[key]:
                    new_grid_x = self.grid_x + dx
                    new_grid_y = self.grid_y + dy
                    if 0 <= new_grid_x < grid_width and 0 <= new_grid_y < grid_height:
                        self.dest_grid_x = new_grid_x
                        self.dest_grid_y = new_grid_y
                        self.moving = True
                    break

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

    def draw(self, display, offset_x, offset_y):
        tile_pixel_size = TILE_SIZE * SCALE
        tile_top_left_x = offset_x + self.pixel_x
        tile_top_left_y = offset_y + self.pixel_y
        tile_center_x = tile_top_left_x + tile_pixel_size / 2
        tile_center_y = tile_top_left_y + tile_pixel_size / 2
        sprite_draw_x = tile_center_x - self.sprite_width / 2
        sprite_draw_y = tile_center_y - self.sprite_height / 2
        display.blit(self.image, (sprite_draw_x, sprite_draw_y))
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

# A opção de ataque: ataca tudo num tile de raio 1
def attack(attacker, defender):
    # Se o inimigo estiver a 1 tile (incluindo diagonais)
    if abs(attacker.grid_x - defender.grid_x) <= 1 and abs(attacker.grid_y - defender.grid_y) <= 1:
        damage = 10
        defender.health -= damage
        if defender.health < 0:
            defender.health = 0
        print(f"{attacker.class_name} atacou {defender.class_name}! HP do defensor: {defender.health}")

# Classe World – gerencia o mapa, os jogadores e as ações de movimento/ataque
class World:
    def __init__(self, x, y, tilepack, tilesize, display, scale, player1_class, player2_class):
        self.x = x
        self.y = y
        self.tilesize = tilesize
        self.display = display
        self.scale = scale
        self.mapa = []
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
        self.player1 = Player(self.player_images.get(player1_class, "assets/Classes/lebre_icon.png"), pos1, speed=0.5, scale= self.scale * 0.70, class_name=player1_class)
        self.player2 = Player(self.player_images.get(player2_class, "assets/Classes/lebre_icon.png"), pos2, speed=0.5, scale= self.scale * 0.70, class_name=player2_class)
        self.current_turn = "p1"
        self.player1.moves_remaining = self.player1.move_range
        self.player2.moves_remaining = self.player2.move_range

    def draw_map(self):
        display_width, display_height = self.display.get_size()
        map_width = self.x * self.tilesize * self.scale
        map_height = self.y * self.tilesize * self.scale
        offset_x = (display_width - map_width) // 2
        offset_y = (display_height - map_height) // 2

        running = True
        clock = pygame.time.Clock()
        player1_controls = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0), pygame.K_s: (0, 1), pygame.K_d: (1, 0)}
        player2_controls = {pygame.K_UP: (0, -1), pygame.K_LEFT: (-1, 0), pygame.K_DOWN: (0, 1), pygame.K_RIGHT: (1, 0)}
        font = pygame.font.Font(None, 36)

        while running:
            dt = clock.tick(60)  # dt em ms
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Pressione RETURN para terminar o turno sem mover
                    if event.key == pygame.K_RETURN:
                        if self.current_turn == "p1":
                            self.player1.moves_remaining = 0
                        else:
                            self.player2.moves_remaining = 0
                    # Pressione SPACE para atacar
                    elif event.key == pygame.K_SPACE:
                        if self.current_turn == "p1":
                            attack(self.player1, self.player2)
                            self.player1.moves_remaining = 0
                        else:
                            attack(self.player2, self.player1)
                            self.player2.moves_remaining = 0

            keys = pygame.key.get_pressed()
            if self.current_turn == "p1":
                self.player1.handle_input(keys, player1_controls, self.x, self.y)
            else:
                self.player2.handle_input(keys, player2_controls, self.x, self.y)

            self.player1.update(dt)
            self.player2.update(dt)

            # Se o jogador ativo concluiu o movimento ou escolheu terminar o turno,
            # alterna turno e reseta os pontos de movimento do próximo jogador.
            if self.current_turn == "p1" and not self.player1.moving:
                if self.player1.moves_remaining == 0:
                    self.current_turn = "p2"
                    self.player2.moves_remaining = self.player2.move_range
            elif self.current_turn == "p2" and not self.player2.moving:
                if self.player2.moves_remaining == 0:
                    self.current_turn = "p1"
                    self.player1.moves_remaining = self.player1.move_range

            if self.bg_image:
                self.display.blit(self.bg_image, (0, 0))
            else:
                self.display.fill(PRETO)

            for y_idx, row in enumerate(self.mapa):
                for x_idx, tile in enumerate(row):
                    pos_x_tile = offset_x + x_idx * self.tilesize * self.scale
                    pos_y_tile = offset_y + y_idx * self.tilesize * self.scale
                    self.display.blit(tile, (pos_x_tile, pos_y_tile))

            self.player1.draw(self.display, offset_x, offset_y)
            self.player2.draw(self.display, offset_x, offset_y)

            turn_text = font.render(f"Turn: {self.current_turn}", True, BRANCO)
            self.display.blit(turn_text, (10, 10))

            pygame.display.flip()
        pygame.quit()
        sys.exit()

# Classe principal do jogo
class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1300
        self.screen_height = 638
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Guerra por Sintra")
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        splash = SplashScreen(self.screen, self.font, self.screen_width, self.screen_height)
        splash.run()
        class_selection = ClassSelectionScreen(self.font)
        class_selection.run()
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
                      class_selection.selected_p1, class_selection.selected_p2)
        world.draw_map()

if __name__ == "__main__":
    jogo = Game()
    jogo.run()
