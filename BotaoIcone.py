import pygame
import random


class World():
    def __init__(self, x, y, tilepack, tilesize, display, scale):
        self.mapa = []
        self.tilesize = tilesize
        self.display = display
        self.scale = scale
        for i in range(y):
            linha = []
            for j in range(x):
                tile = random.choice(tilepack)
                pygame.transform.scale_by(tile, self.scale)
                linha.append(tile)
            self.mapa.append(linha)

    def draw_map(self):
        while True:
            for y, row in enumerate(self.mapa):
                for x, tile in enumerate(row):
                    pos_x = x * self.tilesize * self.scale
                    pos_y = y * self.tilesize * self.scale
                    self.display.blit(tile, (pos_x, pos_y))

