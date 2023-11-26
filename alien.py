import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class for a single alien"""
    
    def __init__(self, ai_settings, screen):
        """Initializes the alien class and spawns it in its startingg position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        #Loads the image of the alien and enerates a hurtbox
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()
        
        #Places every new alien at the top of the the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Stores the position of the alien as a float.
        self.x = float(self.rect.x)
    
    def blitalien(self):
        """Draws the ship on the screen"""
        self.screen.blit(self.image, self.rect)
        
    def check_edges(self):
        """Return True if alien is at the edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    
    def update(self):
        """Moves the alien right"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
        
