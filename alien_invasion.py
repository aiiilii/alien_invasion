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
            # Update aliens moving left or right and down
            self._update_aliens()
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

        # Check for any bullets that have hit aliens.
        #  If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy exiting bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    
    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()


    def _create_fleet(self):
        """
        Create a fleet of alients.
        """
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height= alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for alien_number in range(number_aliens_x):
            for row_number in range(number_rows):
                self._create_alien(alien_number, row_number)

    
    def _create_alien(self, alien_number, row_number):
        # Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height= alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """
        Respond appropriately if any aliens have reached an edge.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """
        Drop the entire fleet and chane the fleet's direction.
        """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    
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