"""
COLIN: So far this version of our project contains:
- Player sprite (Movement and firing ability)
- Two types of enemy sprites (Bug Type 1 and Bug Type 2, both with movement and firing abilities)
- Basic collision between corresponding sprites and lasers (No health system)
COLIN: But it also lacks:
- A Main Menu with game options  (1 player, 2 player co-op,(2 player versus??), Difficulties)
- Sprite lives/health
- Co-op and Versus???
- Level/Difficulty escalation
- Final Boss?
- Music exlusive to main menu?
- Arcade button compatibility
- A box to put it all in
"""

# Import pygame
import pygame
import random
import RPi.GPIO as GPIO

# Initialize the pygame module
pygame.init()


#=====[ IMAGES & AUDIO ]=====
# COLIN: Here, we can put other images for enemies and a possible player 2
# Grabs image for the player sprite
PLAYER1 = pygame.image.load("p1.png")
# Adjusts the image to fit onto the screen with desired (width, height)
PLAYER1 = pygame.transform.scale(PLAYER1, (55, 40))

PLAYER2 = pygame.image.load("p2.png")
# Adjusts the image to fit onto the screen with desired (width, height)
PLAYER2 = pygame.transform.scale(PLAYER2, (55, 40))

# Grabs and adjusts image for the first bug type
BUG1 = pygame.image.load("b1.png")
BUG1 = pygame.transform.scale(BUG1, (55, 40))

# Grabs and adjusts secondary image for first bug type
BUG1A = pygame.image.load("b1a.png")
BUG1A = pygame.transform.scale(BUG1A, (55, 40))

# Grabs and adjusts image for second bug type
BUG2 = pygame.image.load("b2.png")
BUG2 = pygame.transform.scale(BUG2, (65, 80))

# Grabs and adjusts image for third bug type
BUG3 = pygame.image.load("b3.png")
BUG3 = pygame.transform.scale(BUG3, (55, 40))

# Grab image for background
BG = pygame.image.load("space.jpg")

# Grab music for game audio
MUSIC = pygame.mixer.music.load("game_music.mp3")

# Grabs sound for laser fire
FIRE = pygame.mixer.Sound("laserfire.wav")
HIT = pygame.mixer.Sound("Explosion.wav")

#=====[ VARIABLES AND LISTS]=====
# Constant variable representing a movement speed of 5 pixels for the player sprite
PIX = 5
# The following constant variables represent RGB values for colors
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (255,255,255)
# This list represents the amount of time the Bug Type 2 has fired, and its limits can be adjusted accordingly to match
# level difficulty
b2lasers = []
# This constant variable represents the amount of pixels Bug Type 1's travel per frame.
# Can be adjusted for difficulty
BUG1_MOV1 = 5
BUG1_MOV2 = 10

# These constant variables represent the x-coordinates where the Bug Type 1 should bounce off of.
R_EDGE = 745
L_EDGE = -5

# This constant variable represents the number the Bug Type 1s' coordinates can be modulated by to fire.
# Basically, it's the bug's fire rate. The lower the number, the faster it fires. This can be adjusted per difficulty
"""COLIN: BUG TYPE 1 WILL NOT FIRE once movement speed is updated if this remains == 110"""
BUG1_FIRE = 110

# This boolean variable states whether or not the player is alive, and if the game should continue
p1alive = 1
p2alive = 0


leds = [13,16,17]
but = [20,27]
GPIO.setmode(GPIO.BCM)
GPIO.setup(but, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(leds,GPIO.OUT)


#=====[ SPRITE GROUPS ]=====
# This creates a pygame group for (A)LL (SP)RITES
asp = pygame.sprite.Group()
# This creates a pygame group for player(s)
ship = pygame.sprite.Group()
# This creates a pygame group for enemies
enemy = pygame.sprite.Group()
# This creates a pygame group for the player's lasers
lasers = pygame.sprite.Group()
# This creates a pygame group for the bugs' lasers
blasers = pygame.sprite.Group()

#=====[ CREATE WINDOW ]======
# Constant variable for window's width (800) and height (400); RPi screen size
SIZE = 800, 400
# Constant variable for pygame creating the window
WIN = pygame.display.set_mode(SIZE)
# Sets caption for upper left corner of window
pygame.display.set_caption("Tech Universe: Re")

#=====[ CLASSES AND FUNCTIONS ]=====
#-----[ PLAYER SPRITE CLASS ]-----
class Player(pygame.sprite.Sprite):
    # Constructor for Player Sprite
    def __init__(self, health):
        # Call the fancy pygame sprite parent class
        super().__init__()
        # instance variable to grab player image
        self.images = []
        self.images.append(PLAYER1)
        self.images.append(PLAYER2)
        self.index = 0
        self.image = self.images[self.index]
        # Creates the hitbox and tracks coordinates for the player
        self.rect = self.image.get_rect()
        # Instance variable for player's health
        self.health = health

    # Player movement functions
    # Function that moves the player to the right when called
    def moveRight(self, pixels):
        self.rect.x += pixels
    # Function that moves the player to the left when called
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    # Function that moves the player upwards when called
    def moveUp(self, pixels):
        self.rect.y -= pixels
    # Function that moves the player downwards when called
    def moveDown(self, pixels):
        self.rect.y += pixels

    def update(self):
        if p1alive == 1 and p2alive == 0:
            self.image = self.images[0]
        if p1alive == 0 and p2alive != 0:
            self.image = self.images[1]


#-----[ PLAYERS LASER SPIRTE CLASS ]-----
class Laser (pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Creates a rectangle with width and height of 4 and fills it with predefined color RED
        self.image = pygame.Surface([4, 4])
        self.image.fill(RED)
        # Creates a rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()

    # Updates the sprite's movements
    def update(self):
        # Move the sprite up
        self.rect.y -= 7
        if self.rect.y <= 0:
            self.kill()

#------[ BUG TYPE 1 SPRITE CLASS ]------
class BugT1(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # makes an empty list for images
        self.images = []
        # Adds default, pre-defined image to list of images
        self.images.append(BUG1)
        # Adds secondary, pre-defined image to list of images
        self.images.append(BUG1A)
        # Creates index variable to sort through list
        self.index = 0
        # Picks image for sprite that correlates with index number (0 = BUG1, 1 = BUG1A)
        self.image = self.images[self.index]
        # Creates rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()
        # Instance variable that acts as a boolean for the for loop below
        self.move = 1


    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Update the sprite's movement
    def update(self):
        for i in range(self.move):
            # Move from off screen
            if self.rect.x < L_EDGE and self.rect.y == 0:
                self.rect.x += BUG1_MOV1
            # Go right
            if self.rect.x >= L_EDGE and self.rect.y == 0:
                self.rect.x += BUG1_MOV1
            # Go down (x == edge coordinate and (prev y value =< current y value < next y value))
            if self.rect.x == R_EDGE and 0 <= self.rect.y < 40:
                self.rect.y += BUG1_MOV1
            # Go left
            if self.rect.x != L_EDGE and self.rect.y == 40:
                self.rect.x -= BUG1_MOV1
            # Go down
            if self.rect.x == L_EDGE and 40 <= self.rect.y < 80:
                self.rect.y += BUG1_MOV1
            # Go right
            if self.rect.x != R_EDGE and self.rect.y == 80:
                self.rect.x += BUG1_MOV1
            # Go down
            if self.rect.x == R_EDGE and 80 <= self.rect.y < 120:
                self.rect.y += BUG1_MOV1
            # Go left
            if self.rect.x > L_EDGE and self.rect.y == 120:
                self.rect.x -= BUG1_MOV1
            # Go down
            if self.rect.x == L_EDGE and 120 <= self.rect.y < 160:
                self.rect.y += BUG1_MOV1
            # Go right
            if self.rect.x != R_EDGE and self.rect.y == 160:
                self.rect.x += BUG1_MOV1
            # Go down
            if self.rect.x == R_EDGE and 160 <= self.rect.y < 200:
                self.rect.y += BUG1_MOV1
            # Go left
            if self.rect.x > L_EDGE and self.rect.y == 200:
                self.rect.x -= BUG1_MOV2
                # Set image to BUG1A as it moves faster
                self.image = self.images[1]
            # Go down
            if self.rect.x == L_EDGE and 200 <= self.rect.y < 240:
                self.rect.y += BUG1_MOV2
            # Go right
            if self.rect.x != R_EDGE and self.rect.y == 240:
                self.rect.x += BUG1_MOV2
            # Go down
            if self.rect.x == R_EDGE and 240 <= self.rect.y < 280:
                self.rect.y += BUG1_MOV2
            # Go left
            if self.rect.x > L_EDGE and self.rect.y == 280:
                self.rect.x -= BUG1_MOV2
            # Go down
            if self.rect.x == L_EDGE and 280 <= self.rect.y < 320:
                self.rect.y += BUG1_MOV2
            # Go right
            if self.rect.x != R_EDGE and self.rect.y == 320:
                self.rect.x += BUG1_MOV2
            # Go down
            if self.rect.x == R_EDGE and 320 <= self.rect.y < 360:
                self.rect.y += BUG1_MOV2
            # Go left
            if self.rect.x != -40 and self.rect.y == 360:
                self.rect.x -= BUG1_MOV2
                # Once off screen, remove sprite from game
                if self.rect.x <= -40:
                    self.kill()

        # Shoots wherever x coordinate can be cleanly modulated by the number represented
        # by BUG1_FIRE.
        if (self.rect.x % BUG1_FIRE == 0):
            # Creates bug laser (blaser)
            blaser = B1Laser()
            # Set laser to appear from the player's image's center
            blaser.rect.x = self.rect.x + 24
            blaser.rect.y = self.rect.y + 40
            # Add laser to the ALL SPRITES group as it's made
            asp.add(blaser)
            # Add laser to the Lasers group as it's made
            blasers.add(blaser)

    """COLIN: I think it'd be cool if we had a level where the bug type 1 just closed in the player at different y intervals
    while showering down laserfire. You'd have to make it shoot in an infinite loop though"""

#-----[ BUG TYPE 1 LASER SPRITE CLASS ]-----
class B1Laser(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Creates a rectangle with width and height of 4 and fills it with predefined color RED
        self.image = pygame.Surface([4,10])
        self.image.fill(GREEN)
        # Creates a rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()

    # Updates the sprite's movements
    def update(self):
        # Move the sprite down
        self.rect.y += 7
        # Remove laser from screen if it reaches y = 400
        if self.rect.y > 400:
            self.kill()

#-----[ BUG TYPE 2 SPRITE CLASS]-----
class BugT2(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Grabs the predefined variable from up top that represents the bug's image
        self.image = BUG2
        # Creates rectangle for the sprite and tracks coordinates
        self.rect = self.image.get_rect()

    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Update the sprite's movement
    def update(self):
        # Go down the screen until y coordinate == 200
        if self.rect.y != 200 and len(b2lasers) != 10:
            self.rect.y += 1
       # If it reaches y coordiante 50, 100, or 200:
        if self.rect.y == 50 or self.rect.y == 100 or self.rect.y == 200:
            # Make a laser
            blaser = B2Laser()
            # Set laser to appear from center of sprite image
            blaser.rect.x = self.rect.x + 28
            blaser.rect.y = self.rect.y + 60
            # Add laser to the ALL SPRITES group as it's made
            asp.add(blaser)
            # Add laser to the Bug Lasers group as it's made
            blasers.add(blaser)
            # add 1 to the list of how many lasers Bug Type 2 can fire
            b2lasers.append("1")
        # If y coordinate == 200 and the length of the list of fired lasers > 80:
        if self.rect.y == 200 and len(b2lasers) > 80:
            # Stop firing, and continue down the screen
            self.rect.y += 1
        if self.rect.y > 400:
            self.kill()

#-----[ BUG TYPE 2 LASER SPRITE CLASS ]-----
class B2Laser(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Creates a rectangle with width and height of 4 and fills it with predefined color RED
        self.image = pygame.Surface([10,80])
        self.image.fill(GREEN)
        # Creates a rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()

    # Updates the sprite's movements
    def update(self):
        # Move the bug's laser down
        self.rect.y += 3
        # Delete the laser if it reaches bottom of screen
        if self.rect.y > 400:
            self.kill()

#-----[ BUG TYPE 3 SPRITE CLASS]-----
class BugT3(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Grabs the predefined variable from up top that represents the bug's image
        self.image = BUG3
        # Creates rectangle for the sprite and tracks coordinates
        self.rect = self.image.get_rect()

    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        # Go down the screen until y coordinate == 200
        if self.rect.y != 360:
            self.rect.y += 5
        if self.rect.x < 400 and self.rect.y == 360:
            self.rect.x += 10
        if self.rect.x > 400 and self.rect.y == 360:
            self.rect.x -= 10
        # Remove sprite if it goes offscreen
        if self.rect.x == 400:
            self.kill()

#-----[ SPAWNING FUNCTION ]-----
# Spawns all of the enemies at once. Most are off screen and will travel down at various speeds
def spawn():
    # 1st wave: Bug type 1's
    # Incrementer for space between sprites
    b = 0
    # Spawn 20 enemies
    for i in range(1, 21):
        # create a bug 1 type
        b1 = BugT1()
        # add it to the all sprites list
        asp.add(b1)
        # add it to the enemy sprite list
        enemy.add(b1)
        # set its initial coordinates to (-80,0)
        # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug
        b1.rect.x = -80 * b
        b1.rect.y = 0
        b += 1

    # 2nd Wave: Bug Type 2's
    # Incrementer for space between sprites
    s = 0
    # Spawn 4 enemies
    for i in range(1, 11):
        # Create a bug type 2
        b2 = BugT2()
        # add it to all sprites list
        asp.add(b2)
        # add it to enemy list
        enemy.add(b2)

        # Place offscreen
        # Everytime a bug gets spawned, s is incremented by 1, so 100 pixels of space is made between each bug
        b2.rect.x = 100 * s
        b2.rect.y = -500
        s += 1

    # Additions: Bug Type 3's
    for i in range(1, 10):
        # Create Bug Type 3's, add them to appropriate lists
        b3 = BugT3()
        asp.add(b3)
        enemy.add(b3)
        # Chooses a random integer between 1,2
        spawn = random.randint(1,7)
        # If 1, spawn on left side of screen
        if spawn > 3:
            b3.rect.x = 0
        # If 2, spawn on right side of screen
        if spawn < 3:
            b3.rect.x = 760
        # Set y = -500 (offscreen)
        b3.rect.y = -800

    # 3rd Wave: More Bug Type 1's
    # Incrementer
    b = 50
    # Spawn 20 enemies
    for i in range(1, 21):
        # create a bug 1 type
        b1 = BugT1()
        # add it to the all sprites list
        asp.add(b1)
        # add it to the enemy sprite list
        enemy.add(b1)
        # set its initial coordinates to (-80,0)
        # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug
        b1.rect.x = -80 * b
        b1.rect.y = 0
        b += 1


def buttons(x):
    return x

#=====[ MAIN GAME LOOP ]=====
# COLIN: Here is where the game is run. It sets up the foundation of the pygame, then refers to several
# classes and functions to display the pygame.
#-----[ MAIN LOOP ]-----
def main():
    # Run set to True so the game doesn't end
    run = True
    # Sets the Frame Rate
    FPS = 35
    # Creates a clock that makes sure computer runs program at desired FPS
    clock = pygame.time.Clock()

    #-----[ SPRITE SPAWNING]-----
    # create player at desired coordinates (400, 360) and add to appropriate sprite groups
    player1 = Player(3)
    p1alive = 1
    asp.add(player1)
    ship.add(player1)
    player1.rect.x = 400
    player1.rect.y = 360

    # Attempt to spawn a second player
    player2 = Player(3)


    # Calls the function to spawn all the enemies off screen
    spawn()

    #-----[ DISPLAY FUNCTION ]----
    # This function, nested into the main loop, displays everything
    def display():
        if p1alive == 0:
            asp.add(player2)
            ship.add(player2)
            player2.rect.x = 400
            player2.rect.y = 360
        # Blit (draw an object) the background at coordinates (0,0)
        WIN.blit(BG, (0,0))
        # Draws all of the sprites in the ALL SPRITES group
        asp.draw(WIN)
        # Calls the update function fdrom any sprites in the ALL SPRITES group
        asp.update()

        # GAME OVER screen
        if p1alive == 0 and p2alive == 0:
            # empty all sprites list
            pygame.sprite.Group.empty(asp)
            # Create a font and font size
            font = pygame.font.Font(None, 36)
            # Create text and color it (Boolean makes text clearer I think)
            text = font.render("Game OVER!", True, WHITE)
            # Create coordiantes for text
            textRect = text.get_rect()
            textRect.center = (400, 200)
            # Draw text on window
            WIN.blit(text, textRect)

        # Updates the window
        pygame.display.update()

    #-----[ MUSIC FUNCTION ]-----
    def music():
        MUSIC_FILE = ("game_music.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play()

    # Calls the music function
    music()

    #-----[ GAME LOGIC ]-----
    # Game loop for key controls
    while run:
        for i in range(len(but)):
            if (GPIO.input(but[i])):
                print("{}".format(but[i]))

                if but[i] == 20:
                    print("SHOOT")
                    
    
        # Sets the game to reset at the desired frames per second
        clock.tick(FPS)

        #-----[ GAME EVENTS ]-----
        # Player closes window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Run is set to False; main loop stops
                run = False

            #-----[ PLAYER LASER FIRE BUTTON ]-----
                
                if event.type == pygame.KEYDOWN:
                    # If the player hits the fire button and has health remaining
                    if event.key == pygame.K_SPACE and p1alive == 1:
                        # Set laser variable to the Laser class
                        laser = Laser()
                        # Set laser to appear from player's coordinates
                        laser.rect.x = player1.rect.x + 24
                        laser.rect.y = player1.rect.y
                        # Add laser to the ALL SPRITES group as it's made
                        asp.add(laser)
                        # Add laser to the Lasers group as it's made
                        lasers.add(laser)
                        # Troubleshooting: Print Statement to Track if the spacebar is allowing player to fire
                        # print("Fire!")
                        pygame.mixer.Sound.play(FIRE)


        #-----[ PLAYER'S LASERS / BUGS COLLISION ]-----
        # Collision between Player's lasers and enemies
        for laser in lasers:
            # Create a list that removes laser and enemy once they collide
            # The boolean, if set to true, removes both sprites.
            enemyhit = pygame.sprite.spritecollide(laser, enemy, True)
            for laser in enemyhit:
                asp.remove(laser)
                lasers.remove(laser)
                print("HIT!")

        #-----[ BUG'S LASERS / PLAYER(S) COLLISION ]-----
        """COLIN: Slight issue. The bugs' lasers disappear whenever they reach the player's last location after
        they're killed. Maybe this isn't a big problem, but it could be for co op"""
        # Collision between the Bug's lasers and the player
        for blaser in blasers:
            playerhit = pygame.sprite.spritecollide(blaser, ship, False)
            blasergone = pygame.sprite.spritecollide(player1, blasers, True)
            for player1 in playerhit:
                player1.health -= 1
                print("OUCH!")
                pygame.mixer.Sound.play(HIT)
                if player1.health <= 0:
                    player1.kill()
                    asp.remove(player1)
                    ship.remove(player1)
                    p1alive = 0
                if player1.health > 0:
                    asp.add(player1)
                    ship.add(player1)
            for player1 in blasergone:
                blaser.kill()

        #-----[ BUG TYPE 1 / PLAYER SHIP COLLISION ]------
        for b1 in enemy:
            crash = pygame.sprite.spritecollide(b1, ship, False)
            for player1 in crash:
                enemy.remove(b3)
                asp.remove(b3)
                player1.health -= 1
                print("OUCH!")
                pygame.mixer.Sound.play(HIT)
                if player1.health <= 0:
                    player1.kill()
                    asp.remove(player1)
                    ship.remove(player1)
                    p1alive = 0
                if player1.health > 0:
                    asp.add(player1)
                    ship.add(player1)

        # -----[ BUG TYPE 2 / PLAYER SHIP COLLISION ]------
        for b2 in enemy:
            crash = pygame.sprite.spritecollide(b2, ship, False)
            for player1 in crash:
                player1.health -= 1
                print("OUCH!")
                enemy.remove(b3)
                asp.remove(b3)
                pygame.mixer.Sound.play(HIT)
                if player1.health <= 0:
                    player1.kill()
                    asp.remove(player1)
                    ship.remove(player1)
                    p1alive = 0
                if player1.health > 0:
                    asp.add(player1)
                    ship.add(player1)

        # -----[ BUG TYPE 3 / PLAYER SHIP COLLISION ]------
        for b3 in enemy:
            crash = pygame.sprite.spritecollide(b3, ship, False)
            for player1 in crash:
                player1.health -= 1
                print("OUCH!")
                enemy.remove(b3)
                asp.remove(b3)
                pygame.mixer.Sound.play(HIT)
                if player1.health <= 0:
                    player1.kill()
                    asp.remove(player1)
                    ship.remove(player1)
                    p1alive = 0
                if player1.health > 0:
                    asp.add(player1)
                    ship.add(player1)

        #-----[ PLAYER MOVEMENT ]-----
        # Tracks keys being pressed and restricts player from exiting window
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and player1.rect.x - PIX > 0 and p1alive == 1:
            player1.moveLeft(PIX)
        if keys_pressed[pygame.K_d] and player1.rect.x + PIX + 55 < 799 and p1alive == 1:
            player1.moveRight(PIX)
        if keys_pressed[pygame.K_w] and player1.rect.y > 0 and p1alive == 1:
            player1.moveUp(PIX)
        if keys_pressed[pygame.K_s] and player1.rect.y < 360 and p1alive == 1:
            player1.moveDown(PIX)

        # LEDS
        if player1.health == 3:
            GPIO.output(leds, True)
            print("LED ON")
        if player1.health == 2:
            GPIO.output(13, False)
            GPIO.output((16, 17), True)
        if player1.health == 1:
            GPIO.output((13, 16), False)
            GPIO.output(17, True)
        if p1alive == 0:
            GPIO.output(leds, False)
            print("LED OFF")
        # Calls the display function
        display()

#=====[ LAUNCH GAME ]=====
# Calls main loop
main()
