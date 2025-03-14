import pygame
import math
from constants import SCALE, TILE_SIZE, SIZE_X, SIZE_Y, FONT, SOUNDS, VERDE, VERMELHO


class Player:
    def __init__(self, image_path, start_grid_pos, speed, scale=1, class_name="Lebre", font=FONT, powerups=None):
        try:
            # Tenta carregar a imagem do jogador
            full_image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            # Caso a imagem não seja encontrada, cria uma superfície verde
            full_image = pygame.Surface((TILE_SIZE * scale, TILE_SIZE * scale))
            full_image.fill(VERDE)
        
        # Define o fator de escala e o tamanho do sprite
        self.sprite_scale_factor = scale * 0.45
        sprite_size = int(TILE_SIZE * scale * self.sprite_scale_factor)
        self.image = pygame.transform.scale(full_image, (sprite_size, sprite_size))
        self.sprite_width = sprite_size
        self.sprite_height = sprite_size

        # Define a posição inicial do jogador no grid e em pixels
        self.grid_x, self.grid_y = start_grid_pos
        self.pixel_x = self.grid_x * TILE_SIZE * scale
        self.pixel_y = self.grid_y * TILE_SIZE * scale
        self.dest_grid_x = self.grid_x
        self.dest_grid_y = self.grid_y
        self.moving = False  # Indica se o jogador está se a mover
        self.speed = speed  # Velocidade de movimento

        # Configurações base para cada classe
        health_dict = {"Lebre": 40, "Bufo": 50, "Raposa": 60, "Urso": 500, "Arqueiro": 30}
        attack_dict = {"Lebre": 8, "Bufo": 10, "Raposa": 12, "Urso": 50, "Arqueiro": 10}
        move_range_dict = {"Lebre": 4, "Bufo": 3, "Raposa": 2, "Urso": 5, "Arqueiro": 5}
        attack_range_dict = {"Lebre": 1, "Bufo": 2, "Raposa": 3, "Urso": 4, "Arqueiro": 6}
        min_attack_range_dict = {"Lebre": 0, "Bufo": 0, "Raposa": 0, "Urso": 0, "Arqueiro": 4}
        
        # Define os atributos base com base na classe
        self.base_health = health_dict[class_name]
        self.base_attack = attack_dict[class_name]
        self.base_move_range = move_range_dict[class_name]
        self.base_attack_range = attack_range_dict[class_name]
        self.base_min_attack_range = min_attack_range_dict[class_name]
        self.base_speed = speed

        # Aplica os powerups (se houver)
        self.max_health = self.base_health
        self.attack_damage = self.base_attack
        self.move_range = self.base_move_range
        self.attack_range = self.base_attack_range
        self.min_attack_range = self.base_min_attack_range
        self.regeneration = 0  # Regeneração de vida por turno
        self.lifesteal_percentage = 0 # % de vida recuperada ao atacar

        self.stamina = True  # Indica se o jogador pode atacar

        # Aplica os efeitos dos powerups
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
            elif p['type'] == 'armor':
                self.max_health += p['value']['health']
                self.move_range += p['value']['move_range']
            elif p['type'] == 'lifesteal':
                self.lifesteal_percentage += p['value']

        # Define a vida atual e os movimentos restantes
        self.health = self.max_health
        self.moves_remaining = self.move_range
        self.class_name = class_name  # Nome da classe do jogador

        # Configurações da fonte para exibir dano
        self.font = font if font else pygame.font.Font(FONT, 24)
        self.last_damage = 0  # Último dano recebido
        self.damage_display_time = 0  # Tempo de exibição do dano
        self.life_stolen_time = 0
        self.regeneration_display_time = 0

    def apply_lifesteal(self, damage_dealt):
        damage_dealt = self.attack_damage
        health_restored = math.floor(damage_dealt * self.lifesteal_percentage + 0.5) # O math.ceil arredonda para cima (por exemplo, o bufo ataca 13, como 13*0.2 = 2.6, o bufo recupera 3 de vida e não 2)
        self.health += health_restored
        self.life_stolen_amount = health_restored
        if self.lifesteal_percentage > 0:
            self.life_stolen_time = 2000
        if self.health > self.max_health:
            self.health = self.max_health

    def handle_input(self, key, controls, grid_width, grid_height, other_player_pos, coor_pedras):
        # Processa a entrada do jogador para movimentação
        if not self.moving and self.moves_remaining > 0:
            if key in controls:
                # Calcula a nova posição no grid
                new_grid_x = self.grid_x + controls.get(key)[0]
                new_grid_y = self.grid_y + controls.get(key)[1]
                # Verifica se a nova posição é válida
                if (0 <= new_grid_x < grid_width and 0 <= new_grid_y < grid_height
                    and (new_grid_x, new_grid_y) != other_player_pos and not (new_grid_x, new_grid_y) in coor_pedras):
                    self.dest_grid_x = new_grid_x
                    self.dest_grid_y = new_grid_y
                    self.moving = True  # Inicia o movimento
                    self.stamina = True  # Reseta a stamina para permitir ataque
                return

    def update(self, dt):
        # Atualiza a posição do jogador durante o movimento
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
                # Finaliza o movimento e atualiza a posição no grid
                self.grid_x = self.dest_grid_x
                self.grid_y = self.dest_grid_y
                self.moving = False
                if self.moves_remaining > 0:
                    self.moves_remaining -= 1  # Reduz os movimentos restantes
        
        # Atualiza o tempo de exibição do dano
        if self.damage_display_time > 0:
            self.damage_display_time = max(0, self.damage_display_time - dt)

        if self.life_stolen_time > 0:
            self.life_stolen_time = max(0, self.life_stolen_time - dt)

        if self.regeneration > 0 and self.regeneration_display_time > 0 and self.health < self.max_health:
            self.regeneration_display_time = max(0, self.regeneration_display_time - dt)

    def draw(self, display, offset_x, offset_y):
        # Desenha o jogador no ecrã
        tile_pixel_size = TILE_SIZE * SCALE
        tile_top_left_x = offset_x + self.pixel_x
        tile_top_left_y = offset_y + self.pixel_y
        tile_center_x = tile_top_left_x + tile_pixel_size / 2
        tile_center_y = tile_top_left_y + tile_pixel_size / 2
        sprite_draw_x = tile_center_x - self.sprite_width / 2
        sprite_draw_y = tile_center_y - self.sprite_height / 2
        display.blit(self.image, (sprite_draw_x, sprite_draw_y))
        
        # Exibe o dano recebido (se houver)
        if self.damage_display_time > 0:
            damage_text = self.font.render(f"-{self.last_damage}", True, VERMELHO)
            text_rect = damage_text.get_rect(center=(tile_center_x, sprite_draw_y - 20))
            display.blit(damage_text, text_rect)
        
        # Exibe o lifesteal (se houver)
        if self.life_stolen_time > 0:
            life_stolen_text = self.font.render(f"+{self.life_stolen_amount}", True, VERDE)
            text_rect = life_stolen_text.get_rect(center=(tile_center_x, sprite_draw_y - 20))
            display.blit(life_stolen_text, text_rect)

        # Exibe a regeneração (se houver)
        if self.regeneration_display_time > 0:
            regeneration_text = self.font.render(f"+{self.regeneration}", True, VERDE)
            text_rect = regeneration_text.get_rect(center=(tile_center_x, sprite_draw_y - 20))
            display.blit(regeneration_text, text_rect)

def attack(attacker, defender, coor_pedras):
    # Toca o som de ataque da classe do atacante
    SOUNDS[attacker.class_name].play()
    
    # Verifica se o ataque está alinhado (horizontal ou vertical)
    align = (attacker.grid_x == defender.grid_x or attacker.grid_y == defender.grid_y)
    if abs(attacker.grid_x - defender.grid_x) <= attacker.attack_range and abs(attacker.grid_y - defender.grid_y) <= attacker.attack_range and abs(attacker.grid_x - defender.grid_x) + abs(attacker.grid_y - defender.grid_y) >= attacker.min_attack_range and align:
        # Verifica se há pedras bloqueando o caminho do ataque
        blocked = False
        if attacker.grid_x == defender.grid_x:
            # Ataque vertical: verifica as células entre o atacante e o defensor
            start = min(attacker.grid_y, defender.grid_y) + 1
            end = max(attacker.grid_y, defender.grid_y)
            for y in range(start, end):
                if (attacker.grid_x, y) in coor_pedras:
                    blocked = True
                    break
        elif attacker.grid_y == defender.grid_y:
            # Ataque horizontal: verifica as células entre o atacante e o defensor
            start = min(attacker.grid_x, defender.grid_x) + 1
            end = max(attacker.grid_x, defender.grid_x)
            for x in range(start, end):
                if (x, attacker.grid_y) in coor_pedras:
                    blocked = True
                    break

        if blocked:
            # Se houver uma pedra no caminho, o ataque é bloqueado
            return

        # Processa o ataque (reduz a vida do defensor)
        damage = attacker.attack_damage
        defender.health -= damage
        defender.last_damage = damage
        defender.damage_display_time = 2000  # Exibe o dano por 2 segundos

        attacker.apply_lifesteal(damage)  # Aplica o lifesteal

        if defender.health < 0:
            defender.health = 0  # Garante que a vida não seja negativa

        # Aplica o knockback ao oponente
        delta_x = defender.grid_x - attacker.grid_x
        delta_y = defender.grid_y - attacker.grid_y

        knockback_x = 1 if delta_x > 0 else (-1 if delta_x < 0 else 0)
        knockback_y = 1 if delta_y > 0 else (-1 if delta_y < 0 else 0)
        new_x = defender.grid_x + knockback_x
        new_y = defender.grid_y + knockback_y

        # Verifica se a nova posição do knockback é válida
        if 0 <= new_x < SIZE_X and 0 <= new_y < SIZE_Y and not ((new_x, new_y) in coor_pedras):
            if (new_x, new_y) != (attacker.grid_x, attacker.grid_y):
                defender.grid_x = new_x
                defender.grid_y = new_y
                defender.dest_grid_x = new_x
                defender.dest_grid_y = new_y
                defender.pixel_x = new_x * TILE_SIZE * SCALE
                defender.pixel_y = new_y * TILE_SIZE * SCALE
                defender.moving = False