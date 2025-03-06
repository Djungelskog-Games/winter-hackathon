import pygame
import sys
import os
import random
import math

os.environ['SDL_VIDEO_CENTERED'] = '1'

# Cores
VERDE = (0, 255, 0)
CINZENTO = (128, 128, 128)
DOURADO = (218, 165, 32)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
LARANJA = (255, 165, 0)

# Configurações
TILE_SIZE = 32
SIZE_X = 7
SIZE_Y = 7
SCALE = 2

# Sistema de Partículas
class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particles(self, num):
        for _ in range(num):
            x = random.randint(0, 1300)
            y = random.randint(0, 638)
            self.particles.append({
                'pos': [x, y],
                'color': random.choice([VERMELHO, AMARELO, BRANCO, DOURADO]),
                'size': random.randint(2, 5),
                'speed': [random.uniform(-1, 1), random.uniform(-1, 1)],
                'lifetime': random.randint(20, 40)
            })
    
    def update(self):
        for p in self.particles[:]:
            p['pos'][0] += p['speed'][0]
            p['pos'][1] += p['speed'][1]
            p['lifetime'] -= 1
            if p['lifetime'] <= 0:
                self.particles.remove(p)
    
    def draw(self, surface):
        for p in self.particles:
            pygame.draw.circle(surface, p['color'], (int(p['pos'][0]), int(p['pos'][1])), p['size'])

# Itens
class Item:
    def __init__(self, x, y, effect_type):
        self.grid_x = x
        self.grid_y = y
        self.effect_type = effect_type
        self.used = False
        
        try:
            if effect_type == "health":
                self.image = pygame.image.load("assets/Items/health_pack.png").convert_alpha()
            elif effect_type == "energy":
                self.image = pygame.image.load("assets/Items/energy_drink.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE*SCALE, TILE_SIZE*SCALE))
        except:
            self.image = pygame.Surface((TILE_SIZE*SCALE, TILE_SIZE*SCALE))
            self.image.fill(LARANJA if effect_type == "health" else AMARELO)

    def apply_effect(self, player):
        if not self.used:
            if self.effect_type == "health":
                player.health = min(120, player.health + 20)
            elif self.effect_type == "energy":
                player.gain_energy(30)
            self.used = True

# Jogador
class Player:
    def __init__(self, image_path, start_grid_pos, speed, scale=1, class_name="Lebre", font=None):
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
        self.speed = speed

        # Atributos da classe
        health_dict = {"Lebre": 80, "Raposa": 100, "Veado": 120}
        attack_dict = {"Lebre": 8, "Raposa": 10, "Veado": 12}
        move_range_dict = {"Lebre": 3, "Raposa": 2, "Veado": 1}
        
        self.health = health_dict.get(class_name, 1000)
        self.attack_damage = attack_dict.get(class_name, 50)
        self.move_range = move_range_dict.get(class_name, 1)
        self.moves_remaining = self.move_range
        self.class_name = class_name

        # Sistema de energia
        self.energy = 0
        self.max_energy = 100
        self.special_ready = False
        self.invulnerable = False
        self.invulnerability_timer = 0
        self.critical_chance = 0.1
        self.dodge_chance = 0.15 if class_name == "Lebre" else 0.1

        # Visual
        self.font = font if font else pygame.font.Font(None, 24)
        self.last_damage = 0
        self.damage_display_time = 0

    def gain_energy(self, amount):
        self.energy = min(self.max_energy, self.energy + amount)
        if self.energy >= self.max_energy:
            self.special_ready = True

    def use_special(self):
        if self.special_ready:
            if self.class_name == "Raposa":
                self.attack_damage *= 1.5
                self.invulnerable = True
                self.invulnerability_timer = 5000
            elif self.class_name == "Veado":
                self.health = min(120, self.health + 30)
            elif self.class_name == "Lebre":
                self.move_range += 1
                self.moves_remaining += 1
            
            self.energy = 0
            self.special_ready = False

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

        # Atualizações de status
        if self.invulnerable:
            self.invulnerability_timer = max(0, self.invulnerability_timer - dt)
            if self.invulnerability_timer == 0:
                self.invulnerable = False
                if self.class_name == "Raposa":
                    self.attack_damage = 10

        if self.damage_display_time > 0:
            self.damage_display_time = max(0, self.damage_display_time - dt)

        # Geração de energia passiva
        if not self.moving and random.random() < 0.02:
            self.gain_energy(5)

    def draw(self, display, offset_x, offset_y):
        tile_pixel_size = TILE_SIZE * SCALE
        tile_top_left_x = offset_x + self.pixel_x
        tile_top_left_y = offset_y + self.pixel_y
        tile_center_x = tile_top_left_x + tile_pixel_size / 2
        tile_center_y = tile_top_left_y + tile_pixel_size / 2
        
        # Desenhar sprite
        sprite_draw_x = tile_center_x - self.sprite_width / 2
        sprite_draw_y = tile_center_y - self.sprite_height / 2
        display.blit(self.image, (sprite_draw_x, sprite_draw_y))

        # Efeitos de dano
        if self.damage_display_time > 0:
            if isinstance(self.last_damage, str):
                damage_text = self.font.render(self.last_damage, True, VERMELHO)
            else:
                damage_text = self.font.render(f"-{self.last_damage}", True, VERMELHO)
            text_rect = damage_text.get_rect(center=(tile_center_x, sprite_draw_y - 20))
            display.blit(damage_text, text_rect)

        # Barra de vida
        self.draw_health_bar(display, tile_center_x, sprite_draw_y + self.sprite_height)

    def draw_health_bar(self, display, center_x, sprite_bottom_y):
        bar_width = 50
        bar_height = 5
        margin = 5
        fill = (self.health / 120) * bar_width  # Max 120 HP
        
        pygame.draw.rect(display, CINZENTO, (center_x - bar_width/2, sprite_bottom_y + margin, bar_width, bar_height))
        pygame.draw.rect(display, VERDE, (center_x - bar_width/2, sprite_bottom_y + margin, fill, bar_height))

# Função de ataque
def attack(attacker, defender):
    if random.random() < defender.dodge_chance:
        defender.damage_display_time = 2000
        defender.last_damage = "Esquiva!"
        return
    
    damage = attacker.attack_damage
    
    if random.random() < attacker.critical_chance:
        damage = int(damage * 1.5)
        defender.last_damage = f"CRIT! {damage}"
    else:
        defender.last_damage = damage
    
    if not defender.invulnerable:
        defender.health -= damage
        attacker.gain_energy(15)
    
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

# Mundo do jogo
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
        self.font = font
        
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
        self.player1 = Player(self.player_images[player1_class], pos1, 0.5, 
                            self.scale * 0.70, player1_class, font)
        self.player2 = Player(self.player_images[player2_class], pos2, 0.5, 
                            self.scale * 0.70, player2_class, font)
        
        self.current_turn = "p1"
        self.player1.moves_remaining = self.player1.move_range
        self.player2.moves_remaining = self.player2.move_range
        self.items = []
        self.spawn_items()
        self.show_attack_range = False
        self.highlighted_tiles = []
        self.paused = False
        
        try:
            self.attack_sound = pygame.mixer.Sound("assets/Sounds/attack.wav")
        except:
            self.attack_sound = None

        pygame.mixer.music.load("assets/Sounds/song_batalha.wav")
        pygame.mixer.music.play(-1)

    def spawn_items(self):
        for _ in range(3):
            x = random.randint(0, self.x-1)
            y = random.randint(0, self.y-1)
            while (x, y) in [(p.grid_x, p.grid_y) for p in [self.player1, self.player2]]:
                x = random.randint(0, self.x-1)
                y = random.randint(0, self.y-1)
            self.items.append(Item(x, y, random.choice(["health", "energy"])))

    def draw_map(self):
        winner = None
        running = True
        clock = pygame.time.Clock()
        player1_controls = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0), 
                          pygame.K_s: (0, 1), pygame.K_d: (1, 0)}
        player2_controls = {pygame.K_UP: (0, -1), pygame.K_LEFT: (-1, 0),
                          pygame.K_DOWN: (0, 1), pygame.K_RIGHT: (1, 0)}
        
        while running:
            dt = clock.tick(60) if not self.paused else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
                    elif event.key == pygame.K_e:
                        current_player = self.player1 if self.current_turn == "p1" else self.player2
                        current_player.use_special()
                    elif event.key == pygame.K_TAB:
                        self.show_attack_range = not self.show_attack_range
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_r and self.paused:
                        return 'restart'
                    elif event.key == pygame.K_q and self.paused:
                        pygame.quit()
                        sys.exit()

            if not self.paused:
                keys = pygame.key.get_pressed()
                current_player = self.player1 if self.current_turn == "p1" else self.player2
                other_pos = (self.player2.grid_x, self.player2.grid_y) if self.current_turn == "p1" else (self.player1.grid_x, self.player1.grid_y)
                
                current_player.handle_input(keys, 
                                          player1_controls if self.current_turn == "p1" else player2_controls,
                                          self.x, self.y, other_pos)
                
                self.player1.update(dt)
                self.player2.update(dt)

                if current_player.moves_remaining == 0 and not current_player.moving:
                    self.current_turn = "p2" if self.current_turn == "p1" else "p1"
                    next_player = self.player2 if self.current_turn == "p2" else self.player1
                    next_player.moves_remaining = next_player.move_range

                # Verificar coletáveis
                for item in self.items[:]:
                    if (current_player.grid_x, current_player.grid_y) == (item.grid_x, item.grid_y):
                        item.apply_effect(current_player)
                        self.items.remove(item)

                # Verificar vitória
                if self.player1.health <= 0 or self.player2.health <= 0:
                    winner = "p1" if self.player2.health <= 0 else "p2"
                    running = False

            # Desenhar
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
                    pos_x = offset_x + x_idx * self.tilesize * self.scale
                    pos_y = offset_y + y_idx * self.tilesize * self.scale
                    self.display.blit(tile, (pos_x, pos_y))

            for item in self.items:
                pos_x = offset_x + item.grid_x * TILE_SIZE * SCALE
                pos_y = offset_y + item.grid_y * TILE_SIZE * SCALE
                self.display.blit(item.image, (pos_x, pos_y))

            self.player1.draw(self.display, offset_x, offset_y)
            self.player2.draw(self.display, offset_x, offset_y)

            # UI
            turn_text = self.font.render(f"Turno: {self.current_turn}", True, BRANCO)
            self.display.blit(turn_text, (10, 10))
            
            self.draw_energy_bar(self.player1 if self.current_turn == "p1" else self.player2, offset_x, offset_y)
            
            if self.show_attack_range:
                self.draw_attack_range(current_player, offset_x, offset_y)

            if self.paused:
                self.draw_pause_menu()

            pygame.display.flip()

        pygame.mixer.music.stop()
        return winner

    def draw_energy_bar(self, player, offset_x, offset_y):
        bar_width = 100
        bar_height = 8
        x = offset_x + player.grid_x * TILE_SIZE * SCALE
        y = offset_y + player.grid_y * TILE_SIZE * SCALE - 20
        fill = (player.energy / player.max_energy) * bar_width
        
        pygame.draw.rect(self.display, CINZENTO, (x, y, bar_width, bar_height))
        pygame.draw.rect(self.display, AMARELO, (x, y, fill, bar_height))
        
        if player.special_ready:
            text = self.font.render("ESPECIAL PRONTO!", True, VERMELHO)
            text_rect = text.get_rect(center=(self.screen_width//2, 50))
            self.display.blit(text, text_rect)

    def draw_attack_range(self, player, offset_x, offset_y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                x = player.grid_x + dx
                y = player.grid_y + dy
                if 0 <= x < self.x and 0 <= y < self.y:
                    pos_x = offset_x + x * TILE_SIZE * SCALE
                    pos_y = offset_y + y * TILE_SIZE * SCALE
                    surf = pygame.Surface((TILE_SIZE*SCALE, TILE_SIZE*SCALE), pygame.SRCALPHA)
                    surf.fill((255, 0, 0, 50))
                    self.display.blit(surf, (pos_x, pos_y))

    def draw_pause_menu(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.display.blit(overlay, (0, 0))
        
        text = self.font.render("JOGO PAUSADO", True, BRANCO)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 50))
        self.display.blit(text, text_rect)
        
        options = ["Continuar (P)", "Reiniciar (R)", "Sair (Q)"]
        for i, option in enumerate(options):
            text = self.font.render(option, True, BRANCO)
            text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2 + i*50))
            self.display.blit(text, text_rect)

# Telas
class SplashScreen:
    def __init__(self, screen, font, largura, altura):
        self.screen = screen
        self.font = font
        self.largura = largura
        self.altura = altura
        pygame.mixer.music.load("assets/Sounds/song_mainmenu.wav")
        pygame.mixer.music.play(-1)

    def run(self):
        # ... (mantido igual ao anterior)

class ClassSelectionScreen:
    def __init__(self, font):
        # ... (mantido igual ao anterior)

class VictoryScreen:
    def __init__(self, screen, font, winner):
        self.screen = screen
        self.font = font
        self.winner = winner
        self.largura = screen.get_width()
        self.altura = screen.get_height()
        self.particles = ParticleSystem()
        
        try:
            pygame.mixer.music.load("assets/Sounds/victory_sound.wav")
            pygame.mixer.music.play(-1)
        except:
            pass

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.screen.fill(PRETO)
            
            # Partículas
            self.particles.add_particles(2)
            self.particles.update()
            self.particles.draw(self.screen)
            
            # Texto
            text = self.font.render(f"Vitória do Jogador {self.winner}!", True, DOURADO)
            text_rect = text.get_rect(center=(self.largura//2, self.altura//2))
            self.screen.blit(text, text_rect)
            
            instruction = self.font.render("Pressione R para recomeçar ou Q para sair", True, BRANCO)
            instruction_rect = instruction.get_rect(center=(self.largura//2, self.altura//2 + 50))
            self.screen.blit(instruction, instruction_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 'restart'
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
            
            clock.tick(60)

# Jogo principal
class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 1300
        self.screen_height = 638
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Guerra por Sintra")
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        while True:
            # Telas
            splash = SplashScreen(self.screen, self.font, self.screen_width, self.screen_height)
            splash.run()
            
            class_selection = ClassSelectionScreen(self.font)
            class_selection.run()
            
            TILES = (
                pygame.image.load("assets/Tiles/tile0.png").convert_alpha(),
                # ... (carregar outros tiles)
            )
            
            world = World(SIZE_X, SIZE_Y, TILES, TILE_SIZE, self.screen, SCALE, 
                        class_selection.selected_p1, class_selection.selected_p2, self.font)
            
            winner = world.draw_map()
            if winner is not None:
                victory_screen = VictoryScreen(self.screen, self.font, winner)
                result = victory_screen.run()
                if result != 'restart':
                    break

if __name__ == "__main__":
    jogo = Game()
    jogo.run()