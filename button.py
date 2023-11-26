import pygame.font

class Button():
    
    def __init__(self, ai_settings, screen, msg):
        """Initializes button atrtributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        #Sets the dimensions and other properties of the button
        self.width, self.height = 200,50
        self.button_color = (127, 127, 127)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Draws the button rectangle and centers it on the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #Prepping the button's message
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turns the msg into a rendered image and centers it to the button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """Draws a blank button and then draws a message on it"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        