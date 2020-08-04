import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

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
        # Using the following commented code if want full screen mode
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        # Storing bullets in a group
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()


    def run_game(self):
        """
        Start the main loop for the game.
        """
        while True:
            # Event loop to watch for keyboard and mouse events
            self._check_events()
            # Ship's position is updated after we've checked for keyboard events and before we update the screen.
            self.ship.update()
            # Update bullets
            self._update_bullets()
            # Update the whole pygame screen
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
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_event(self, event):
        """
        Respong to releases.
        :type event: pygame.event
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """
        Create a new bullet and add it to the bullets group.
        """
        # Limite player to bullets_allowed number of bullets at a time.
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """
        Update position of bullets and get rid of old bullets.
        """
        # Update each of the position of the bullets, using sprite
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))


    def _create_fleet(self):
        """
        Create a fleet of alients.
        """
        # Make an alien.
        alien = Alien(self)
        self.aliens.add(alien)

    
    def __update_screen(self):
        """
        Update images on the screen, and flip to the new screen.
        """
        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        # Continuously updates the display to show the new positions of game elements
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()