# This imports what is needed for the project
import math
import os.path
import random
import sys
import pickle
import pygame
import config
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.joystick.init()


# This class makes it easy to add obstacles
class obsticle():
    def __init__(self, x, y, width, height, color=(100,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        ob.append(self)


class cat():
    # Adds basic parameters to the cats and makes it easier to use
    def __init__(self, x, y, xvel, yvel, status):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.status = status
        catspeed = random.random()*2 + 1
        self.speed = catspeed
        self.rect = pygame.Rect(x, y, catrect.width, catrect.height)
        catlist.append(self)

    # Moves the cats and updates their rectangles
    def move(self,tortx,torty,tortrect):
        if self.x > tortx:
            self.xvel = -self.speed
        else:
            self.xvel = self.speed
        if self.y > torty:
            self.yvel = -self.speed
        else:
            self.yvel = self.speed
        self.x = self.x + self.xvel
        self.rect.topleft = [self.x, self.y]

        for obsticles in ob:
            if self.rect.colliderect(obsticles.rect):
                if self.xvel > 0:
                    self.x = obsticles.rect.left-self.rect.width
                if self.xvel < 0:
                    self.x = obsticles.rect.right

        tortrect.topleft = [tortx, torty]
        self.y = self.y + self.yvel
        self.rect.topleft = [self.x, self.y]

        # Checks for collisions between cats and obstacles
        for obsticles in ob:
            if self.rect.colliderect(obsticles.rect):
                if self.yvel > 0:
                    self.y = obsticles.rect.top - self.rect.height
                if self.yvel < 0:
                    self.y = obsticles.rect.bottom

        # Checks for collisions between cats and the turtle
        if tortrect.colliderect(self.rect):
            self.status = 0
            collide()

class ranged(cat):
    # Subclass of cats that is the ghosts that uses about the same init method just changing the collison box
    # and adding a cooldown
    def __init__(self, x, y, xvel, yvel, status):
        super().__init__(x, y, xvel, yvel, status)
        self.cooldown = config.rangedCooldown
        self.rect = pygame.Rect(x, y, rangedrect.width, rangedrect.height)
        rangedlist.append(self)

    def move(self,tortx,torty,tortrect):
        # Same movement but checks if it is time to fire
        super().move(tortx, torty, tortrect)
        self.cooldown -= 1
        if self.cooldown <= 0:
            self.checkFire()

    def fire(self, direction, d):
        # Fires a bullet from the ghost
        for bullet in bulletlist:
            if bullet.status == 0:
                bullet.status = 1
                bullet.x = self.x
                bullet.y = self.y
                if direction == 0:
                    bullet.rect = pygame.Rect(bullet.x, bullet.y, bulletrect.height, bulletrect.width)
                    bullet.x = self.x + self.rect.width/2 - bullet.rect.width
                    bullet.y = self.y + self.rect.height/2 - bullet.rect.width
                    if d > 0:
                        bullet.xvel = 0
                        bullet.yvel = -bulletspeed
                    else:
                        bullet.xvel = 0
                        bullet.yvel = bulletspeed
                else:
                    bullet.x = self.x + self.rect.width/2 - bullet.rect.width
                    bullet.y = self.y + self.rect.height/2 - bullet.rect.width
                    if d > 0:
                        bullet.xvel = -bulletspeed
                        bullet.yvel = 0
                    else:
                        bullet.xvel = bulletspeed
                        bullet.yvel = 0
                break

    def checkFire(self):
        # Checks if the turtle is in range to fire
        if abs(self.x - config.tortx) <= 30:
            self.fire(0, self.y - config.torty)
            self.cooldown = config.rangedCooldown

        if abs(self.y - config.torty) <= 30:
            self.fire(1, self.x - config.tortx)
            self.cooldown = config.rangedCooldown

class nablu():
    # The bird's class it defines the attributes of the bird
    def __init__(self, x, y, xvel, yvel, status):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.status = status
        self.timer = config.nablu_cooldown
        self.rect = pygame.Rect(self.x, self.y, nablurect.width, nablurect.height)
        self.speed = 3
        nablulist.append(self)

    def finddistance(self):
        # This returns how far away the turtle is
        if config.tortx >= self.x:
            right = 1
        else:
            right = 0
        if config.torty >= self.y:
            lower = 1
        else:
            lower = 0
        x_calc = self.x + right * self.rect.width - config.tortx
        y_calc = self.y + lower * self.rect.height - config.torty

        return math.sqrt(x_calc*x_calc + y_calc*y_calc)

    def teleport(self):
        # This keeps teleporting the bird randomly until it is not in a obstacle or right next to the turtle
        n = 1
        while self.finddistance() < 300 or n == 1:
            self.x = random.randrange(0, width-self.rect.width)
            self.y = random.randrange(80, height-30-self.rect.height)
            n = 0
            self.rect.topleft = [self.x, self.y]
            for obsticles in ob:
                if self.rect.colliderect(obsticles.rect):
                    n = 1
                    break

    def move(self):
        # This checks if the bird is overlapping with the turtle and ends the level if it is
        if self.timer <= 0 and self.finddistance() <= 200:
            self.teleport()
            self.timer = config.nablu_cooldown

        if config.tortx > self.x:
            self.xvel = -self.speed
        else:
            self.xvel = self.speed

        if config.torty > self.y:
            self.yvel = -self.speed
        else:
            self.yvel = self.speed

        self.x += self.xvel
        self.rect.topleft = [self.x, self.y]
        for obsticles in ob:
            if self.rect.colliderect(obsticles.rect):
                if self.xvel > 0:
                    self.x = obsticles.rect.left-self.rect.width
                if self.xvel < 0:
                    self.x = obsticles.rect.right

        tortrect.topleft = [config.tortx, config.torty]

        self.y = self.y + self.yvel
        self.rect.topleft = [self.x, self.y]

        # This moves the bird and stops it at obstacles
        for obsticles in ob:
            if self.rect.colliderect(obsticles.rect):
                if self.yvel > 0:
                    self.y = obsticles.rect.top - self.rect.height
                if self.yvel < 0:
                    self.y = obsticles.rect.bottom

        # This checks if the bird is overlapping with the turtle and ends the level if it is
        if tortrect.colliderect(self.rect) and self.status > 0:
            self.status = 0
            self.timer = config.nablu_cooldown
            config.score += 1
            if config.score == 5 or config.score == 10:
                config.gamestate = 5
            nextlevel()

        self.timer -= 1

class bullets():
    def __init__(self, x, y, xvel, yvel, status):
        # This defines the attributes of the bullets
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.status = status
        self.rect = pygame.Rect(self.x, self.y, bulletrect.width, bulletrect.height)
        bulletlist.append(self)

    def move(self):
        # This moves the bullets and checks for collisions with the turtle and obstacles
        self.x += self.xvel
        self.y += self.yvel
        self.rect.topleft = [self.x, self.y]

        for obsticles in ob:
            if self.rect.colliderect(obsticles.rect):
                self.status = 0
        if tortrect.colliderect(self.rect):
            collide()
            self.status = 0

def entername():
    # This function is to enter your name for the leaderboard and
    # at first it defines some variables that are necessary for the next part
    picking = True
    selection = 0
    typed = 0
    alph = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    font = pygame.font.SysFont('arial', 20)
    abclist = []
    if True:
        A = font.render("A", False, (255, 255, 255))
        B = font.render("B", False, (255, 255, 255))
        C = font.render("C", False, (255, 255, 255))
        D = font.render("D", False, (255, 255, 255))
        E = font.render("E", False, (255, 255, 255))
        F = font.render("F", False, (255, 255, 255))
        G = font.render("G", False, (255, 255, 255))
        H = font.render("H", False, (255, 255, 255))
        I = font.render("I", False, (255, 255, 255))
        J = font.render("J", False, (255, 255, 255))
        K = font.render("K", False, (255, 255, 255))
        L = font.render("L", False, (255, 255, 255))
        M = font.render("M", False, (255, 255, 255))
        N = font.render("N", False, (255, 255, 255))
        O = font.render("O", False, (255, 255, 255))
        P = font.render("P", False, (255, 255, 255))
        Q = font.render("Q", False, (255, 255, 255))
        R = font.render("R", False, (255, 255, 255))
        S = font.render("S", False, (255, 255, 255))
        T = font.render("T", False, (255, 255, 255))
        U = font.render("U", False, (255, 255, 255))
        V = font.render("V", False, (255, 255, 255))
        W = font.render("W", False, (255, 255, 255))
        X = font.render("X", False, (255, 255, 255))
        Y = font.render("Y", False, (255, 255, 255))
        Z = font.render("Z", False, (255, 255, 255))
        abclist.extend((A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z))

    # This updates the screen
    while picking:
        pygame.display.flip()
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 20)
        text = font.render("Enter Your Name", False, (255, 255, 255))
        screen.blit(text, (100,10))
        n = 40
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(30 + 30 * selection, 50, 30, 30))
        for letter in abclist:
            screen.blit(letter, (n,50))
            n += 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.JOYAXISMOTION:
                for joy_num in range(1):
                    horiz_axis_pos = round(my_joystick[joy_num].get_axis(0))
                    if horiz_axis_pos == 1 and selection < 25:
                        selection += 1
                    if horiz_axis_pos == -1 and selection > 0:
                        selection -= 1

            # This takes user input to move the selection box and select the letters
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and selection < 25:
                    selection += 1
                if event.key == pygame.K_a and selection > 0:
                    selection -= 1
                if event.key == pygame.K_SPACE:
                    if typed == 0:
                        firstletter = selection
                    elif typed == 1:
                        secoundletter = selection
                    elif typed == 2:
                        thirdletter = selection
                    typed += 1
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.quit()
                    sys.exit()
                if event.button == 1:
                    if config.selection == 1:
                        if typed == 0:
                            firstletter = selection
                        elif typed == 1:
                            secoundletter = selection
                        elif typed == 2:
                            thirdletter = selection
                        typed += 1


        # This puts the letters chosen on the screen
        n = 0
        while n < typed:
            screen.blit(abclist[firstletter], (width/2 - 45, height/2))
            if typed >= 2:
                screen.blit(abclist[secoundletter], (width/2 - 15, height/2))
            if typed >= 3:
                screen.blit(abclist[thirdletter], (width/2 + 15, height/2))
            n += 1

        # This sets the name and score and ends the loop
        if typed == 3:
            config.name = [alph[firstletter] + alph[secoundletter] + alph[thirdletter], config.score]
            pygame.display.flip()
            picking = False

def gameover():
    # Puts the game over screen and waits for a little bit then calls the enter name function to get the players name
    screen.fill((0, 0, 0))
    if height > width:
        screen.blit(gameOverScreen, (0, (height-width)/2))
    else:
        screen.blit(gameOverScreen, ((width-height)/2, 0))
    pygame.display.flip()
    pygame.time.delay(3000)
    entername()

    if os.path.getsize("highscore.txt") == 0:
        highscorefile = open("highscore.txt", "wb")
        highscorelist = [config.name]
        print(config.name)
        pickle.dump(highscorelist, highscorefile)
        highscorefile.close()
    else:
        # This adds the score to the high score list then removes the lowest score
        highscorefile = open("highscore.txt", "rb")
        highscorelist = pickle.load(highscorefile)
        scores = []
        for values in highscorelist:
            scores.append(int(values[-1]))
        scores.sort(reverse=True)
        while len(scores) < 3:
            scores.append(0)

        if config.score > scores[2]:
            if config.score > scores[1]:
                if config.score > scores[0]:
                    highscorelist.insert(0, config.name)
                else:
                    highscorelist.insert(1, config.name)
            else:
                highscorelist.insert(2, config.name)
        else:
            highscorelist.append(config.name)
        while len(highscorelist) > 3:
            highscorelist.pop()
        highscorefile.close()
        highscorefile = open("highscore.txt", "wb")
        pickle.dump(highscorelist, highscorefile)
        highscorefile.close()
    #print(highscorelist)

    pygame.quit()
    sys.exit()

def collide():
    # This code decreases health by one and checks if the character died
    config.health -= 1
    if config.health == 0:
        gameover()
    damagesound = pygame.mixer.Sound('damage.wav')
    damagesound.play()


def nextlevel():
    # Increases the difficulty, randomizes the position of the enemies,
    # and moves the turtle back to the starting position
    global difficulty
    difficulty += 1
    config.tortx = 100
    config.torty = 100
    for b in bulletlist:
        b.status = 0
    for c in catlist:
        c.status = 0
        c.x = random.randrange(400, width-10)
        c.y = random.randrange(100, height-100)

    # Makes the enemies and randomizes the bird's position
    i = 1
    n = 0
    while i < difficulty:
        for c in catlist:
            if c.status == 0 and n != i:
                c.status = 1
                n = i
        n = 0
        for g in rangedlist:
            if i % 2 == 1 and g.status == 0 and n != i:
                g.status = 1
                n = i

        for n in nablulist:
            n.status = 3
            n.teleport()
        i += 1

# Declares variables needed for the game and initializes the screen
pygame.mouse.set_visible(0)
joy = False
if pygame.joystick.get_count() > 0:
    my_joystick = [pygame.joystick.Joystick(0)]
    my_joystick[0].init()
    joy = True
difficulty = 1
bulletspeed = 7
nablulist = []
catlist = []
ob = []
width = 1000
height = 600
size = width, height
screen = pygame.display.set_mode(size)
GameClock = pygame.time.Clock()
leftpressed = False
rightpressed = False

# Defines the player's variables
tort = pygame.image.load('turtle.png').convert()
tort_left_img = tort
tort_right_img = pygame.transform.flip(tort, True, False)
config.tortx = 100
config.torty = 100
tortxvel = 0
tortyvel = 0
tortrect = tort.get_rect()
tortspeed = 4

# Gets the cats image and makes 30 cats that will activated and deactivated throughout the game
catpic = pygame.image.load('cat.png').convert()
catpicright = pygame.transform.flip(catpic, True, False)
catrect = catpic.get_rect()
n = 30
while n > 0:
    cat(random.randrange(400, width-10), random.randrange(100, height-100), 0, 0, 0)
    n -= 1
for i in [difficulty]:
    for c in catlist:
        if c.status == 0:
            c.status = 1
            break

# Gets the bird picture and makes the bird
nablupic = pygame.image.load('NaBlu.png').convert()
nabluright = pygame.transform.flip(nablupic, True, False)
nablurect = nablupic.get_rect()
nablu(300, 300, 0, 0, 3)

# Gets the heart images
fullheart = pygame.image.load('fullheart.png').convert()
fullheart = pygame.transform.scale(fullheart, (50, 50))
emptyheart = pygame.image.load('emptyheart.png').convert()
emptyheart = pygame.transform.scale(emptyheart, (50, 50))

# Gets the ghost images and creates 20 ghosts that are inactive
ghost = pygame.image.load('ghost.png').convert()
ghostright = pygame.transform.flip(ghost, True, False)
rangedrect = ghost.get_rect()
rangedlist = []
n = 20
while n > 0:
    ranged(random.randrange(400, width - 10), random.randrange(100, height-100), 0, 0, 0)
    n -= 1

# Gets the bullet image and makes 50 inactive bullets
bullet = pygame.image.load('lazer.png').convert()
bulletrect = bullet.get_rect()
bulletlist = []
n = 50
while n > 0:
    bullets(0, 0, 0, 0, 0)
    n -= 1

# Gets the game over picture and plays the music on loop
gameOverScreen = pygame.image.load('Gameover.png').convert()
if width > height:
    gameOverScreen = pygame.transform.scale(gameOverScreen, (height, height))
else:
    gameOverScreen = pygame.transform.scale(gameOverScreen, (width, width))
pygame.mixer.music.load('background_music.wav')
pygame.mixer.music.play(-1)

# Gets all the screen wide images and scales them to the screen
startselect = pygame.image.load('Startselect.png')
tutorialselect = pygame.image.load('Tutorialselect.png')
leaderboardselect = pygame.image.load('Leaderboardselect.png')
tutorial = pygame.image.load('tutorial.png')
onestarc = pygame.image.load('onestarcountinue.png')
onestare = pygame.image.load('onestarfinish.png')
twostarc = pygame.image.load('twostarcountinue.png')
twostare = pygame.image.load('twostarexit.png')
if width > height:
    onestarc = pygame.transform.scale(onestarc, (height, height))
    onestare = pygame.transform.scale(onestare, (height, height))
    twostarc = pygame.transform.scale(twostarc, (height, height))
    twostare = pygame.transform.scale(twostare, (height, height))
    tutorial = pygame.transform.scale(tutorial, (height, height))
    startselect = pygame.transform.scale(startselect, (height, height))
    tutorialselect = pygame.transform.scale(tutorialselect, (height, height))
    leaderboardselect = pygame.transform.scale(leaderboardselect, (height, height))
else:
    onestarc = pygame.transform.scale(onestarc, (width, width))
    onestare = pygame.transform.scale(onestare, (width, width))
    twostarc = pygame.transform.scale(twostarc, (width, width))
    twostare = pygame.transform.scale(twostare, (width, width))
    tutorial = pygame.transform.scale(tutorial, (width, width))
    startselect = pygame.transform.scale(startselect, (width, width))
    tutorialselect = pygame.transform.scale(tutorialselect, (width, width))
    leaderboardselect = pygame.transform.scale(leaderboardselect, (width, width))