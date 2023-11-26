import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien

def check_keyPress_events(event, ai_settings, screen, stats, ship, aliens, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = True
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, 
                bullets)
    

def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a new bullet if the number of bullets on screen does is less that the maximum number of allowed bullets"""
    #Creates a new bullet and add it to the bullets group upon pressing the spacebar if maximum amount of bullets is not reached.
    if len(bullets) < ai_settings.maximum_bullets:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyRelease_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False  
    # elif event.key == pygame.K_UP:
    #     ship.moving_up = False  
    # elif event.key == pygame.K_DOWN:
    #     ship.moving_down = False

def check_events(ai_settings, screen, stats, scoreboard, play_button,
                 ship, aliens, bullets):
    """Makes it so that the game will respond to user input/keypresses"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keyPress_events(event, ai_settings, screen, stats, ship, aliens,
                                  bullets)
        elif event.type == pygame.KEYUP:
            check_keyRelease_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, scoreboard,
                              play_button, ship, aliens, bullets,
                              mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, scoreboard, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Starts a game when the play button is clicked."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Resets the game's difficulty settings
        ai_settings.initialize_dynamic_settings()
        
        start_game(ai_settings, screen, stats, scoreboard, ship, aliens, 
                bullets)
        

def start_game(ai_settings, screen, stats, scoreboard, ship, aliens, 
                bullets):
        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        
        #Resets the scoreboard images
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()
        
        
        #Emptys the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #Creates a new fleet and centers the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
            
         
def screen_update(ai_settings, screen, stats, scoreboard, ship, aliens, bullets,
                  play_button):
    """Update images on the screen and flip to the new screen"""
    #Redraws screen everytime in passes through the loop
    screen.fill(ai_settings.background_color)
    #Redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitship()
    aliens.draw(screen)
    #Draw the score information
    scoreboard.show_score()

    #Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    #Shows the most recently drawn screen
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, scoreboard, 
                   ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets"""
    #Update bullet position
    bullets.update()
           
    #Deletes bullets that are no longer on screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, 
                                  ship, aliens, bullets)    

def check_bullet_alien_collisions(ai_settings, screen, stats, scoreboard, 
                                  ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    #Check if a bullet hits an alien
    #If so, get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) 
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)
    
    if len(aliens) == 0:
        #Starts a new level upon destroying one fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        
        #Increases the game's difficulty level
        stats.level += 1
        scoreboard.prep_level()

def get_number_aliens_x(ai_settings, alien_width):
    """Performs the calculations necessary to decide how many aliens will be in a single row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Performs the calculations necessary to decide how many rows of aliens will fit in the screen"""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Creates an alien then places it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    
    #Create the fleet of aliens
    for row_number in range (number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)

def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
    
def change_fleet_direction(ai_settings, aliens):
    """Drops the fleet and change's its direction right after."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
            

def ship_hit(ai_settings, screen, stats, scoreboard,
                  ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    
    if stats.ships_left >0:
        #Reduces remaining player lives by 1
        stats.ships_left -= 1
        
        #Updates amount of lives owned
        scoreboard.prep_ships()
    
        #Resets the game state
        #Empties the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
    
        #Creates a new fleet and re-positions the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    
        #Pauses the game temporarily
        sleep(0.5)
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)    

def check_aliens_bottom(ai_settings, screen, stats, scoreboard,
                        ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
def update_aliens(ai_settings, screen, stats, scoreboard,
                  ship, aliens, bullets):
    """
    Checks if the fleet has hit the edge,
        then update the positions of all aliens in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    #Detects when aliens and player's ship collides
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, scoreboard,
                  ship, aliens, bullets)
    #Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, scoreboard,
                  ship, aliens, bullets)

def check_high_score(stats, scoreboard):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()