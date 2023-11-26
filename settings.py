class Settings():
    """A class storing all the settings for the game"""
    
    def __init__(self):
        """Initialize the game's static settings"""
        # Screen-related settings
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (206, 206, 207)
    
        #Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed_factor = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.maximum_bullets = 2
        
        #Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        #fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        #Determines how fast the game speeds up
        self.speedUp_scale = 1.1
        self.score_multiplier = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializes settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        
        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and score multiplier."""
        self.ship_speed_factor *= self.speedUp_scale
        self.bullet_speed_factor *= self.speedUp_scale
        self.alien_speed_factor *= self.speedUp_scale
        self.alien_points = int(self.alien_points *
                                self.score_multiplier)
        print(self.alien_points)