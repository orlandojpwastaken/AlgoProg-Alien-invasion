import sys

import pygame

from pygame.sprite import Group

from settings import Settings

from game_stats import GameStats

from scoreboard import Scoreboard

from button import Button

from ship import Ship

from alien import Alien

import game_functions as gf

def run_game():
    #Initializes the game and generates a screen for the game's GUI, initializes settings as well
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #Makes the Play Button
    play_button = Button(ai_settings, screen, "Play")
    
    #Creating an instance to store game statistics
    stats = GameStats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)

    #Makes a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    
    #Makes the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
#Starts the main loop of the game
    while True:
        gf.check_events(ai_settings, screen, stats, scoreboard,
                        play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, scoreboard, 
                                  ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, scoreboard,
                                ship, aliens, bullets)
        gf.screen_update(ai_settings, screen, stats, scoreboard, ship, aliens, bullets,
                         play_button)
        
run_game()
