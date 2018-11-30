import pygame
from player import Player
from camera import Camera
from settings import *
from colors import *
from map import Map
from tile import Tile

class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode(
            (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.map = Map(128, 64)
        self.map.generate()
        self.player = Player(self,
                             self.map.spawn_point[0] * TILESIZE,
                             self.map.spawn_point[1] * TILESIZE)
        self.camera = Camera(4000, 4000)
        self.run()

    def run(self):
        # run game loop
        self.playing = True
        while self.playing:
            # tick clock and store delta time for last frame
            self.dt = self.clock.tick(FPS) / 1000

            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop update
        self.camera.update(self.player)
        self.player.update()
        pass

    def events(self):
        # game loop events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # game loop draw
        self.screen.fill(DARKGRAY)
        for row in range(self.map.height):
            for col in range(self.map.width):
                tile = Tile(self, TILESIZE * col, TILESIZE * row, self.map.array[row][col])
                self.screen.blit(tile.image, self.camera.apply(tile))
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        pygame.display.flip()

    def show_main_menu(self):
        # main game menu
        self.new()
        pass

    def show_splash_screen(self):
        self.clock.tick(FPS)
        self.screen.fill(LIGHTGRAY)
        self.draw_text(TITLE, 128, y = DISPLAY_HEIGHT / 4)
        self.draw_text("Press Any Key to Start", 48, x = DISPLAY_WIDTH * 0.05, y = DISPLAY_HEIGHT * 7 / 8)
        pygame.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, x = None, y = (DISPLAY_HEIGHT / 4)):
        f = pygame.font.Font("fonts/SF_Archery_Black.ttf", size)
        surf = f.render(text, True, BLACK)
        if not x:
            x = DISPLAY_WIDTH / 2 - surf.get_width() / 2
        self.screen.blit(surf, (x, y))

    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
