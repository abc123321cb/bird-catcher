# This imports what is needed for the project
from setup import *
pygame.init()
pygame.font.init()
pygame.joystick.init()

selection = 1
tortcharing = False
tortcharge = 0


def update():
    screen.fill((0, 0, 0))

    for obsticles in ob:
        pygame.draw.rect(screen, obsticles.color, pygame.Rect(obsticles.x, obsticles.y, obsticles.width, obsticles.height))

    # Clears the screen add the obstacles then for each cat instance puts it on the screen
    for cat in catlist:
        if not cat.status == 0:

            if cat.xvel > 0:
                screen.blit(catpicright, (cat.x, cat.y))
            else:
                screen.blit(catpic, (cat.x, cat.y))

    # Puts the ghosts on the screen
    for ranged in rangedlist:
        if not ranged.status == 0:
            if ranged.xvel > 0:
                screen.blit(ghost, (ranged.x, ranged.y))
            else:
                screen.blit(ghostright, (ranged.x, ranged.y))

    # Puts the bird on the screen and is set up to make it easy to add multiple birds for future updates
    for nablu in nablulist:
        if not nablu.status == 0:
            if nablu.xvel > 0:
                screen.blit(nabluright, (nablu.x, nablu.y))
            else:
                screen.blit(nablupic, (nablu.x, nablu.y))

    # Puts the turtle on the screen
    global tort
    if tortxvel > 0:
        tort = tort_right_img
    if tortxvel < 0:
        tort = tort_left_img
    screen.blit(tort, (config.tortx, config.torty))

    # Puts the hearts in the top right of the screen
    h = config.health
    n = 60
    while h > 0:
        screen.blit(fullheart, (width - n, 5))
        h -= 1
        n += 60

    h = 3 - config.health
    n = 180
    while h > 0:
        screen.blit(emptyheart, (width - n, 5))
        n-=60
        h-=1

    # Puts the bullets on the screen and then updates the display
    for b in bulletlist:
        if not b.status == 0:
            screen.blit(bullet, (b.x, b.y))
    pygame.display.flip()

# The walls are defined along with the edge borders
floor = obsticle(-10, height - 30, width + 20, 30)
platform1 = obsticle(100, 300, 100, 200)
platform2 = obsticle(600, 200, 100, 150)
celling = obsticle(-10, -10, width+20, 100, (0, 0, 100))
leftwall = obsticle(-10, -10, 10, height + 20)
rightwall = obsticle(width, -10, 10, height + 20)
#platform3 = obsticle(0, height / 2, 300, 100)

while True:
    # Sets the frame rate
    GameClock.tick(60)
    # This puts the right image on the screen
    if config.gamestate == 1:   # INTRO screen
        screen.fill((0, 0, 0))
        if config.selection == 1:
            if height > width:
                screen.blit(startselect, (0, (height - width) / 2))
            else:
                screen.blit(startselect, ((width - height) / 2, 0))
        elif config.selection == 2:
            if height > width:
                screen.blit(tutorialselect, (0, (height - width) / 2))
            else:
                screen.blit(tutorialselect, ((width - height) / 2, 0))
        elif config.selection == 3:
            if height > width:
                screen.blit(leaderboardselect, (0, (height - width) / 2))
            else:
                screen.blit(leaderboardselect, ((width - height) / 2, 0))
        pygame.display.flip()

        # This takes user input and moves the box and selects the options
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.quit()
                    sys.exit()
                if event.button == 1:
                    if config.selection == 1:
                        config.gamestate = 2
                    if config.selection == 2:
                        config.gamestate = 3
                    if config.selection == 3:
                        config.gamestate = 4
            if event.type == pygame.JOYAXISMOTION:
                for joy_num in range(1):
                    vert_axis_pos = -round(my_joystick[joy_num].get_axis(1))
                    if vert_axis_pos == 1 and config.selection > 1:
                        config.selection -= 1
                    if vert_axis_pos == -1 and config.selection < 3:
                        config.selection += 1
                        pygame.time.delay(1)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and config.selection < 3:
                    config.selection += 1
                if event.key == pygame.K_w and config.selection > 1:
                    config.selection -= 1
                if event.key == pygame.K_SPACE:
                    if config.selection == 1:
                        config.gamestate = 2
                    if config.selection == 2:
                        config.gamestate = 3
                    if config.selection == 3:
                        config.gamestate = 4
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


    elif config.gamestate == 2: # GAME screen
        # Takes user input and updates variables
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.JOYAXISMOTION:
                for joy_num in range(1):
                    hor_axis_pos = round(my_joystick[joy_num].get_axis(0))
                    if hor_axis_pos == 1:
                        tortxvel = tortspeed
                    if hor_axis_pos == -1:
                        tortxvel = -tortspeed
                    if hor_axis_pos == 0:
                        tortxvel = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    tortxvel = -tortspeed

                if event.key == pygame.K_d:
                    tortxvel = tortspeed

                if event.key == pygame.K_w:
                    tortyvel=-8

                if event.key == pygame.K_SPACE:
                    tortcharing = True

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and tortxvel < 0:
                    tortxvel = 0
                if event.key == pygame.K_d and tortxvel > 0:
                    tortxvel = 0
                if event.key == pygame.K_SPACE:
                    tortcharing = False

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.quit()
                    sys.exit()
                if event.button == 1:
                    tortyvel = -8

        # For a future update...
        if tortcharing:
            tortcharge += 1
        else:
            tortcharge -= 1

        # Gravity
        tortyvel += 0.2

        # Obstacle collison to make sure the turtle doesn't go through walls
        config.tortx = config.tortx + tortxvel
        tortrect.topleft = [config.tortx, config.torty]
        for obsticles in ob:
            if tortrect.colliderect(obsticles.rect):
                if tortxvel>0:
                    config.tortx = obsticles.rect.left - tortrect.width

                elif tortxvel<0:
                    config.tortx = obsticles.rect.right

        config.torty = config.torty + tortyvel
        tortrect.topleft = [config.tortx, config.torty]
        for obsticles in ob:
            if tortrect.colliderect(obsticles.rect):
                if tortyvel > 0:
                    config.torty = obsticles.rect.top - tortrect.height
                if tortyvel < 0:
                    config.torty = obsticles.rect.bottom
                tortyvel=0

        # Update position of enemies and bullets
        for cats in catlist:
            if not cats.status == 0:
                cats.move(config.tortx, config.torty, tortrect)
        for b in bulletlist:
            if not b.status == 0:
                b.move()
        for nablus in nablulist:
            nablus.move()

        # Update screen
        update()

    elif config.gamestate == 3: # The tutorial screen
        screen.fill((0, 0, 0))
        if height > width:
            screen.blit(tutorial, (0, (height - width) / 2))
        else:
            screen.blit(tutorial, ((width - height) / 2, 0))

        pygame.display.flip()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    config.gamestate = 1

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.quit()
                    sys.exit()
                if event.button == 1:
                    config.gamestate = 1

    elif config.gamestate == 4: # HIGH SCORE screen
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont('arial', 40)
        records = open("highscore.txt", "rb")
        recordlist = pickle.load(records)
        n = -50
        for scores in recordlist:
            a = scores[0] + "  " + str(scores[1])
            a = font.render(a, False, (255, 255, 255))
            screen.blit(a, (width/2 - 30, height/2 + n))
            n += 50
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    config.gamestate = 1

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.quit()
                    sys.exit()
                if event.button == 1:
                    config.gamestate = 1

    elif config.gamestate == 5: # STAR screen
        screen.fill((0, 0, 0))
        if config.score == 5:
            if config.selection == 1:
                starscreen = onestarc
            else:
                starscreen = onestare
        else:
            if config.selection == 1:
                starscreen = twostarc
            else:
                starscreen = twostare
        if height > width:
            screen.blit(starscreen, (0, (height - width) / 2))
        else:
            screen.blit(starscreen, ((width - height) / 2, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if config.selection == 1:
                        config.gamestate = 2
                    else:
                        gameover()
                    config.selection = 1
                if event.key == pygame.K_w and config.selection > 1:
                    config.selection -= 1
                if event.key == pygame.K_s and config.selection < 2:
                    config.selection += 1

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.JOYAXISMOTION:
                for joy_num in range(1):
                    vert_axis_pos = -round(my_joystick[joy_num].get_axis(1))
                    if vert_axis_pos == 1 and config.selection > 1 and config.selection > 1:
                        config.selection -= config.selection
                    if vert_axis_pos == -1 and config.selection > 1 and config.selection < 2:
                        config.selection += config.selection

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    pygame.quit()
                    sys.exit()
                if event.button == 1:
                    if config.selection == 1:
                        config.gamestate = 2
                    else:
                        gameover()
