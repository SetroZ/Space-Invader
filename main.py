import pygame, asyncio, time
import random
import math
from pygame import mixer
import os

# Initialize the pygame
pygame.init()

# Create the screen (w,h)
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("Data/space.jpg").convert()
music = "Data/background.wav"
mixer.music.load(music)
mixer.music.play(-1)
Restart = "False"
menu = "False"
score_value = 0
score_highest = 0
Lives = 3

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Data/spaceship.png")
pygame.display.set_icon(icon)
Speed_enemy = 2.5

# Player
playerimg = pygame.image.load("Data/ufo.png")
gunimg = pygame.image.load("Data/rocket2.png")
a = pygame.image.load("Data/heart1.png")
b = pygame.image.load("Data/heart1.png")
c = pygame.image.load("Data/heart1.png")

# Player initial position
playerX = 370
playerY = 480
move = 0
move2 = 0
movey = 0
movey2 = 0

# Enemy initialization
enemyimg = []
enemyX = []
enemyY = []
enemymoveY = []
enemymoveX = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("Data/alien2.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 150))
    enemymoveX.append(Speed_enemy)
    enemymoveY.append(Speed_enemy)

# Gun initialization
gunX = 0
gunY = 0
gunmoveY = 0
gun_state = "Ready"


def collision(x, y, X2, Y2, distance1):
    distance = math.sqrt((math.pow(x - X2, 2)) + (math.pow(y - Y2, 2)))
    if distance < distance1:
        return True
    else:
        return False


# Draw image
def player(img, x, y):
    screen.blit(img, (x, y))


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire(x, y):
    global gun_state
    gun_state = "Fire"
    screen.blit(gunimg, (x + 10, y))


font = pygame.font.Font("Data/Fluo Gums.ttf", 20)
hfont = pygame.font.Font("Data/Fluo Gums.ttf", 15)

fontX = 10
fontY = 10
losefont = pygame.font.Font("freesansbold.ttf", 40)


def display_score(x, y):
    score = font.render("SCORE:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def loserfunc(x, y):
    loser = losefont.render("Press R to Restart", True, (255, 0, 0))
    screen.blit(loser, (x, y))


def highest(x, y):
    highest = hfont.render("HIGHEST SCORE:" + str(score_highest), True, (255, 255, 255))
    screen.blit(highest, (x, y))


print("s")


# Game Loop makes sure that the game is always running
async def main():
    bullet_sound = mixer.Sound("Data/laser.wav")
    Lose = mixer.Sound("Data/Loser.ogg")
    global playerX, movey, movey2, move, move2, a, b, c, running, score_value, score_highest, Lives, menu, Restart, gun_state, playerY
    while running:
        # screen color
        screen.fill((0, 0, 0))

        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if a key is pressed check whether it is left or right
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move2 = -0.5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move = 0.5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move2 = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    movey2 = -0.5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    movey = 0.5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    movey2 = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    movey = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if gun_state == "Ready":
                        bullet_sound.play()
                        gunY = playerY
                        gunX = playerX
                        fire(gunX, gunY)
                        gunmoveY = -0.5
                if event.key == pygame.K_r:
                    if Restart == "True":
                        for j in range(num_of_enemies):
                            enemyX[j] = random.randint(0, 736)
                            enemyY[j] = random.randint(0, 150)
                        score_value = 0
                        menu = "False"
                        music = "Data/background.wav"
                        mixer.music.load(music)
                        mixer.music.play(-1)
                        Restart = "False"
                        playerX = 370
                        playerY = 480
                        Lives = 3
                        a = pygame.image.load("Data/heart1.png")
                        b = pygame.image.load("Data/heart1.png")
                        c = pygame.image.load("Data/heart1.png")

        if menu == "True":
            loserfunc(215, 300)
        if gun_state == "Ready":
            gunY = playerY
            gunX = playerX

        # update display
        # 5=5+x
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        if playerY <= 0:
            playerY = 0
        elif playerY >= 536:
            playerY = 536

        for i in range(num_of_enemies):
            if enemyX[i] <= 0:
                enemymoveX[i] = Speed_enemy
            elif enemyX[i] >= 736:
                enemymoveX[i] = -1 * Speed_enemy

            if enemyY[i] <= 0:
                enemymoveY[i] = Speed_enemy
            elif enemyY[i] >= 536:
                enemymoveY[i] = -1 * Speed_enemy

            collison2 = collision(enemyX[i], enemyY[i], gunX, gunY, 30)
            if collison2:
                if score_value == score_highest:
                    score_highest += 1
                gun_state = "Ready"

                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 150)
                explosion_sound = mixer.Sound("Data/explosion.wav")
                explosion_sound.play()

            collision3 = collision(enemyX[i], enemyY[i], playerX, playerY, 60)
            if collision3:
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 150)
                Minecraft = mixer.Sound("Data/Minecraft.ogg")
                Minecraft.play()
                Lives -= 1
                if Lives == 2:
                    a = pygame.image.load("Data/noheart.png")
                if Lives == 1:
                    b = pygame.image.load("Data/noheart.png")
                if Lives == 0:
                    c = pygame.image.load("Data/noheart.png")
                    menu = "True"
                    for j in range(num_of_enemies):
                        enemyX[j] = 300000
                    pygame.mixer.quit()
                    pygame.mixer.init()

                    Lose.play()
                    Restart = "True"

            enemy(enemyX[i], enemyY[i], i)

            if gunY <= 0:
                gunY = playerY
                gun_state = "Ready"
            if gun_state == "Fire":
                fire(gunX, gunY)
                gunY += gunmoveY*4
            enemyY[i] += enemymoveY[i]
            enemyX[i] += enemymoveX[i]
        playerY += movey*10
        playerY += movey2*10
        playerX += move*10
        playerX += move2*10

        highest(10, 60)
        display_score(fontX, fontY)

        player(playerimg, playerX, playerY)
        player(a, 770, 5)
        player(b, 735, 5)
        player(c, 700, 5)

        pygame.display.update()
        await asyncio.sleep(0)


# Define initial values for global variables

running = True
# Run the main function using asyncio.run
asyncio.run(main())


