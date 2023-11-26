import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initializes the ship sprite and places it in the starting position"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #Load the ship image and generates a hurtbox
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_space = screen.get_rect()
        
        #Sets the initial position of ship on the bottom
        self.rect.centerx = self.screen_space.centerx
        self.rect.bottom = self.screen_space.bottom
        
        #Stores a decimal value for the ship's centre
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        
        #Movement Flag
        self.moving_right = False
        self.moving_left = False
        # self.moving_up = False
        # self.moving_down = False
        
    def update(self):
        """Update the ship's position based on movement flag"""
        #Update's the ship's center value, not the hitbox
        if self.moving_right and self.rect.right < self.screen_space.right:
            self.centerx += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor

        # if self.moving_up and self.rect.top > 0:
        #     self.centery -= self.ai_settings.ship_speed_factor

        # if self.moving_down and self.rect.bottom < self.screen_space.bottom:
        #     self.centery += self.ai_settings.ship_speed_factor
            
        #Updates the hitbox to where the ship sprite is
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        
    def blitship(self):
        """Draws the ship on the screen"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_space.centerx
        