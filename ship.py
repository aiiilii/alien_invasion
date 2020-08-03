import pygame

class Ship:
    """
    A class to manage the ship.
    """

    def __init__(self, ai_game):
        """
        Initialize the ship and set its starting position.
        :type ai_game: AlienInvasion
        """
        # Get the screen from AlienInvasion instance
        self.screen = ai_game.screen
        # Access the screen's rect attribute using get_rect()
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        # make ship.rect.midbottom = screen_rect.midbottom
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """
        Draw the ship at its current location.
        """
        self.screen.blit(self.image, self.rect)