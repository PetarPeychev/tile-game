import pygame, settings

class Camera:
    def __init__(self, map_width, map_height):
        self.camera = pygame.Rect(0, 0, map_width, map_height)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        return entity.rect.move(self.camera.topLeft)

    def update(self, target):
        x = -target.rect.x + int(settings.DISPLAY_WIDTH / 2)
        y = -target.rect.y + int(settings.DISPLAY_HEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.map_width, self.map_height)
