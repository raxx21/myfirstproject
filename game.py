import pygame
import random
import math
from pygame import mixer

# initialization
pygame.init()


# create a window
screen = pygame.display.set_mode((800, 600))

# background
backgroundImp = pygame.image.load("background.jpg")

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invador")
icon = pygame.image.load("space-ship.png")
pygame.display.set_icon(icon)

# player
playerImp = pygame.image.load("spaceship.png")
playerX = 380
playerY = 500
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerImp, (x, y))


# monster
monsterImp = []
monsterX = []
monsterY = []
monsterX_change = []
monsterY_change = []
no_of_monster = 10
for i in range(no_of_monster):
    monsterImp.append(pygame.image.load("monster.png"))
    monsterX.append(random.randint(0, 768))
    monsterY.append(random.randint(32, 150))
    monsterX_change.append(2)
    monsterY_change.append(40)


def monster(x, y, i):
    screen.blit(monsterImp[i], (x, y))


# bullet
bulletImp = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = -5

bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImp, (x+16, y+20))

# collision function


def iscollision(monsterX, monsterY, bulletX, bulletY):
    distance = math.sqrt(math.pow(monsterX - bulletX, 2) +
                         (math.pow(monsterY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game over function
game_over_Imp = "NO"


def game_over(monsterX, monsterY, playerX, playerY):
    distance1 = math.sqrt(math.pow(monsterX - playerX, 2) +
                          (math.pow(monsterY - playerY, 2)))
    if distance1 < 32:
        global game_over_Imp
        game_over_Imp = "YES"
    else:
        game_over_Imp = "NO"


# game over screen

game_overImp = pygame.image.load("gameover.png")
game_overX = 0
game_overY = 0


# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# window loop
running = True
while running:
     # background colure
    screen.fill((0, 0, 0))
    # background image
    if monsterY[i] > 1000:
        screen.blit(game_overImp, (0, 0))
    else:
        screen.blit(backgroundImp, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # keystroke pressed left or right
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = +2
            # keystroke pressed up or down
            if event.key == pygame.K_UP:
                playerY_change = -2

            if event.key == pygame.K_DOWN:
                playerY_change = +2

            # keystroke pressed space
            if event.key == pygame.K_SPACE:
                # bullet sound
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                # only one bullet at a time
                if bullet_state is "ready":
                    bulletY = playerY
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            # keystroke resized left or right
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            # keystroke resized down or up
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    # boundarie of x axis of ship
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    # boundarie of y axis of ship
    playerY += playerY_change
    if playerY < 0:
        playerY = 0
    elif playerY > 538:
        playerY = 536

    # movement of monster
    for i in range(no_of_monster):
        game_over(monsterX[i], monsterY[i], playerX, playerY)
        if game_over_Imp == "YES":
            global collision_sound
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            for j in range(no_of_monster):
                monsterY[j] = 2000
                playerX = 380
                playerY = 500
            break
        monsterX[i] += monsterX_change[i]
        if monsterX[i] < 0:
            monsterX_change[i] = 2
            monsterY[i] += monsterY_change[i]
        if monsterX[i] > 768:
            monsterX_change[i] = -2
            monsterY[i] += monsterY_change[i]

        # collision
        collision = iscollision(monsterX[i], monsterY[i], bulletX, bulletY)
        if collision:
            # collision music
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullet_state = "ready"
            bulletY = playerY
            score_value += 1
            # monster respone
            monsterX[i] = random.randint(0, 768)
            monsterY[i] = random.randint(32, 150)

        monster(monsterX[i], monsterY[i], i)

    # reload bullet
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"
    # movement of the bullet
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
   
