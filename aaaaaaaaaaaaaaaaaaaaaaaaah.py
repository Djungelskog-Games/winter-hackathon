import pygame
import sys
import os
import math
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Definições globais de cores e tamanhos
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CINZENTO = (128, 128, 128)
DOURADO = (218, 165, 32)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0, 50)
TILE_SIZE = 32
SIZE_X = 7
SIZE_Y = 7
SCALE = 2
FONT = "assets\Font\Pixeboy.ttf"

POWERUPS = [
    {'type': 'health', 'name': ' Queijada Especial', 'description': '+20 Vida Maxima', 'value': 20},
    {'type': 'attack', 'name': 'Travesseiro Magico', 'description': '+3 Ataque', 'value': 3},
    {'type': 'move_range', 'name': 'Faca da Chinada', 'description': '+1 Movimento', 'value': 1},
    {'type': 'attack_range', 'name': 'Pedra da Calcada', 'description': '+1 Alcance de Ataque', 'value': 1},
    {'type': 'regeneration', 'name': 'Betty', 'description': 'Cura 5 por turno', 'value': 5}
]

pygame.mixer.init()
SOUNDS = {'vencer': pygame.mixer.Sound('assets/Sounds/vencer.wav'),
           'morrer': pygame.mixer.Sound('assets/Sounds/morrer.wav'),
           'butao': pygame.mixer.Sound('assets/Sounds/clicar_butao.wav'),
           'powerup': pygame.mixer.Sound('assets/Sounds/apanhar_powerup.wav'),
           'Bufo': pygame.mixer.Sound('assets/Sounds/Bufo_ataque.wav'),
           'Raposa': pygame.mixer.Sound('assets/Sounds/Raposa_ataque.wav'),
           'Lebre': pygame.mixer.Sound('assets/Sounds/Lebre_ataque.wav'),
           'Urso': pygame.mixer.Sound('assets/Sounds/urso_ataque.wav')}

# -------------------- Classes de Interface --------------------
class BotaoIcone:
    def __init__(self, x, y, image_path, class_name, callback, player, size=(150, 150)):
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
            overlay_rect2 = overlay_image2.get_rect(center=(self.largura // 2, 325))
        except pygame.error:
            overlay_image2 = pygame.Surface((600, 100), pygame.SRCALPHA)
            overlay_image2.fill((0, 0, 0, 180))
            overlay_rect2 = overlay_image2.get_rect(center=(self.largura // 2, 250))

        # Configurações da animação
        amplitude = 10  # Altura do movimento em pixels
        velocidade = 0.04  # Velocidade da animação
        angulo = 0
        clock = pygame.time.Clock()

        while True:
            # Calcula movimento vertical usando seno
            deslocamento_y = math.sin(angulo) * amplitude
            overlay_rect.centery = 150 + deslocamento_y  # Aplica o deslocamento
            angulo += velocidade

            # Redesenha todos os elementos
            self.screen.blit(splash_image, image_rect)
            self.screen.blit(overlay_image, overlay_rect)
            self.screen.blit(overlay_image2, overlay_rect2)
            pygame.display.flip()

            # Controla a taxa de atualização
            clock.tick(60)

            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.stop()
                    return

class ClassSelectionScreen:
    def __init__(self, font):
        SOUNDS['butao'].play()
        self.largura = 1000
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
                       "assets/Classes/Lebre.png", "Lebre", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x, self.player1_y, 
                       "assets/Classes/Bufo.png", "Bufo", self.handle_class_selection, "p1"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player1_y, 
                       "assets/Classes/Raposa.png", "Raposa", self.handle_class_selection, "p1")    
        ]
        self.buttons_p2 = [
            BotaoIcone(self.base_x - self.icon_spacing, self.player2_y, 
                       "assets/Classes/Lebre.png", "Lebre", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x, self.player2_y, 
                       "assets/Classes/Bufo.png", "Bufo", self.handle_class_selection, "p2"),
            BotaoIcone(self.base_x + self.icon_spacing, self.player2_y, 
                       "assets/Classes/Raposa.png", "Raposa", self.handle_class_selection, "p2")
        ]
        self.confirm_button = BotaoIcone(self.largura//2, self.altura - 100, 
                                         "assets/Classes/confirm_button.png", "Confirmar", 
                                         lambda p, c: self.confirm_selection(), "confirm", (700, 90))

        self.stats = {
            "Lebre": {"Vida": 80, "Ataque": 8, "Movimento": 4, "Alcance": 1},
            "Bufo": {"Vida": 100, "Ataque": 10, "Movimento": 3, "Alcance": 2},
            "Raposa": {"Vida": 120, "Ataque": 12, "Movimento": 2, "Alcance": 3}
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
            
            self.screen.blit(tooltip_surface, (x, y))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill(PRETO)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            text_p1 = self.font.render("Player 1", True, VERMELHO)
            self.screen.blit(text_p1, text_p1.get_rect(center=(self.largura//2, 75)))
            text_p2 = self.font.render("Player 2", True, VERMELHO)
            self.screen.blit(text_p2, text_p2.get_rect(center=(self.largura//2, 325)))
            
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
                    
            pygame.display.flip()
            clock.tick(60)

class PowerupButton:
    def __init__(self, x, y, width, height, powerup, callback):
        SOUNDS['powerup'].play()
        self.rect = pygame.Rect(x, y, width, height)
        self.powerup = powerup
        self.callback = callback
        self.font = pygame.font.Font(FONT, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, DOURADO, self.rect, border_radius=10)
        pygame.draw.rect(screen, PRETO, self.rect.inflate(-4, -4), border_radius=8)
        
        title = self.font.render(self.powerup['name'], True, BRANCO)
        title_rect = title.get_rect(center=(self.rect.centerx, self.rect.top + 20))
        screen.blit(title, title_rect)
        
        desc = self.font.render(self.powerup['description'], True, BRANCO)
        desc_rect = desc.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(desc, desc_rect)

    def on_click(self):
        self.callback(self.powerup)

class PowerupSelectionScreen:
    def __init__(self, screen, font, powerups, player):
        self.screen = screen
        self.font = font
        self.powerups = powerups
        self.player = player
        self.selected_powerup = None
        self.buttons = []
        
        try:
            self.powerup_bg = pygame.image.load("assets/Classes/Powerup_Background.png").convert_alpha()
            self.powerup_bg = pygame.transform.scale(self.powerup_bg, screen.get_size())
        except pygame.error:
            self.powerup_bg = None

        pygame.display.flip()

        button_width = 300
        button_height = 150
        spacing = 30
        total_width = 3 * button_width + 2 * spacing
        start_x = (screen.get_width() - total_width) // 2
        y = screen.get_height() // 2

        for i, powerup in enumerate(powerups):
            x = start_x + i * (button_width + spacing)
            btn = PowerupButton(x, y, button_width, button_height, powerup, self.select_powerup)
            self.buttons.append(btn)

    def select_powerup(self, powerup):
        self.selected_powerup = powerup

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            if self.powerup_bg:
                self.screen.blit(self.powerup_bg, (0, 0))
            else:
                self.screen.fill(PRETO)

            title_text = self.font.render(f"Jogador, {self.player.upper()} - Escolha um Powerup:", True, VERMELHO)
            title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 100))
            self.screen.blit(title_text, title_rect)

            for btn in self.buttons:
                btn.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        if btn.rect.collidepoint(event.pos):
                            btn.on_click()
                            return self.selected_powerup
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return None
            clock.tick(60)

# -------------------- Classes de Jogo --------------------
class Player:
    def __init__(self, image_path, start_grid_pos, speed, scale=1, class_name="Lebre", font=FONT, powerups=None):
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
        self.speed = speed

        # Configurações base
        health_dict = {"Lebre": 80, "Bufo": 100, "Raposa": 120}
        attack_dict = {"Lebre": 8, "Bufo": 10, "Raposa": 12}
        move_range_dict = {"Lebre": 4, "Bufo": 3, "Raposa": 2}
        attack_range_dict = {"Lebre": 1, "Bufo": 2, "Raposa": 3}
        
        self.base_health = health_dict[class_name]
        self.base_attack = attack_dict[class_name]
        self.base_move_range = move_range_dict[class_name]
        self.base_attack_range = attack_range_dict[class_name]
        self.base_speed = speed

        # Aplicar powerups
        self.max_health = self.base_health
        self.attack_damage = self.base_attack
        self.move_range = self.base_move_range
        self.attack_range = self.base_attack_range
        self.regeneration = 0

        for p in (powerups or []):
            if p['type'] == 'health':
                self.max_health += p['value']
            elif p['type'] == 'attack':
                self.attack_damage += p['value']
            elif p['type'] == 'move_range':
                self.move_range += p['value']
            elif p['type'] == 'attack_range':
                self.attack_range += p['value']
            elif p['type'] == 'regeneration':
                self.regeneration += p['value']

        self.health = self.max_health
        self.moves_remaining = self.move_range
        self.class_name = class_name

        self.font = font if font else pygame.font.Font(FONT, 24)
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
                    self.stamina = True
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
        
        if self.damage_display_time > 0:
            damage_text = self.font.render(f"-{self.last_damage}", True, (255, 0, 0))
            text_rect = damage_text.get_rect(center=(tile_center_x, sprite_draw_y - 20))
            display.blit(damage_text, text_rect)

def attack(attacker, defender):
    SOUNDS[attacker.class_name].play()
    align = (attacker.grid_x == defender.grid_x or attacker.grid_y == defender.grid_y)
    if abs(attacker.grid_x - defender.grid_x) <= attacker.attack_range and abs(attacker.grid_y - defender.grid_y) <= attacker.attack_range and align:
        damage = attacker.attack_damage
        defender.health -= damage
        defender.last_damage = damage
        defender.damage_display_time = 2000
        
        if defender.health < 0:
            defender.health = 0

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
    def __init__(self, x, y, tilepack, tilesize, display, scale, player1_class, player2_class, font, p1_powerups=None, p2_powerups=None):
        SOUNDS['butao'].play()
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
            "Lebre": "assets/Classes/Lebre.png",
            "Bufo": "assets/Classes/Bufo.png",
            "Raposa": "assets/Classes/Raposa.png"
        }
        pos1 = (0, 0)
        pos2 = (self.x - 1, self.y - 1)
        self.player1 = Player(self.player_images.get(player1_class), 
                             pos1, speed=0.5, scale= self.scale, 
                             class_name=player1_class, font=font, powerups=p1_powerups)
        self.player2 = Player(self.player_images.get(player2_class), 
                             pos2, speed=0.5, scale= self.scale, 
                             class_name=player2_class, font=font, powerups=p2_powerups)
        self.current_turn = "p1"
        self.player1.moves_remaining = self.player1.move_range
        self.player2.moves_remaining = self.player2.move_range
        
        
        pygame.mixer.music.load("assets/Sounds/song_batalha.wav")
        pygame.mixer.music.play(-1)

    def draw_attack_range(self, offset_x, offset_y):
        overlay = pygame.Surface((self.x * TILE_SIZE * SCALE, self.y * TILE_SIZE * SCALE), pygame.SRCALPHA)
        
        current_player = self.player1 if self.current_turn == "p1" else self.player2
        attack_range = current_player.attack_range
        px, py = current_player.grid_x, current_player.grid_y

        for dx in range(-attack_range, attack_range + 1):
            for dy in range(-attack_range, attack_range + 1):
                if (dx == 0 and abs(dy) <= attack_range) or (dy == 0 and abs(dx) <= attack_range):
                    x = px + dx
                    y = py + dy
                    if 0 <= x < self.x and 0 <= y < self.y:
                        pos_x = x * TILE_SIZE * SCALE
                        pos_y = y * TILE_SIZE * SCALE
                        pygame.draw.rect(overlay, VERMELHO, (pos_x, pos_y, TILE_SIZE*SCALE, TILE_SIZE*SCALE))

        self.display.blit(overlay, (offset_x, offset_y))

    def draw_player_stats(self, display, offset_x, offset_y, player, side):
        panel_width = 200
        panel_height = 250
        spacing = 20
        
        if side == "left":
            panel_x = offset_x - panel_width - spacing
        else:
            panel_x = offset_x + (self.x * self.tilesize * self.scale) + spacing
            
        panel_y = offset_y + 50
        
        # Fundo do painel
        pygame.draw.rect(display, DOURADO, (panel_x, panel_y, panel_width, panel_height), border_radius=10)
        pygame.draw.rect(display, PRETO, (panel_x+2, panel_y+2, panel_width-4, panel_height-4), border_radius=8)
        
        # Sprite do jogador
        sprite = pygame.transform.scale(player.image, (100, 100))
        display.blit(sprite, (panel_x + (panel_width-100)//2, panel_y + 10))
        
        # Stats
        stats_font = pygame.font.Font(FONT, 24)
        y_offset = 120
        
        # Ataque
        attack_text = stats_font.render(f"Ataque: {player.attack_damage}", True, BRANCO)
        display.blit(attack_text, (panel_x + 20, panel_y + y_offset))
        y_offset += 30
        
        # Movimento
        move_text = stats_font.render(f"Movimento: {player.move_range}", True, BRANCO)
        display.blit(move_text, (panel_x + 20, panel_y + y_offset))
        y_offset += 30
        
        # Alcance
        range_text = stats_font.render(f"Alcance: {player.attack_range}", True, BRANCO)
        display.blit(range_text, (panel_x + 20, panel_y + y_offset))
        y_offset += 30
        
        # Barra de vida
        health_width = 160
        health_height = 20
        health_x = panel_x + (panel_width - health_width)//2
        health_y = panel_y + y_offset
        
        # Fundo da barra
        pygame.draw.rect(display, CINZENTO, (health_x, health_y, health_width, health_height))
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
        clock = pygame.time.Clock()
        player1_controls = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0), pygame.K_s: (0, 1), pygame.K_d: (1, 0)}
        player2_controls = {pygame.K_UP: (0, -1), pygame.K_LEFT: (-1, 0), pygame.K_DOWN: (0, 1), pygame.K_RIGHT: (1, 0)}
        font = pygame.font.Font(FONT, 40)
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
                        if self.current_turn == "p1":
                            self.player1.moves_remaining = 0
                        else:
                            self.player2.moves_remaining = 0
                    elif event.key == pygame.K_SPACE:
                        if self.current_turn == "p1":
                            attack(self.player1, self.player2)
                            self
                        else:
                            attack(self.player2, self.player1)
                    else:
                        self.key = event.key
                        SOUNDS['butao'].play()

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
                    self.player1.health = min(self.player1.health + self.player1.regeneration, self.player1.max_health)
                    self.current_turn = "p2"
                    self.player2.moves_remaining = self.player2.move_range
            elif self.current_turn == "p2" and not self.player2.moving:
                if self.player2.moves_remaining == 0:
                    self.player2.health = min(self.player2.health + self.player2.regeneration, self.player2.max_health)
                    self.current_turn = "p1"
                    self.player1.moves_remaining = self.player1.move_range

            if self.player1.health <= 0:
                SOUNDS['morrer'].play()
                winner = "p2"
                running = False
            elif self.player2.health <= 0:
                SOUNDS['morrer'].play()
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

            self.draw_attack_range(offset_x, offset_y)

            # Desenha stats dos jogadores
            self.draw_player_stats(self.display, offset_x, offset_y, self.player1, "left")
            self.draw_player_stats(self.display, offset_x, offset_y, self.player2, "right")

            self.player1.draw(self.display, offset_x, offset_y)
            self.player2.draw(self.display, offset_x, offset_y)

            turn_text = font.render(f"TURNO DO JOGADOR: {self.current_turn.upper()}", True, DOURADO)
            text_rect = turn_text.get_rect(center=(self.screen_width//2, 70))
            self.display.blit(turn_text, text_rect)
            
            controls_y = self.screen_height - 100
            controls = [
                "WASD - Movimentar Jogador 1",
                "SETAS - Movimentar Jogador 2",
                "SPACE - Atacar",
                "ENTER - Finalizar Turno"
            ]
            
            for i, text in enumerate(controls):
                control_text = controls_font.render(text, True, DOURADO)
                text_rect = control_text.get_rect(center=(self.screen_width//2, controls_y + i*25))
                self.display.blit(control_text, text_rect)

            pygame.display.flip()
        
        pygame.mixer.music.stop()
        return winner

class VictoryScreen:
    def __init__(self, screen, font, winner, p1_score, p2_score, final=False):
        SOUNDS['vencer'].play()
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
            
            if self.final:
                main_text = f"JOGADOR {self.winner.upper()} VENCEU O JOGO!"
            else:
                main_text = f"JOGADOR {self.winner.upper()} VENCEU A RODADA!"
            
            text = self.font.render(main_text, True, DOURADO)
            text_rect = text.get_rect(center=(self.largura//2, self.altura//2 - 50))
            self.screen.blit(text, text_rect)
            
            score_text = self.font.render(
                f"PLACAR: Jogador 1 - {self.p1_score}  |  Jogador 2 - {self.p2_score}", 
                True, BRANCO
            )
            score_rect = score_text.get_rect(center=(self.largura//2, self.altura//2 + 20))
            self.screen.blit(score_text, score_rect)
            
            if self.final:
                instruction = "Pressione R para recomeçar ou Q para sair"
            else:
                instruction = "Pressione qualquer tecla para a proxima rodada..."
            
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
        self.font = pygame.font.Font(FONT, 30)
        self.p1_score = 0
        self.p2_score = 0
        self.p1_powerups = []
        self.p2_powerups = []

    def run(self):
        while True:
            splash = SplashScreen(self.screen, self.font, self.screen_width, self.screen_height)
            splash.run()
            class_selection = ClassSelectionScreen(self.font)
            class_selection.run()
            
            self.p1_score = 0
            self.p2_score = 0
            self.p1_powerups = []
            self.p2_powerups = []
            
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
                
                final_victory = self.p1_score >= 5 or self.p2_score >= 5
                
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