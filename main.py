# new_importing libraries
import random
import pygame
import math

from pygame import mixer

#initializing the module
pygame.init()
#new_creating screen here we can change the width and heoighht of screen this values are in pixels
#creating the screen
screen = pygame.display.set_mode((1600, 900))

#Sound effect
mixer.music.load("background.wav")
#new_(-1) is playing tyhe sound infinite times
mixer.music.play(-1)

# Score
#new_we can change lives,font size,and initial score value,here freesansbold ,ttf is font style and 32 is font size
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
lives = 3
font = pygame.font.Font('freesansbold.ttf', 32)



#new_textx and texty denotes distance of score and lives (font) text from X and Y respectively
textX = 10
testY = 10

# new initialising text of game over entirely difined three variables
# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 128)
below_font = pygame.font.Font('freesansbold.ttf', 32)
esc_font = pygame.font.Font('freesansbold.ttf', 16)

#title of the game and icon of the game and background
#display title of game and background image
pygame.display.set_caption("Warplane Game")
icon = pygame.image.load("./title_icon.png")
pygame.display.set_icon(icon)
background = pygame.image.load("./background-2.png")

#player details
#new_here player X and player Y are initial distance distance when game start(matlab screen ke biche mein dikahna player ko) half of screen size is cordinate

player_img = pygame.image.load("space-ship.png")
playerX = 775
playerY = 800
playerX_change = 0
playerY_change = 0

#ufo details
#new_loading image of alliens
aliens = []
ufo_img = pygame.image.load("ufo.png")

#bullet details
bullet_img = pygame.image.load("bullet.png")
bomb_img = pygame.image.load("bomb.png")

#bullets
#intial player and aliens have zero bullets and zero bombs thats why array is zero
bullets = []
all_fired_bullets = []
bombs = []
all_fired_bombs = []

#**************        ALL FUNCTIONS      **********************************


# new_the role of the function is to show the image of the player on the screen and position
def show_player(x, y):
    screen.blit(player_img, (x, y))

# new_showing the position of ufo
def show_ufo(x, y):
    screen.blit(ufo_img, (x, y))

#new_this funtion is callled when game gets over
def game_over_text():
   #new_global variables cannot be changed inside functions to use global variable inside the function we use syntax word global we earlier use this 3 word
    global over_font
    global below_font
    global esc_font
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    below_text = below_font.render("press 'ENTER' to play the game again",
                                   True, (255, 255, 255))
    esc_text = esc_font.render("PRESS ANY KEY TO ESCAPE", True,
                               (255, 255, 255))
    screen.blit(over_text, (425, 322))
    screen.blit(below_text, (540, 450))
    screen.blit(esc_text, (700, 500))

#new_this function is initalizing bullets and filling empty bullets array this bullets belongs to player
def make_bullets(number):
    global bullets
    for item in range(0, number):
        bullets.append([bullet_img, item, "not-fired", 0, 0])

#new_this function is initalizing alleins and filling empty alliens  
def make_aliens(num):
    global ufo_img
    for num in range(0, num):
        x = random.randint(100, 1500)
        y = random.randint(30, 100)
        x_c = 2
        y_c = 40
        aliens.append([ufo_img, x, y, x_c, y_c])

#new_this function is showing and counting scores
def show_score():
    global score_value
    global lives
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (20, 20))
    live = font.render("Lives: " + str(lives), True, (255, 255, 255))
    screen.blit(live, (20, 60))


def show_aliens():
    global aliens
    global gameon
    global game_over
    for alien in aliens:
        if alien[2] >= 900:
            #checking game over
            game_over = True
            aliens.clear()

            score_value = 0
        screen.blit(alien[0], (alien[1], alien[2]))


def fire_bullet(x, y):
    bullet = bullets.pop(0)

    bullet[2] = "fired"
    bullet[3] = x
    bullet[4] = y

    return bullet

#new_this function is showing bullets of players on screen
def show_bullet(b):
    b[4] -= 5

    if b[4] <= 0:
        all_fired_bullets.remove(b)
        new_bullet = [bullet_img, 0, "not-fired", 0, 0]
        bullets.append(new_bullet)

    screen.blit(b[0], (b[3], b[4]))

#new_this function is checking collusion between bullets and aliens(matlab touch nbulet with aliens)
def iscol(enemyX, bulletX, enemyY, bulletY):
    dist = math.sqrt(
        math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if dist < 30:
        return True

#new_this function is making boombs 
def make_bombs(num):
    global bomb_img
    for num in range(0, num):
        bombs.append([bomb_img, 0, 0, "not-fired"])

#new_this function is checking collusion between player and bomb(matlab touch player withbomb)
def check_the_collision():
    global playerX
    global playerY
    global gameon
    global game_over
    global lives
    for bomb in all_fired_bombs:
        dist = math.sqrt((math.pow(playerX - bomb[1], 2)) +
                         (math.pow(playerY - bomb[2], 2)))

        if dist <= 30:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            lives -= 1
            all_fired_bombs.remove(bomb)

            bombs.append([bomb_img, 0, 0, "not-fired"])

#new_ we choose random alien and find x and y co ordinate and shooting with bombs
def choose_the_random_alien_and_shoot():
    global bombs
    random_alien = random.choice(aliens)

    random_alienX = random_alien[1]
    random_alienY = random_alien[2]

    bomb = bombs.pop(0)

    bomb[1] = random_alienX
    bomb[2] = random_alienY
    bomb[3] = "fired"
    all_fired_bombs.append(bomb)
    
    
#new_ we need to show the bomb in screen
def show_bomb():
    global all_fired_bombs

    for b in all_fired_bombs:

        if b[3] == "fired":
            b[2] += 2.25
            screen.blit(b[0], (b[1], b[2]))

        if b[2] >= 900:
            all_fired_bombs.remove(b)
            bombs.append([bomb_img, 0, 0, "not-fired"])

#*************  game start from here***************
#intial we are makeing alien 7 and bullets 25 and bomb 20 in game
make_aliens(7)
make_bullets(25)
make_bombs(20)

bullet_firing = False
is_game_over = False


#new_ 1 unit per 200 mile sec mein bullet nikal rahi h
#new_if we comment below line then bullet will be fired only when 1 st bullet will touch upper screen then next bullet will be fiered.
pygame.key.set_repeat(1, 200)
gameon = True


while gameon:

    #updating the display
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))


    # new_checking for events at which key 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameon = False

        #checking for the keyup and keydown

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3

            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_UP:
                playerY_change = -2

            if event.key == pygame.K_DOWN:
                playerY_change = 2

            if is_game_over == True:

                if event.key == pygame.K_RETURN:

                    if is_game_over == True:
                        make_aliens(12)

                        score_value = 0
                        lives = 3
                        is_game_over = False

            if event.key == pygame.K_SPACE:
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()

                bulletX_cordinate = playerX + 15
                bulletY_cordinate = playerY

                fired_bullet = fire_bullet(bulletX_cordinate,
                                           bulletY_cordinate)
                all_fired_bullets.append(fired_bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    #for loop end***********************
    #new_if statements is for checkinhg the game is over or not
    if is_game_over == True:

        game_over_text()

    playerX += playerX_change
    playerY += playerY_change

    #player boundaries check (not to cross the boundary of game of player cango out of screen here)
    if playerX <= 0:
        playerX = 0
    elif playerX >= 1536:
        playerX = 1536

    if playerY <= 0:
        playerY = 0
    elif playerY >= 836:
        playerY = 836

    #ufo boundaries check

    for alien in aliens:

        alien[1] = alien[1] + alien[3]

        if alien[1] <= 0:
            alien[3] = (2)
            alien[2] += 30

        elif alien[1] >= 1536:
            #new_allien ka speed rotation badh jayega
            alien[3] = (2)
            #new_allien ka down speed badh jayuega
            alien[2] += 30

    #check the collision between aliens and bullets

    for bullet in all_fired_bullets:

        for alien in aliens:
            col = iscol(alien[1], bullet[3], alien[2], bullet[4])
            if col == True:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()

                aliens.remove(alien)
                score_value += 1

                #making new alien
                x = random.randint(100, 1500)
                y = random.randint(30, 400)
                x_c = 2
                y_c = 40
                aliens.append([ufo_img, x, y, x_c, y_c])

                #reloding the bullet
                # all_fired_bullets.remove(bullet)
                # bullets.append([bullet_img, 0, "not-fired", 0, 0])

    #move the bullet

    for b in all_fired_bullets:
        show_bullet(b)

#check the lives of the player
    if lives <= 0:
        #checking game over

        is_game_over = True
        aliens.clear()
        score_value = 0
        lives = 0

#check the collision of bommb with ship

    if is_game_over == False:
        check_the_collision()

    #shoot the bomb

    if is_game_over == False:
        random_number = random.randint(1, 1000)
        if random_number < 15:
            choose_the_random_alien_and_shoot()

    show_player(playerX, playerY)
    show_aliens()
    show_score()
    show_bomb()

    pygame.display.update()

