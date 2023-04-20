import pygame

from models import Player, Tile
from settings import *


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.obstacles_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.tile = Tile
        self.create_map()

    @staticmethod
    def get_position(x, y):
        return x * TILESIZE, y * TILESIZE

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, column in enumerate(row):
                x, y = self.get_position(x=col_index, y=row_index)

                if column == 'x':
                    Tile(pos=(x, y), groups=(self.visible_sprites, self.obstacles_sprites))

                if column == 'p':
                    Player(pos=(x, y), groups=(self.visible_sprites,), obstacle_sprites=self.obstacles_sprites)

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
