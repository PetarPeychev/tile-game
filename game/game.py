import pygame
from player import Player
from camera import Camera
from settings import *
from colors import *

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
        self.player = Player(self,
                             10 * TILESIZE,
                             20 * TILESIZE)
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

    def draw_grid(self):
        # draw lines on the x axis every TILESIZE pixels
        for x in range(0, DISPLAY_WIDTH, TILESIZE):
            pygame.draw.line(self.screen,
                             LIGHTGRAY,
                             (x, 0),
                             (x, DISPLAY_HEIGHT))

        # draw lines on the y axis every TILESIZE pixels
        for y in range(0, DISPLAY_HEIGHT, TILESIZE):
            pygame.draw.line(self.screen,
                             LIGHTGRAY,
                             (0, y),
                             (DISPLAY_WIDTH, y))

    def draw(self):
        # game loop draw
        self.screen.fill(DARKGRAY)
        self.screen.blit(self.player.image,
                         self.camera.apply(self.player))
        self.draw_grid()
        pygame.display.flip()

    def show_main_menu(self):
        # main game menu
        self.new()
        pass

    def show_splash_screen(self):
        # game splash screen
        pass
