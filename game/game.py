import pygame, settings, colors

class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode(
            (settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.run()

    def run(self):
        # run game loop
        self.playing = True
        while self.playing:
            # tick clock and store delta time for last frame
            self.dt = self.clock.tick(settings.FPS)

            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop update
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
        for x in range(0, settings.DISPLAY_WIDTH, settings.TILESIZE):
            pygame.draw.line(self.screen,
                             colors.LIGHTGRAY,
                             (x, 0),
                             (x, settings.DISPLAY_HEIGHT))

        # draw lines on the y axis every TILESIZE pixels
        for y in range(0, settings.DISPLAY_HEIGHT, settings.TILESIZE):
            pygame.draw.line(self.screen,
                             colors.LIGHTGRAY,
                             (0, y),
                             (settings.DISPLAY_WIDTH, y))

    def draw(self):
        # game loop draw
        self.screen.fill(colors.DARKGRAY)
        self.draw_grid()
        pygame.display.flip()

    def show_main_menu(self):
        # main game menu
        self.new()
        pass

    def show_splash_screen(self):
        # game splash screen
        pass
