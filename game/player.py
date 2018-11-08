import pygame, settings, colors

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((settings.TILESIZE * 2,
                                    settings.TILESIZE * 3))
        self.image.fill(colors.GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 0, 0

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -settings.PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = settings.PLAYER_SPEED

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def update(self):
        self.get_keys()
        self.rect.x += self.vx * self.game.dt
        self.rect.y = self.y
