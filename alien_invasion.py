import sys

import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """
    Overall class to manage game assets and behavior.
    """

    def __init__(self):
        """
        Initialize the game, and create game resources
        """
        pygame.init()
        self.settings = Settings()

        # Create display window using a tuple
        # assign this display window to self.screen, so it is available in all methods in the class
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)


    def run_game(self):
        """
        Start the main loop for the game.
        """
        while True:
            # Event loop to watch for keyboard and mouse events
            self._check_events()
            self.__update_screen()


    def _check_events(self):
        """
        Respond to keypresses and mouse events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    
    def __update_screen(self):
        """
        Update images on the screen, and flip to the new screen.
        """
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()

        # Make the most recently drawn screen visible
        # Continuously updates the display to show the new positions of game elements
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()