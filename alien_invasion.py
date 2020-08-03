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
            # Ship's position is updated after we've checked for keyboard events and before we update the screen.
            self.ship.update()
            self.__update_screen()


    def _check_events(self):
        """
        Respond to keypresses and mouse events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)


    def _check_keydown_event(self, event):
        """
        Respong to keypresses.
        :type event: pygame.event
        """
        if event.key == pygame.K_RIGHT:
            # Set move the ship to the right to True.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Set move the ship to the left to True.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()


    def _check_keyup_event(self, event):
        """
        Respong to releases.
        :type event: pygame.event
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    
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