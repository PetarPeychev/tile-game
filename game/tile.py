import pygame
from colors import *
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,
                                    TILESIZE))
        if type == 1:
            self.image.fill(LIGHTGRAY)
        else:
            self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft = (x, y))
