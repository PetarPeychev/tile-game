import pygame, settings, colors

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((settings.TILESIZE * 2,
                                    settings.TILESIZE * 3))
        self.image.fill(colors.GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x * settings.TILESIZE
        self.rect.y = self.y * settings.TILESIZE
