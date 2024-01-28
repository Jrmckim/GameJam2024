import numpy as np
import pygame
from pygame import mixer
from time import sleep
import random
import math

mixer.init()
pygame.init()


dis = pygame.display.set_mode((800, 600))
pygame.display.update()
pygame.display.set_caption("Tag")
game_over = False

#Music
mixer.music.load("10_Second_round.mp3")
lava_texture = pygame.image.load('lava.gif')
mixer.music.set_volume(0.2)


# colours
barrier_color = (255, 121, 11) 
blue = (0, 0, 255)
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255,255,0)

fps = 30
# starting position and display

disx = 800
disy = 600
dis = pygame.display.set_mode((disx, disy))

def getrandx(sizex):
    return (random.randint(0,disx-sizex))
def getrandy(sizey):
    return (random.randint(0,disy-sizey))

def procedural_map_generation():
        # Define the barriers
    # Define the size of the grid cells
    cell_size = 20  # Adjust this value as needed
    # Define the size of the grid
    grid_width = disx // cell_size
    grid_height = disy // cell_size
    # Initialize the grid with random values (0 = floor, 1 = wall)
    cells = np.random.choice([0, 1], size=(grid_height, grid_width), p=[0.7, 0.3])
    # Define the update function
    def update(cells):
        temp = np.zeros((cells.shape[0], cells.shape[1]))
        for row, col in np.ndindex(cells.shape):
            walls = np.sum(cells[max(0, row - 1):min(row + 2, grid_height), max(0, col - 1):min(col + 2, grid_width)]) - cells[row, col]
            if walls > 3:  # Lowered threshold
                temp[row, col] = 1
        return temp
    # Apply the update function multiple times to generate the final map
    for _ in range(5):
        cells = update(cells)

    # Create the barriers
    barriers = []
    for row, col in np.ndindex(cells.shape):
        if cells[row, col] == 1:
            x = col * cell_size
            y = row * cell_size
            width = cell_size
            height = cell_size
            barriers.append({'x': x, 'y': y, 'width': width, 'height': height})
    return barriers

barriers = procedural_map_generation()

def is_inside_any_barrier(x, y, sizex, sizey, barriers):
    for barrier in barriers:
        if (x + sizex > barrier['x'] and x < barrier['x'] + barrier['width']) and (y + sizey > barrier['y'] and y < barrier['y'] + barrier['height']):
            return True
    return False


def check_x(x,y, sizex, sizey,ability:bool = False):
    if (x + sizex > disx):
        return False
    if (x < 0):
        return False
    if ability:
        for barrier in barriers:
            if pygame.Rect(x, y, sizex, sizey).colliderect(pygame.Rect(barrier['x'], barrier['y'], barrier['width'], barrier['height'])):
                return False
    return True

def check_y(x,y, sizex, sizey, ability:bool = False):
    if (y + sizey > disy):
        return False
    if (y < 50):
        return False
    if ability:
        for barrier in barriers:
            if pygame.Rect(x, y, sizex, sizey).colliderect(pygame.Rect(barrier['x'], barrier['y'], barrier['width'], barrier['height'])):
                return False
    return True

def getValidRand_X(sizex, sizey, opponent_x=0, opponent_y=0):  
    randX = getrandx(sizex)
    randY = getrandy(sizey)  # Generate a random y-coordinate
    while (randX + sizex > disx) or (randX < 0) or (randX < 50) or (abs(randX - opponent_x) < 150) or is_inside_any_barrier(randX, randY, sizex, sizey, barriers):
        randX = getrandx(sizex)
        randY = getrandy(sizey) 
    if not check_x(randX,randY,sizex, sizey) or not check_y(randX,randY,sizex, sizey) or randY < 250:
        return getValidRand_X()# Generate a new y-coordinate if the previous one was inside a barrier
    return randX, randY  # Return both x and y coordinates

def getValidRand_Y(sizey, sizex, opponent_y=0, opponent_x=0):  
    randY = getrandy(sizey)
    randX = getrandx(sizex)  # Generate a random x-coordinate
    while (randY + sizey > disy) or (randY < 100) or (abs(randY - opponent_y) < 150) or is_inside_any_barrier(randX, randY, sizex, sizey, barriers):
        randY = getrandy(sizey)
        randX = getrandx(sizex)  
    if not check_x(randX,randY,sizex, sizey) or not check_y(randX,randY,sizex, sizey) or randY < 250:
        return getValidRand_X()# Generate a new x-coordinate if the previous one was inside a barrier
    return randX, randY  # Return both x and y coordinates

p1sizex = 30
p1sizey = 30
p1speed = 8.5
p1score = 0
p1jump = 1
p1ability = 1
p1abilitytimer = 0
p1abilitymaxsizex = 70
p1abilitymaxsizey = 70
growth = 4
x1, y1 = getValidRand_X(p1sizex, p1sizey)
ability = False
shrinking = False
p1Heat = 0

p2sizex = 30
p2sizey = 30
p2speed = 7
p2speed_temp = 7
p2score = 0
p2jump = 1
p2ability = 1
x2, y2 = getValidRand_X(p1sizex, p1sizey,x1,y1)
p2Heat = 0

circleActive = True
overheatDelay = 0

clock = pygame.time.Clock()
timer = 10
font = pygame.font.Font('freesansbold.ttf', 32)

def message (msg,colour,x,y):
    mesg = font.render(msg, True, colour)
    dis.blit(mesg, [x, y])

def home_screen():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tag - Home Screen")

    font = pygame.font.Font('freesansbold.ttf', 32)
    white = (255, 255, 255)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    text = font.render("Press S to Start or Esc to Exit", True, white)
    text_rect = text.get_rect(center=(400, 300))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()

        screen.fill(black)
        screen.blit(text, text_rect)
        pygame.display.flip()

def character_select():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Tag - Character Select")

    player1_ability = "None"
    player2_ability = "None"

    while player1_ability == "None" or player2_ability == "None":

        text = font.render("Character Select (s to continue)", True, white)
        text_rect = text.get_rect(center=(400, 100))

        instructions_1 = font.render("Player 1: Press '1' for Get Large ability", True, white)
        instructions_1_rect = instructions_1.get_rect(center=(400, 200))

        instructions_2 = font.render("Player 2: Press '2' for Teleport ability", True, white)
        instructions_2_rect = instructions_2.get_rect(center=(400, 300))

        Player_1_ability_displayed = font.render("Player 1 Ability: " + player1_ability, True, white)
        Player_1_ability_displayed_rect = Player_1_ability_displayed.get_rect(center=(400, 400))

        Player_2_ability_displayed = font.render("Player 2 Ability: " + player2_ability, True, white)
        Player_2_ability_displayed_rect = Player_2_ability_displayed.get_rect(center=(400, 500))

        screen.fill(black)
        screen.blit(text, text_rect)
        screen.blit(instructions_1, instructions_1_rect)
        screen.blit(instructions_2, instructions_2_rect)
        screen.blit(Player_1_ability_displayed, Player_1_ability_displayed_rect)
        screen.blit(Player_2_ability_displayed, Player_2_ability_displayed_rect)

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player1_ability = "Get Large"
                elif event.key == pygame.K_2:
                    player1_ability = "Teleport"
                elif event.key == pygame.K_3:
                    player2_ability = "Get Large"
                elif event.key == pygame.K_4:
                    player2_ability = "Teleport"

    return player1_ability, player2_ability

# Run the home screen
home_screen()

# Run the character select screen
player1_ability, player2_ability = character_select()

mixer.music.play()
while check_x(x1, y1, p1sizex, p1sizey, p1ability) == False:
    print("spawan error")
    x1,y1 = getValidRand_X(p1sizex, p1sizey,x2,y2)
while check_y(x1, y1, p1sizex, p1sizey,p1ability) == False:
    print("spawan error")
    x1,y1 = getValidRand_X(p1sizex, p1sizey,x2,y2)
while check_x(x2, y2, p2sizex, p2sizey, p2ability) == False:
    print("spawan error")
    x2,y2 = getValidRand_X(p1sizex, p1sizey,x1,y1)
while check_y(x2, y2, p2sizex, p2sizey, p2ability) == False:
    print("spawan error")
    x2,y2 = getValidRand_X(p1sizex, p1sizey,x1,y1)

while not game_over:
    # p2speed = 8
    # Closes window if you press the X button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    sleep(1/fps)
    keys = pygame.key.get_pressed()
#Abilities
    if keys[pygame.K_LSHIFT] and p2ability > 0:
        p2speed_temp = p2speed
        p2speed = 300
        p2ability -= 1
    else:
        p2speed = p2speed_temp
    if keys[pygame.K_SPACE] and p1ability > 0:
        ability = True
        p1abilitytimer = 2
        p1ability -= 1
# Player 1 movement
    if keys[pygame.K_w]:
        new_y1 = y1 - p1speed
        if check_y(x1, new_y1, p1sizex, p1sizey,p1ability):
            y1 = new_y1
    if keys[pygame.K_s]:
        new_y1 = y1 + p1speed
        if check_y(x1, new_y1, p1sizex, p1sizey,p1ability):
            y1 = new_y1
    if keys[pygame.K_a]:
        new_x1 = x1 - p1speed
        if check_x(new_x1, y1, p1sizex, p1sizey,p1ability):
            x1 = new_x1
    if keys[pygame.K_d]:
        new_x1 = x1 + p1speed
        if check_x(new_x1, y1, p1sizex, p1sizey,p1ability):
            x1 = new_x1

    # Player 2 movement
    if keys[pygame.K_UP]:
        new_y2 = y2 - p2speed
        if check_y(x2, new_y2, p2sizex, p2sizey,p1ability):
            y2 = new_y2
    if keys[pygame.K_DOWN]:
        new_y2 = y2 + p2speed
        if check_y(x2, new_y2, p2sizex, p2sizey,p1ability):
            y2 = new_y2
    if keys[pygame.K_LEFT]:
        new_x2 = x2 - p2speed
        if check_x(new_x2, y2, p2sizex, p2sizey,p1ability):
            x2 = new_x2
    if keys[pygame.K_RIGHT]:
        new_x2 = x2 + p2speed
        if check_x(new_x2, y2, p2sizex, p2sizey,p1ability):
            x2 = new_x2


#PLAYER 1 ABILITY
    if p1sizex <= p1abilitymaxsizex and p1sizey <= p1abilitymaxsizey and ability == True:
        p1abilitytimer -= (1/fps)
        if shrinking == False:
            p1sizex += growth
            p1sizey += growth
            x1 -= growth/2
            y1 -= growth/2
        if p1sizex > p1abilitymaxsizex and p1sizey > p1abilitymaxsizey:
            x1 += (p1sizex - 70)/2
            y1 += (p1sizey - 70)/2
            p1sizex = p1abilitymaxsizex
            p1sizey = p1abilitymaxsizey
            shrinking = True
        if p1abilitytimer <= 0:
            p1sizex -= growth
            p1sizey -= growth
            x1 += growth/2
            y1 += growth/2
        if p1sizex <= 30 and p1sizey <= 30:
            p1sizex = 30
            p1sizey = 30
            ability = False
            shrinking = False
    dis.fill(black)
    message(str(round(timer,1)), white, disx/2, 10)
    message(f"P1 : {p1score}", red, 10, 10)
    message(f"P2 : {p2score}", blue, disx-100, 10)
    
    pygame.draw.rect(dis, blue, [x2, y2, p2sizex, p2sizey])
    pygame.draw.rect(dis, red, [x1, y1, p1sizex, p1sizey])
    # Draw Player 1 and Player 2
    pygame.draw.rect(dis, blue, [x2, y2, p2sizex, p2sizey])
    pygame.draw.rect(dis, red, [x1, y1, p1sizex, p1sizey])
    
    for barrier in barriers:
        # print(barrier)
        scaled_lava_texture = pygame.transform.scale(lava_texture, (barrier['width'], barrier['height']))
        # Draw the scaled lava texture onto the barrier
        # dis.blit(scaled_lava_texture, (barrier['x'], barrier['y']))
        pygame.draw.rect(dis, barrier_color, [barrier['x'], barrier['y'], barrier['width'], barrier['height']])


    # Define progress bar properties
    bar_width = 200
    bar_height = 15
    bar_y = 50
    bar_background_color = (255, 255, 255)  # White
    border_width = bar_width + 3  # Add 4 pixels to the width
    border_height = bar_height + 3  # Add 4 pixels to the height
    border_color = (252, 235, 120)  
    
    # player1
    bar_color1 = (220, 20, 60) if p1Heat>2 else  (255, 127, 80) if p1Heat>1 else (255, 226, 6)
    bar_x1 = 10
    progress1 = p1Heat/3  
    border_x1 = bar_x1 - 2  # Subtract 2 pixels from the x position
    border_y1 = bar_y - 2  # Subtract 2 pixels from the y position

    # player2
    bar_color2 = (220, 20, 60) if p2Heat>2 else  (255, 127, 80) if p2Heat>1 else (255, 226, 6)
    bar_x2 = disx-210
    progress2 = p2Heat/3 
    border_x2 = bar_x2 - 2  # Subtract 2 pixels from the x position
    border_y = bar_y - 2  # Subtract 2 pixels from the y position

    # Draw bar11
    pygame.draw.rect(dis, border_color, [border_x1, border_y, border_width, border_height])
    pygame.draw.rect(dis, bar_background_color, [bar_x1, bar_y, bar_width, bar_height])
    pygame.draw.rect(dis, bar_color1, [bar_x1, bar_y, bar_width * progress1, bar_height])

    # Draw bar2
    pygame.draw.rect(dis, border_color, [border_x2, border_y, border_width, border_height])
    pygame.draw.rect(dis, bar_background_color, [bar_x2, bar_y, bar_width, bar_height])
    pygame.draw.rect(dis, bar_color2, [bar_x2, bar_y, bar_width * progress2, bar_height])

    # Define circle properties
    circle_radius = 20
    circle_x = disx // 2
    circle_y = disy // 2
    circle_color = yellow  # Define green color at the top of your script

    # Speed boost properties
    speed_boost_duration = 5  # 5 seconds
    p1_speed_boost_timer = 0
    p2_speed_boost_timer = 0

    # Draw the circle at the center of the map
    if circleActive == True: pygame.draw.circle(dis, circle_color, (circle_x, circle_y), circle_radius)

    # Check if Player 1 reaches the circle
    if ((x1 - circle_x)**2 + (y1 - circle_y)**2 <= circle_radius**2) and circleActive == True:
        circleActive = False
        print("Player 1 reached the circle")
        p1_speed_boost_timer = speed_boost_duration
        p1Heat += 1

    # Check if Player 2 reaches the circle
    if ((x2 - circle_x)**2 + (y2 - circle_y)**2 <= circle_radius**2) and circleActive == True:
        circleActive = False
        print("Player 2 reached the circle")
        p2_speed_boost_timer = speed_boost_duration
        p2Heat += 1

    # Update player speed if they have a speed boost
    if p1_speed_boost_timer > 0:
        p1speed *= 2  # Double the speed
        p1_speed_boost_timer -= 1/fps

    if p2_speed_boost_timer > 0:
        p2speed *= 2  # Double the speed
        p2speed_temp *= 2
        p2_speed_boost_timer -= 1/fps

    # Update the display
    # pygame.display.update()
    pygame.display.update()
    timer -= 1/fps
#Player 2 Win condition
    if timer < 0:
        mixer.music.pause()
        sleep(1)
        p2score += 1
        p2ability = 1
        p1ability = 1
        timer = 10
        mixer.music.play()
        x1 = getrandx(p1sizex)
        y1 = getrandy(p1sizey)
        x2 = getrandx(p2sizex)
        y2 = getrandy(p2sizey)
        p1sizex = 30
        p1sizey = 30
        ability = False
        shrinking = False
        circleActive = True
        p1abilitytimer = 0
        p1speed = 8.5
        p2speed = 7
        p2speed_temp = 7
        barriers = procedural_map_generation()
#Player 1 Win condition
    if (x1 + p1sizex > x2) and (x1 - p2sizex < x2) and (y1 + p1sizey > y2) and (y1 - p2sizey < y2):
        mixer.music.pause()
        sleep(1)
        x1 = getrandx(p1sizex)
        y1 = getrandy(p1sizey)
        x2 = getrandx(p2sizex)
        y2 = getrandy(p2sizey)
        p1score += 1
        timer = 10
        mixer.music.play()
        p1ability = 1
        p2ability = 1
        p1abilitytimer = 0
        p1sizex = 30
        p1sizey = 30
        ability = False
        shrinking = False
        circleActive = True
        p1speed = 8.5
        p2speed_temp = 7
        p2speed = 7
        barriers = procedural_map_generation()

#Updates player scores

    if p1score == 5 or p2Heat == 3:
        mixer.music.pause()
        if p2Heat == 3 and overheatDelay <1:
            overheatDelay += 1/fps
            continue
        dis.fill(black)
        message("PLAYER 1 WINS", red, disx / 3, disy / 2.5)
        message(f"P1 : {p1score}", red, 10, 10)
        message(f"P2 : {p2score}", blue, disx - 100, 10)
        pygame.display.update()
        sleep(2)
        game_over = True
    if p2score == 5 or p1Heat == 3:
        mixer.music.pause()
        if p1Heat == 3 and overheatDelay <1:
            overheatDelay += 1/fps
            continue
        dis.fill(black)
        message("PLAYER 2 WINS", blue, disx // 3, disy // 2.5)
        pygame.display.update()
        message(f"P1 : {p1score}", red, 10, 10)
        message(f"P2 : {p2score}", blue, disx - 100, 10)
        pygame.display.update()
        sleep(3)
        game_over = True

pygame.quit()
quit()
