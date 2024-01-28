import pygame
from pygame import mixer
from time import sleep
import random

mixer.init()
pygame.init()


dis = pygame.display.set_mode((800, 600))
pygame.display.update()
pygame.display.set_caption("Tag")
game_over = False

#Music
mixer.music.load("10_Second_round.mp3")
mixer.music.set_volume(0.2)


# colours
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

def getValidRand_X(sizex, opponent_x=0):
    randX = getrandx(sizex)
    while (randX + sizex > disx) or (randX < 0) or (randX < 50) or (abs(randX - opponent_x) < 100):
        randX = getrandx(sizex)
    return randX

def getValidRand_Y(sizey, opponent_y=0):
    randY = getrandy(sizey)
    while (randY + sizey > disy) or (randY < 50) or (abs(randY - opponent_y) < 100):
        randY = getrandy(sizey)
    return randY

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
x1 = getValidRand_X(p1sizex)
y1 = getValidRand_Y(p1sizey)
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
x2 = getValidRand_X(p1sizex, x1)
y2 = getValidRand_Y(p1sizey, y1)
p2Heat = 0

circleActive = True
overheatDelay = 0

clock = pygame.time.Clock()
timer = 10
font = pygame.font.Font('freesansbold.ttf', 32)

def check_x(x,psizex):
    if (x + psizex > disx):
        x = disx - psizex
    if (x < 0):
        x = 0
    return x

def check_y(y,psizey):
    if (y + psizey > disy):
        y = disy - psizey
    if (y < 0):
        y = 0
    return y

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
    if keys[pygame.K_LEFT]:
        x1 += -p1speed
        if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            x1 += 0.414 * p1speed
        x1 = check_x(x1, p1sizex)
    if keys[pygame.K_RIGHT]:
        x1 += p1speed
        if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            x1 += 0.414 * -p1speed
        x1 = check_x(x1, p1sizex)
    if keys[pygame.K_UP]:
        y1 += -p1speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            y1 += 0.414 * p1speed
        y1 = check_y(y1, p1sizey)
    if keys[pygame.K_DOWN]:
        y1 += p2speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            y1 += 0.414 * -p1speed
        y1 = check_y(y1, p1sizey)

#PLAYER 2 Movement
    if keys[pygame.K_a]:
        x2 += -p2speed
        if keys[pygame.K_s] or keys[pygame.K_w]:
            x2 += 0.414 * p2speed
        x2 = check_x(x2, p2sizex)
    if keys[pygame.K_d]:
        x2 += p2speed
        if keys[pygame.K_s] or keys[pygame.K_w]:
            x2 += 0.414 * -p2speed
        x2 = check_x(x2, p2sizex)
    if keys[pygame.K_w]:
        y2 += -p2speed
        if keys[pygame.K_d] or keys[pygame.K_a]:
            y2 += 0.414 * p2speed
        y2 = check_y(y2, p2sizey)
    if keys[pygame.K_s]:
        y2 += p2speed
        if keys[pygame.K_d] or keys[pygame.K_a]:
            y2 += 0.414 * -p2speed
        y2 = check_y(y2, p2sizey)

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
