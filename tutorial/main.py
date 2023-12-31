import pygame
from sys import exit
from random import randint

def display_score(): # use pygame.time.get_ticks() to get miliseconds passed since start of program
    # integer division by 1000 since we don't want miliseconds
    # global current_time
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    # or int((pygame.time.... - start_time) / 1000)
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    print(current_time)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:   # ensure list isn't empty
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            # draw fly/snail based on bottom position
            if obstacle_rect.bottom == 300:
                # we can draw multiple rectangles from the same surface
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        
        # only keep existing rectangles if they have not passed the player (& frmae)
        # rest are deleted
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        
        return obstacle_list
    else: return [] # return empty list to prevent having None.append()

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

pygame.init() 
screen = pygame.display.set_mode((800, 400))                            
pygame.display.set_caption('paigaim')
clock = pygame.time.Clock()                                             

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

''' SURFACES '''
sky_surface = pygame.image.load('graphics/Sky.png').convert()           
ground_surface = pygame.image.load('graphics/ground.png').convert()     

# score_surf = test_font.render('My Game', False, (64, 64, 64))   # rgb tuple for the color
# score_rect = score_surf.get_rect(center = (400, 50))

# Obstacles
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# player stand surface, reassigned to overwrite the initial surface by re-scaling it
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
# player_stand = pygame.transform.scale(player_stand, (200, 400))  # scaling the surface to make it bigger
# player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) # arguments are surface, angle, scale -- also Rotozoom filters the picture to make it better
player_stand_rect = player_stand.get_rect(center = (400, 200))


game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 340))

# Timer
obstacle_timer = pygame.USEREVENT + 1   # add 1 to skip pygame's own events
pygame.time.set_timer(obstacle_timer, 1500)  # event, time (in milliseconds)

'''MAIN GAME LOOP'''
while True:
    # if any events happened since the prev. frame check them
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:      
            pygame.quit()                   
            exit()   
        # event loop checking for mouse & keyboard input  
        # note: checking for mousemotion is more efficient than checking for a collision   
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # only jumping if the player is on/below the ground
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: # note: using and might make it more difficult for the input to register for some reason
                    player_gravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300: 
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True      
                # above not enough to work because we have to keep spacing until the player and enemy do not collide
                # snail_rect.left = 800    
                # update start time so that score re-starts from 0 when we restart the game
                start_time = pygame.time.get_ticks() 
        if event.type == obstacle_timer and game_active:
            # snail spawns to the right of the screen (outside) and we move it in
            if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100), 300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100), 210)))
            
    '''GAME'''
    if game_active:
        # drawing sky & ground
        screen.blit(sky_surface, (0,0))             
        screen.blit(ground_surface, (0,300))
        
        # drawing outline for score text
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)

        # update score every time so that we can show it in the start/death screen
        score = display_score()

        # managing the snail's movements
        # snail_rect.x -= 4                      # x, y coordinates of rectangles can be accessed                 
        # if snail_rect.right <= 0:   snail_rect.left = 800   
        # screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)
        
        # Obstalce movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision 
        game_active = collisions(player_rect, obstacle_rect_list)
        # if snail_rect.colliderect(player_rect):
        #     screen.fill((94, 129, 162))
        #     game_active = False
            
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        
        # need to clear it because if player is colliding with a snail then the game will crash if we try to restart because they're still colliding
        obstacle_rect_list.clear()

        # resetting player info
        player_rect.midbottom = (80,300)    # in case player was left in the sky
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 330))

        screen.blit(game_name, game_name_rect)

        # only display score if we've played at least once
        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()                                                         
    clock.tick(60)                          
