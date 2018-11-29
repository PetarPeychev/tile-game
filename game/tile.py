import pygame
from colors import *
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, isWall):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,
                                    TILESIZE))
        if isWall:
            self.image.fill(GRAY)
        else:
            self.image.fill(BROWN)
        self.rect = self.image.get_rect(topleft = (x, y))
