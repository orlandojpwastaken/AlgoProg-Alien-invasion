import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for bullets fired by the player's ship"""
    def __init__(self, ai_settings, screen, ship):
        """Generates a bullet sprite at where the player is located"""
        super().__init__()
        self.screen = screen

        #Generates a rect which acts as the bullet's hitbox at (0,0) and moves it to the correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                  ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #Stores the position of the bullet as a decimal value, just like the ship
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor
        
    def update(self):
        """Moves the bullet up the screen"""
        #Update the decimal value of the bullet's y position
        self.y -= self.speed_factor
        #Makes the hitbox of the bullet follow the bullet's y position
        self.rect.y = self.y
    
    def draw_bullet(self):
        """Draws the bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        

