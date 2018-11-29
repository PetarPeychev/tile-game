import pygame
from game import Game

# instantiate main game object
game = Game()

# show logo splash screen
game.show_splash_screen()

# show the main menu, which in turn calls the game loop
while game.running:
    game.show_main_menu()

# exit game
pygame.quit()
