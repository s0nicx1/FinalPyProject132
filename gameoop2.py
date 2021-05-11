""" THIS VERSION IS FOR DEVELOPMENT PURPOSES"""
""" THE FINAL, RPi-COMPATIBLE VERSION IS gameoopRPi.py"""

# Import pygame and random module
import pygame
import random

# Initialize the pygame module
pygame.init()

#=====[ IMAGES & AUDIO ]=====
# Grabs and adjusts the image to fit onto the screen with desired (width, height)
PLAYER1 = pygame.image.load("p1.png")
PLAYER1 = pygame.transform.scale(PLAYER1, (55, 40))

# Grabs and adjusts the image for player 2
PLAYER2 = pygame.image.load("p2.png")
PLAYER2 = pygame.transform.scale(PLAYER2, (55, 40))

# Grabs and adjusts image for the Bug Type 1
BUG1 = pygame.image.load("b1.png")
BUG1 = pygame.transform.scale(BUG1, (55, 40))

# Grabs and adjusts secondary image for Bug Type 1
BUG1A = pygame.image.load("b1a.png")
BUG1A = pygame.transform.scale(BUG1A, (55, 40))

# Grabs and adjusts image for centipede variation of Bug Type 1
BUG1B = pygame.image.load("b1b.png")
BUG1B = pygame.transform.scale(BUG1B, (55, 40))

# Grabs and adjusts image for centipede variation of Bug Type 1
BUG1C = pygame.image.load("b1c.png")
BUG1C = pygame.transform.scale(BUG1C, (55, 40))

# Grabs and adjusts image for centipede variation of Bug Type 1
BUG1D = pygame.image.load("b1c.png")
BUG1D = pygame.transform.scale(BUG1C, (55, 40))
BUG1D = pygame.transform.rotate(BUG1C, 180)

# Grabs and adjusts image for Bug Type 2
BUG2 = pygame.image.load("b2.png")
BUG2 = pygame.transform.scale(BUG2, (65, 80))

# Grabs and adjusts secondary image for Bug Type 2
BUG2A = pygame.image.load("b2a.png")
BUG2A = pygame.transform.scale(BUG2A, (65, 80))

# Grabs and adjusts image for left variation of Bug Type 2
BUG2L = pygame.image.load("b2.png")
BUG2L = pygame.transform.scale(BUG2, (65, 80))
BUG2L = pygame.transform.rotate(BUG2, 90)

# Grabs and adjusts image for right variation of Bug Type 2
BUG2R = pygame.image.load("b2.png")
BUG2R = pygame.transform.scale(BUG2, (65, 80))
BUG2R = pygame.transform.rotate(BUG2, 270)

# Grabs and adjusts image for Bug Type 3
BUG3 = pygame.image.load("b3.png")
BUG3 = pygame.transform.scale(BUG3, (55, 40))

# Grabs and adjusts image for Bug Type 4
BUG4 = pygame.image.load("b4.png")
BUG4 = pygame.transform.scale(BUG4, (55, 40))

# Grabs and adjusts image for the Boss
BOSS = pygame.image.load("boss.png")
BOSS = pygame.transform.scale(BOSS, (300, 150))

# Grabs and adjusts  image for the damaged Boss
BOSS_D1 = pygame.image.load("boss_damage1.png")
BOSS_D1 = pygame.transform.scale(BOSS_D1, (300, 150))

# Grabs and adjusts  image for the damaged Boss
BOSS_D2 = pygame.image.load("boss_damage2.png")
BOSS_D2 = pygame.transform.scale(BOSS_D2, (300, 150))

# Grabs and adjusts  image for the damaged Boss
BOSS_D3 = pygame.image.load("boss_damage3.png")
BOSS_D3 = pygame.transform.scale(BOSS_D3, (300, 150))

# Grab image for first background
BG = pygame.image.load("space.jpg")
# This is a good background. use it
BG2 = pygame.image.load("space4.png")
BG3 = pygame.image.load("N2D Space.png")


# Grabs sound for laser fire
FIRE = pygame.mixer.Sound("laserfire.wav")
HIT = pygame.mixer.Sound("Explosion.wav")
BUZZ = pygame.mixer.Sound("buzz.wav")
DEATH = pygame.mixer.Sound("death.wav")

#=====[ VARIABLES AND LISTS ]=====
# The following constant variables represent RGB values for colors
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255,255,0)

#-----[ ON SCREEN BUTTONS ]-----
# Constant variable for button (rectangle) height
BUTTON_H = 40
# Constant variable for button (rectangle) width
BUTTON_W = 150
# Text color (WHITE)
text_color = (255, 255, 255)
# Default button color (LIGHT GREY)
button_color = (200, 200, 200)
# Secondary button color (highlighted) (DARK GREY)
button_color_2 = (100, 100, 100)
# Text font and size
font = pygame.font.Font('8-BitMadness.ttf', 40)
# 1-Player text
one_player_text = font.render('1-Player', True, text_color)
# 2-Player text
two_player_text = font.render('2-Player', True, text_color)
# QUIT text
quit_text = font.render('quit', True, text_color)

# This list represents the amount of time the Bug Type 2 has fired, and its limits can be adjusted accordingly to match
# level difficulty
b2lasers = []
# These lists keep track with how many times the boss has fired from each blaster (going left to right) and resets
# itself in the Boss sprite class so it can fire, pause, fire again.
bossblaster1 = []
bossblaster2 = []
bossblaster3 = []
bossblaster4 = []

# This constant variable represents the amount of pixels Bug Type 1's travel per frame.
# CAN BE ADJUSTED LATER FOR DIFFICULTY
# Top half of the screen (y < 200)
BUG1_MOV1 = 5
# Bottom half of the screen (y > 200)
BUG1_MOV2 = 10

# These constant variables represent the x-coordinates where the Bug Type 1 should bounce off of.
R_EDGE = 745
L_EDGE = -5

# This constant variable represents the number the Bug Type 1s' coordinates can be modulated by to fire.
# Basically, it's the bug's fire rate. The lower the number, the faster it fires. This can be adjusted per difficulty
"""COLIN: BUG TYPE 1 WILL NOT FIRE once movement speed is updated if this remains == 110"""


#=====[ SPRITE GROUPS ]=====
# Pygame's groupings (lists) of sprites
# This creates a pygame group for (A)LL (SP)RITES
asp = pygame.sprite.Group()
# This creates a pygame group for player in Solo
ship = pygame.sprite.Group()
# This creates a pygame group for player1 in Co-op
ship1 = pygame.sprite.Group()
# This creates a pygame group for player2 in Co-op
ship2 = pygame.sprite.Group()
# This creates a pygame group for the player's/players' lasers
lasers = pygame.sprite.Group()
# This creates a pygame group for the bugs' lasers
blasers = pygame.sprite.Group()
# This creates a pygame group for the first bug type
bug1 = pygame.sprite.Group()
# This creates a pygame group for the second bug type
bug2 = pygame.sprite.Group()
# This creates a pygame group for the third bug type
bug3 = pygame.sprite.Group()
# This creates a pygame group for the fourth bug type
bug4 = pygame.sprite.Group()
# This creates a pygame group for the boss bug type
boss1 = pygame.sprite.Group()

#=====[ CREATE WINDOW ]======
# Constant variable for window's width (800) and height (400); RPi screen size
SIZE = 800, 400
# Constant variable for pygame creating the window
WIN = pygame.display.set_mode(SIZE)
# Sets caption for upper left corner of window
pygame.display.set_caption("Tech Universe: Re")
# Constant variables for window's width and height for buttons
WIDTH = WIN.get_width() # 800
HEIGHT = WIN.get_height() # 400

# Dictionary that keeps and updates game variables
status = {
    # Key for if player1 is alive
    "p1alive": 0,
    # Key for if player2 is alive
    "p2alive": 0,
    # Key to show if game has started
    "start": 0,
    # Key to show if co-op was selected
    "coop": 0,
    # Key to track if ending boss' health == 0
    "bossdead": 0,
    # Key that defines Bug Type 1's fire rate
    "bug1fr": 110,
    # Keys that iterate
    "counter": 0,
    "points": 0,
}


#=====[ CLASSES ]=====
#-----[ PLAYER SPRITE CLASS ]-----
class Player1(pygame.sprite.Sprite):
    # Constructor for Player Sprite
    def __init__(self, health):
        # Call the fancy pygame sprite parent class
        super().__init__()
        # instance variable to grab player image
        self.image = PLAYER1
        # Creates the hitbox and tracks coordinates for the player
        self.rect = self.image.get_rect()
        # Instance variable for player's health
        self.health = health

    # Player movement functions
    # Function that moves the player  when called
    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.rect.x - 5 > 0:
            self.rect.x -= 5
        if keys_pressed[pygame.K_d] and self.rect.x + 5 + 55 < 799:
            self.rect.x += 5
        if keys_pressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= 5
        if keys_pressed[pygame.K_s] and self.rect.y < 360:
            self.rect.y += 5

#-----[ PLAYER 2 SPRITE CLASS ]-----
class Player2(pygame.sprite.Sprite):
    # Constructor for Player Sprite
    def __init__(self, health):
        # Call the fancy pygame sprite parent class
        super().__init__()
        # instance variable to grab player image
        self.image = PLAYER2
        # Creates the hitbox and tracks coordinates for the player
        self.rect = self.image.get_rect()
        # Instance variable for player's health
        self.health = health

    # Player movement functions
    # Function that moves the player  when called
    def move(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT] and self.rect.x - 5 > 0:
            self.rect.x -= 5
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + 5 + 55 < 799:
            self.rect.x += 5
        if keys_pressed[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= 5
        if keys_pressed[pygame.K_DOWN] and self.rect.y < 360:
            self.rect.y += 5

#-----[ PLAYER 1 LASER SPIRTE CLASS ]-----
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

#-----[ PLAYER 2 LASER SPIRTE CLASS ]-----
class Laser2 (pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Creates a rectangle with width and height of 4 and fills it with predefined color RED
        self.image = pygame.Surface([4, 4])
        self.image.fill(CYAN)
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
    def __init__(self, health):
        # Calls pygame's sprite class
        super().__init__()
        # makes an empty list for images
        self.images = []
        # Adds default, pre-defined image to list of images
        self.images.append(BUG1)
        # Adds second, pre-defined image to list of images
        self.images.append(BUG1A)
        # Adds a third, pre-defined image to list of images
        self.images.append(BUG1B)
        # Adds a fourth, pre-defined image to list of images
        self.images.append(BUG1C)
        # Adds a fifth, predefined images to list of images
        self.images.append(BUG1D)
        # Creates index variable to sort through list
        self.index = 0
        # Picks image for sprite that correlates with index number (0 = BUG1, 1 = BUG1A)
        self.image = self.images[self.index]
        # Creates rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()
        # Instance variable that acts as a boolean for the for loop below
        self.move = 1
        self.health = health


    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Update the sprite's movement
    def update(self):
        for i in range(self.move):
            # Move from off screen
            if self.rect.x < L_EDGE and self.rect.y == 0:
                self.rect.x += BUG1_MOV1
            if self.rect.x > R_EDGE and self.rect.y == 0:
                self.rect.x -= BUG1_MOV1
            # Go right once on screen
            if L_EDGE <= self.rect.x < R_EDGE and self.rect.y == 0:
                self.rect.x += BUG1_MOV1
            # Go down (x >= edge coordinate and (prev y value =< counter y value < next y value))
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
                if self.image == self.images[0]:
                    self.image = self.images[1]
                # If it's a centipede, keep centipede image
                if self.image == self.images[2]:
                    self.image = self.images[2]
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
        if (self.rect.x % status["bug1fr"] == 0):
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
    def __init__(self, health):
        # Calls pygame's sprite class
        super().__init__()
        self.health = health
        # Grabs the predefined variable from up top that represents the bug's image
        self.images = []
        # Default image at index 0
        self.images.append(BUG2)
        # Secondary (Damaged) image at index 1
        self.images.append(BUG2A)
        # Left variation at index 2
        self.images.append(BUG2L)
        # Right variation at index 3
        self.images.append(BUG2R)
        self.index = 0
        self.image = self.images[self.index]
        # Creates rectangle for the sprite and tracks coordinates
        self.rect = self.image.get_rect()

    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Update the sprite's movement
    def update(self):
        # If health decreases, choose secondary image
        if self.health == 1:
            self.image = self.images[1]

        # If BT2 is between the edges of the screen:
        # Go down the screen until y coordinate == 200
        if L_EDGE < self.rect.x < R_EDGE:
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
    def __init__(self,health):
        # Calls pygame's sprite class
        super().__init__()
        # Grabs the predefined variable from up top that represents the bug's image
        self.image = BUG3
        # Creates rectangle for the sprite and tracks coordinates
        self.rect = self.image.get_rect()
        self.health = health

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

#-----[ BUG TYPE 4 SPRITE CLASS]-----
class BugT4(pygame.sprite.Sprite):
    def __init__(self, health):
        # Calls pygame's sprite class
        super().__init__()
        # Grabs the predefined variable from up top that represents the bug's image
        self.image = BUG4
        # Creates rectangle for the sprite and tracks coordinates
        self.rect = self.image.get_rect()
        self.health = health
    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        # Go down the screen until y coordinate == 200
        if self.rect.x != 800:
            self.rect.x += 5
        # Remove sprite if it goes offscreen
        if self.rect.x == 800:
            self.kill()

#-----[ BOSS SPRITE CLASS ]-----
class Boss(pygame.sprite.Sprite):
    def __init__(self, health):
        # Calls pygame's sprite class
        super().__init__()
        # Grabs the predefined variable from up top that represents the bug's image
        self.images = []
        # Default image at index 0
        self.images.append(BOSS)
        # Second image at index 1
        self.images.append(BOSS_D1)
        # Third image at index 2
        self.images.append(BOSS_D2)
        # Fourth image at index 3
        self.images.append(BOSS_D3)
        self.index = 0
        self.image = self.images[self.index]
        # Creates rectangle for the sprite and tracks coordinates
        self.rect = self.image.get_rect()
        self.health = health

    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Update the sprite's movement
    def update(self):
        # Extra Audio:
        # Each time the boss's image updates, play death sound for audio impact
        if self.health == 30:
            pygame.mixer.Sound.play(DEATH)
        if self.health == 20:
            pygame.mixer.Sound.play(DEATH)
        if self.health == 10:
            pygame.mixer.Sound.play(DEATH)

        # Boss Image:
        # If the boss's health ranges between certain numbers, update the image so damage is visible
        if 30 < self.health <= 40:
            self.image = self.images[0]
        if 20 < self.health <= 30:
            self.image = self.images[1]
        if 10 < self.health <= 20:
            self.image = self.images[2]
        if 0 < self.health <= 10:
            self.image = self.images[3]

        # Boss Movement:
        # Go down the screen until y coordinate == 50
        if self.rect.y != 50:
            self.rect.y += 1

        # Boss Firing:
        if self.rect.y == 50:

            # If health is above 20 (screen left wing visible), fire blasters 1 and 2
            if self.health > 20:
                # BLASTER 1:
                # Fire until list reaches MINIMUM length
                if len(bossblaster1) < 110:
                    blaser = BOSSLaser()
                    blaser.rect.x = 265
                    blaser.rect.y = 180
                    asp.add(blaser)
                    blasers.add(blaser)
                    # Add to the list each time blaster is fired
                    bossblaster1.append("1")
                # Once past the appropriate length, keep adding to the list
                if 110 <= len(bossblaster1) < 180:
                    bossblaster1.append("1")
                # If list reaches MAXIMUM length, clear all the elements of the list
                if len(bossblaster1) == 180:
                    bossblaster1.clear()

                # BLASTER 2:
                if len(bossblaster2) < 80:
                    blaser = BOSSLaser()
                    blaser.rect.x = 345
                    blaser.rect.y = 180
                    asp.add(blaser)
                    blasers.add(blaser)
                    bossblaster2.append("1")
                if 80 <= len(bossblaster2) < 150:
                    bossblaster2.append("1")
                if len(bossblaster2) == 150:
                    bossblaster2.clear()


            # If health is above 10 (screen right wing visible), fire blasters 3 and 4
            if self.health > 10:
                # BLASTER 3:
                if len(bossblaster3) < 110:
                    blaser = BOSSLaser()
                    blaser.rect.x = 525
                    blaser.rect.y = 180
                    asp.add(blaser)
                    blasers.add(blaser)
                    bossblaster3.append("1")
                if 110 <= len(bossblaster3) < 180:
                    bossblaster3.append("1")
                if len(bossblaster3) == 180:
                    bossblaster3.clear()

                # BLASTER 4:
                if len(bossblaster4) < 80:
                    blaser = BOSSLaser()
                    blaser.rect.x = 450
                    blaser.rect.y = 180
                    asp.add(blaser)
                    blasers.add(blaser)
                    bossblaster4.append("1")
                if 80 <= len(bossblaster4) < 150:
                    bossblaster4.append("1")
                if len(bossblaster4) == 150:
                    bossblaster4.clear()

#-----[ BOSS LASER SPRITE CLASS ]-----
class BOSSLaser(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Creates a rectangle with width and height of 4 and fills it with predefined color RED
        self.image = pygame.Surface([10,80])
        self.image.fill(CYAN)
        # Creates a rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()

    # Updates the sprite's movements
    def update(self):
        # Move the bug's laser down
        self.rect.y += 3
        # Delete the laser if it reaches bottom of screen
        if self.rect.y > 400:
            self.kill()

#=====[ MAIN GAME LOOP ]=====
# COLIN: Here is where the game is run. It sets up the foundation of the pygame, then refers to several
# classes and functions to display the pygame.

#-----[ MAIN LOOP ]-----
def main():
    # creates a player sprites (but doesn't display them just yet)
    player1 = Player1(3)
    player2 = Player2(3)
    # Iterating variable (controls enemy spawn and background changes)
    status["counter"] = 0
    # Empty variable for points (iterated per enemy shot)
    status["points"] = 0
    # Run set to True so the game doesn't end
    run = True
    # Sets the Frame Rate (RPi friendly)
    FPS = 35
    # Creates a clock that makes sure computer runs program at desired FPS
    clock = pygame.time.Clock()

    # -----[ DISPLAY FUNCTION ]-----
    def display(status):

        #-----[ MAIN MENU ]-----
        if status["p1alive"] == 0 and status["start"] == 0:
            # Draw background
            WIN.blit(BG, (0, 0))
            # Title text
            text = font.render("TECH UNIVERSE: ", True, text_color)
            text2 = font.render("Re", True, CYAN)
            # draw the rectangle (surface, color, [x,y,width,height]
            pygame.draw.rect(WIN, BLACK, [320, 170, 50, 50])
            # Create coordinates for text
            textRect = text.get_rect()
            textRect.center = (200, 200)
            # Draw text on window
            WIN.blit(text, textRect)
            WIN.blit(text2, (325, 185))

            #-----[ MAIN MENU BUTTONS ]-----

            # [SINGLE PLAYER BUTTON]
            # Blit it on screen, default color, x = 400, y = 150, w = 150, h = 40
            pygame.draw.rect(WIN, button_color, [WIDTH / 2, 150, BUTTON_W, BUTTON_H])
            # SINGLE PLAYER BUTTON HIGHLIGHT
            # If mouse is over button, draw with secondary color
            if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and 150 < mouse[1] < 190:
                pygame.draw.rect(WIN, button_color_2, [WIDTH / 2, 150, BUTTON_W, BUTTON_H])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # -----[ SPAWN PLAYER 1]-----
                    status["p1alive"] = 1
                    asp.add(player1)
                    ship.add(player1)
                    player1.rect.x = 400
                    player1.rect.y = 360
                    status["start"] = 1

            # [CO-OP BUTTON]
            # Blit it on screen, default color, x = 400, y = 150, w = 150, h = 40
            pygame.draw.rect(WIN, button_color, [WIDTH / 2, HEIGHT / 2, BUTTON_W, BUTTON_H])
            # CO-OP BUTTON (HIGHLIGHT)
            # If mouse is over button, draw with secondary color
            if (WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140) and (HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40):
                # Draw the same button, but use secondary color
                pygame.draw.rect(WIN, button_color_2, [WIDTH / 2, HEIGHT / 2, BUTTON_W, BUTTON_H])
                # If button is pressed while over button, que appropriate action.
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # -----[ SPAWN PLAYERS]-----
                    status["coop"] = 1
                    status["p1alive"] = 1
                    status["p2alive"] = 1
                    asp.add(player1)
                    ship1.add(player1)
                    asp.add(player2)
                    ship2.add(player2)
                    player1.rect.x = 400
                    player1.rect.y = 360
                    player2.rect.x = 480
                    player2.rect.y = 360
                    status["start"] = 1

            # [QUIT THE GAME BUTTON]
            # Blit it on screen, default color, x = 400, y = 150, w = 150, h = 40
            pygame.draw.rect(WIN, button_color, [WIDTH / 2, 250, BUTTON_W, BUTTON_H])
            # QUIT BUTTON (HIGHLIGHT)
            # If mouse is over button, draw with secondary color
            if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and 250 <= mouse[1] <= 290:
                # Draw the same button, but use secondary color
                pygame.draw.rect(WIN, button_color_2, [WIDTH / 2, 250, BUTTON_W, BUTTON_H])
                # If button is pressed while over QUIT BUTTON, Exit game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()

            # -----[ BUTTON TEXTS ]-----
            """Must be called after button color changes, as it must appear OVER THEM"""
            # 1-PLAYER TEXT
            WIN.blit(one_player_text, (WIDTH / 2, 150 + 6))
            # 2- PLAYER TEXT
            WIN.blit(two_player_text, (WIDTH / 2, HEIGHT / 2 + 6))
            # QUIT TEXT
            WIN.blit(quit_text, (WIDTH / 2 + 40, 250 + 6))

        #-----[ GAME PROGRESSION ]-----
        # SOLO:
        if status["coop"] == 0:
            if status["p1alive"] == 1 and status["start"] == 1:
                # Level 1 (BG)
                if status["counter"] < 1200:
                    WIN.blit(BG, (0, 0))
                # Level 2 (BG2)
                if 1200 < status["counter"] < 1800:
                    WIN.blit(BG2, (0, 0))
                if status["counter"] > 1800:
                    WIN.blit(BG3, (0,0))
        # CO-OP:
        if status["coop"] == 1:
            if status["p1alive"] == 1 or status["p2alive"] == 1 and status["start"] == 1:
                # Level 1 (BG)
                if status["counter"] < 1200:
                    WIN.blit(BG, (0, 0))
                # Level 2 (BG2)
                if 1200 < status["counter"] < 1800:
                    WIN.blit(BG2, (0, 0))
                if status["counter"] > 1800:
                    WIN.blit(BG3, (0, 0))

        #-----[ GAME OVER ]-----
        # SOLO LOSS!:
        if status["coop"] == 0:
            # PLAYER LOSES:
            if status["p1alive"] == 0 and status["start"] == 1:
                # empty all the sprites list
                pygame.sprite.Group.empty(asp)
                pygame.sprite.Group.empty(ship)
                pygame.sprite.Group.empty(lasers)
                pygame.sprite.Group.empty(blasers)
                pygame.sprite.Group.empty(bug1)
                pygame.sprite.Group.empty(bug2)
                pygame.sprite.Group.empty(bug3)
                pygame.sprite.Group.empty(bug4)
                pygame.sprite.Group.empty(boss1)

                # Create text and color it (Boolean makes text clearer I think)
                text = font.render("Game OVER!", True, text_color)
                # Create coordinates for text
                textRect = text.get_rect()
                textRect.center = (400, 200)
                # Draw text on window
                WIN.blit(text, textRect)

                score = font.render(" SCORE: {}".format(status["points"]),True, RED)
                scoreRect = score.get_rect()
                scoreRect.center = (400,250)
                WIN.blit(score,scoreRect)

                # -----[ QUIT TO MAIN MENU BUTTON ]-----
                # Blit it on screen, default color, x = 400, y = 200, w = 140, h = 40
                pygame.draw.rect(WIN, button_color, [330, 300, 140, 40])
                # QUIT BUTTON (HIGHLIGHT)
                # If 400 < mouse x coordinate < 540 and 200 < mouse y coordinate < 240
                if 330 <= mouse[0] <= 470 and 300 <= mouse[1] <= 340:
                    # Draw the same button, but use secondary color
                    pygame.draw.rect(WIN, button_color_2, [330, 300, 140, 40])
                    # If button is pressed while over QUIT BUTTON, Exit game
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        status["p1alive"] = 0
                        status["start"] = 0
                        status["counter"] = 0
                        status["points"] = 0
                        status["bossdead"] = 0
                # -----[ BUTTON TEXTS ]-----
                """Must be called after button color changes, as it must appear OVER THEM"""
                # QUIT TEXT
                WIN.blit(quit_text, (370, 305))
        # SOLO WIN!:
        if status["coop"] == 0:
            # PLAYER WINS!!!
            if status["bossdead"] == 1 and status["start"] == 1:
                # empty all the sprites list
                pygame.sprite.Group.empty(asp)
                pygame.sprite.Group.empty(ship)
                pygame.sprite.Group.empty(lasers)
                pygame.sprite.Group.empty(blasers)
                pygame.sprite.Group.empty(bug1)
                pygame.sprite.Group.empty(bug2)
                pygame.sprite.Group.empty(bug3)
                pygame.sprite.Group.empty(bug4)
                pygame.sprite.Group.empty(boss1)

                # Create text and color it (Boolean makes text clearer I think)
                text = font.render("CONGRATULATIONS!", True, text_color)
                # Create coordinates for text
                textRect = text.get_rect()
                textRect.center = (400, 200)
                # Draw text on window
                WIN.blit(text, textRect)

                score = font.render(" SCORE: {}".format(status["points"]),True, RED)
                scoreRect = score.get_rect()
                scoreRect.center = (400,250)
                WIN.blit(score,scoreRect)

                # -----[ QUIT TO MAIN MENU BUTTON ]-----
                # Blit it on screen, default color, x = 400, y = 200, w = 140, h = 40
                pygame.draw.rect(WIN, button_color, [330, 300, 140, 40])
                # QUIT BUTTON (HIGHLIGHT)
                # If 400 < mouse x coordinate < 540 and 200 < mouse y coordinate < 240
                if 330 <= mouse[0] <= 470 and 300 <= mouse[1] <= 340:
                    # Draw the same button, but use secondary color
                    pygame.draw.rect(WIN, button_color_2, [330, 300, 140, 40])
                    # If button is pressed while over QUIT BUTTON, Exit game
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        status["p1alive"] = 0
                        status["start"] = 0
                        status["counter"] = 0
                        status["points"] = 0
                        status["bossdead"] = 0

                # -----[ BUTTON TEXTS ]-----
                """Must be called after button color changes, as it must appear OVER THEM"""
                # QUIT TEXT
                WIN.blit(quit_text, (370, 305))

        # CO-OP LOSS:
        if status["coop"] == 1:
            # PLAYERS LOSE:
            if status["p1alive"] == 0 and status["p2alive"] == 0 and status["start"] == 1:
                # empty all the sprites list
                pygame.sprite.Group.empty(asp)
                pygame.sprite.Group.empty(ship1)
                pygame.sprite.Group.empty(ship2)
                pygame.sprite.Group.empty(lasers)
                pygame.sprite.Group.empty(blasers)
                pygame.sprite.Group.empty(bug1)
                pygame.sprite.Group.empty(bug2)
                pygame.sprite.Group.empty(bug3)
                pygame.sprite.Group.empty(bug4)
                pygame.sprite.Group.empty(boss1)

                # Create text and color it (Boolean makes text clearer I think)
                text = font.render("Game OVER!", True, text_color)
                # Create coordinates for text
                textRect = text.get_rect()
                textRect.center = (400, 200)
                # Draw text on window
                WIN.blit(text, textRect)

                score = font.render(" SCORE: {}".format(status["points"]), True, RED)
                scoreRect = score.get_rect()
                scoreRect.center = (400, 250)
                WIN.blit(score, scoreRect)

                # -----[ QUIT TO MAIN MENU BUTTON ]-----
                # Blit it on screen, default color, x = 400, y = 200, w = 140, h = 40
                pygame.draw.rect(WIN, button_color, [330, 300, 140, 40])
                # QUIT BUTTON (HIGHLIGHT)
                # If 400 < mouse x coordinate < 540 and 200 < mouse y coordinate < 240
                if 330 <= mouse[0] <= 470 and 300 <= mouse[1] <= 340:
                    # Draw the same button, but use secondary color
                    pygame.draw.rect(WIN, button_color_2, [330, 300, 140, 40])
                    # If button is pressed while over QUIT BUTTON, Exit game
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        status["p1alive"] = 0
                        status["p2alive"] = 0
                        status["start"] = 0
                        status["counter"] = 0
                        status["points"] = 0
                        status["coop"] = 0
                        status["bossdead"] = 0

                # -----[ BUTTON TEXTS ]-----
                """Must be called after button color changes, as it must appear OVER THEM"""
                # QUIT TEXT
                WIN.blit(quit_text, (370, 305))
        # CO-OP WIN!:
        if status["coop"] == 1:
            # PLAYERS WIN!!!:
            if status["bossdead"] == 1 and status["start"] == 1:
                # empty all the sprites list
                pygame.sprite.Group.empty(asp)
                pygame.sprite.Group.empty(ship1)
                pygame.sprite.Group.empty(ship2)
                pygame.sprite.Group.empty(lasers)
                pygame.sprite.Group.empty(blasers)
                pygame.sprite.Group.empty(bug1)
                pygame.sprite.Group.empty(bug2)
                pygame.sprite.Group.empty(bug3)
                pygame.sprite.Group.empty(bug4)
                pygame.sprite.Group.empty(boss1)

                # Create text and color it (Boolean makes text clearer I think)
                text = font.render("CONGRATS!", True, text_color)
                # Create coordinates for text
                textRect = text.get_rect()
                textRect.center = (400, 200)
                # Draw text on window
                WIN.blit(text, textRect)

                score = font.render(" SCORE: {}".format(status["points"]), True, RED)
                scoreRect = score.get_rect()
                scoreRect.center = (400, 250)
                WIN.blit(score, scoreRect)

                # -----[ QUIT TO MAIN MENU BUTTON ]-----
                # Blit it on screen, default color, x = 400, y = 200, w = 140, h = 40
                pygame.draw.rect(WIN, button_color, [330, 300, 140, 40])
                # QUIT BUTTON (HIGHLIGHT)
                # If 400 < mouse x coordinate < 540 and 200 < mouse y coordinate < 240
                if 330 <= mouse[0] <= 470 and 300 <= mouse[1] <= 340:
                    # Draw the same button, but use secondary color
                    pygame.draw.rect(WIN, button_color_2, [330, 300, 140, 40])
                    # If button is pressed while over QUIT BUTTON, Exit game
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        status["p1alive"] = 0
                        status["p2alive"] = 0
                        status["start"] = 0
                        status["counter"] = 0
                        status["points"] = 0
                        status["coop"] = 0
                        status["bossdead"] = 0

                # -----[ BUTTON TEXTS ]-----
                """Must be called after button color changes, as it must appear OVER THEM"""
                # QUIT TEXT
                WIN.blit(quit_text, (370, 305))

        # Draws all of the sprites in the ALL SPRITES group
        asp.draw(WIN)
        # Calls the update function from any sprites in the ALL SPRITES group
        asp.update()
        # Updates the window
        pygame.display.update()

        #-----[ SPAWNING FUNCTION ]-----
        # Uses pygame's sprite groups to create waves of enemies


        # This function is called immediately upon game's launch. After, conditionals will run the game
        def spawn():

            # WAVE 1: (25 Bug Type 1's) 25 TOTAL
            if status["counter"] == 3:

                # Incrementer for space between sprites
                b = 0
                # Spawn 20 enemies
                for i in range(1, 26):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = -80 * b
                    b1.rect.y = 0
                    b += 1

            # WAVE 2: (20 BT1's, 10 BT2's, 10 BT2's) 40 TOTAL
            if status["counter"] == 500:
                # Incrementer for space between sprites
                b = 20
                # Spawn 20 BT1's
                for i in range(1, 21):
                    # Create a bug type 1
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)

                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = -80 * b
                    b1.rect.y = 0
                    b += 1

                # Incrementer for space between sprites
                s = 0
                # Spawn 10 BT2's
                for i in range(1, 11):
                    # Create a bug type 2
                    b2 = BugT2(2)
                    # add it to all appropriate sprite lists
                    asp.add(b2)
                    bug2.add(b2)
                    # Everytime a bug gets spawned, s is incremented by 1, so 100 pixels of space is made between each bug's x
                    b2.rect.x = 100 * s
                    b2.rect.y = -100
                    s += 1

                # Incrementer for space between sprites
                s = 0
                # Spawn 10 BT2's
                for i in range(1, 11):
                    # Create a bug type 2
                    b2 = BugT2(2)
                    # add it to all appropriate sprite lists
                    asp.add(b2)
                    bug2.add(b2)
                    # Everytime a bug gets spawned, s is incremented by 1, so 100 pixels of space is made between each bug's x
                    b2.rect.x = 85 * s
                    b2.rect.y = -200
                    s += 1

            # WAVE 3: (8 BT2'S) 8 TOTAL
            if status["counter"] == 900:
                f = 1
                for i in range(1, 3):
                    # Create a bug type 2
                    b2 = BugT2(2)
                    # add it to all appropriate sprite lists
                    asp.add(b2)
                    bug2.add(b2)
                    # Everytime a bug gets spawned, s is incremented by 1, so 100 pixels of space is made between each bug's x
                    b2.rect.x = 400
                    b2.rect.y = -100 * f
                    f += 1

                f = 1
                for i in range(1, 3):
                    # Create a bug type 2
                    b2 = BugT2(2)
                    # add it to all appropriate sprite lists
                    asp.add(b2)
                    bug2.add(b2)
                    # Everytime a bug gets spawned, s is incremented by 1, so 100 pixels of space is made between each bug's x
                    b2.rect.x = 465
                    b2.rect.y = -100 * f
                    f += 1

                f = 1
                for i in range(1, 3):
                    # Create a bug type 2
                    b2 = BugT2(2)
                    # add it to all appropriate sprite lists
                    asp.add(b2)
                    bug2.add(b2)
                    # Everytime a bug gets spawned, s is incremented by 1, so 100 pixels of space is made between each bug's x
                    b2.rect.x = 335
                    b2.rect.y = -100 * f
                    f += 1

                f = 1
                for i in range(1, 3):
                    # Create a bug type 2
                    b2 = BugT2(2)
                    # add it to all appropriate sprite lists
                    asp.add(b2)
                    bug2.add(b2)
                    # Everytime a bug gets spawned, s is incremented by 1, so 100 pixels of space is made between each bug's x
                    b2.rect.x = 270
                    b2.rect.y = -100 * f
                    f += 1

            # BACKGROUND CHANGE at 1200
            # WAVE 4: ( 11 BT3's, 10 BT4's, 42 BT1's) 63 TOTAL
            if status["counter"] == 1200:
                # Bug Type 3's
                for i in range(1, 11):
                    # Create Bug Type 3's
                    b3 = BugT3(1)
                    # Add them to appropriate lists
                    asp.add(b3)
                    bug3.add(b3)
                    # Chooses a random integer between 1,2
                    spawn = random.randint(1, 100)
                    # If > 60, spawn on left side of screen
                    if spawn > 60:
                        b3.rect.x = 0
                    # Else, spawn on right side of screen
                    else:
                        b3.rect.x = 760
                    # Set  (off screen)
                    b3.rect.y = -800


                # Bug Type 1's
                # Incrementer for space between sprites
                n = 0
                for i in range(1, 2):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    b1.image = b1.images[4]
                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = 800
                    b1.rect.x += 10 * n
                    b1.rect.y = 40
                    n += 1

                # Bug Type 1's
                # Incrementer for space between sprites
                b = 1
                # Spawn 20 enemies
                for i in range(1, 21):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    b1.image = b1.images[2]
                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = 800
                    b1.rect.x += 10 * b
                    b1.rect.y = 40
                    b += 1

                # Bug Type 1's
                # Incrementer for space between sprites
                m = 21
                for i in range(1, 2):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    b1.image = b1.images[3]

                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = 800
                    b1.rect.x += 10 * m
                    b1.rect.y = 40
                    m += 1

                # Bug Type 1's
                # Incrementer for space between sprites
                s = 0
                # Spawn 20 enemies
                for i in range(1, 21):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    b1.image = b1.images[2]
                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = -10 * s
                    b1.rect.y = 0
                    s += 1

            # WAVE 5: ( 32 BT4's) 32 TOTAL
            if status["counter"] == 1600:
                # Bug Type 4's
                # Incrementer for space between sprites
                q = 0
                for i in range(1, 11):
                    # Create Bug Type 4
                    b4 = BugT4(1)
                    # Add sprites to all appropriate lists
                    asp.add(b4)
                    bug4.add(b4)
                    # Spawn at x coordinate 0, a y coordinate 80 pixels from other sprites, and increment incrementer
                    b4.rect.x = 0
                    b4.rect.y = 40 * q
                    q += 1
                    if b4.rect.y == 200 or b4.rect.y == 240:
                        b4.kill()

                # Bug Type 4's
                # Incrementer for space between sprites
                q = 0
                for i in range(1, 11):
                    # Create Bug Type 4
                    b4 = BugT4(1)
                    # Add sprites to all appropriate lists
                    asp.add(b4)
                    bug4.add(b4)
                    # Spawn at x coordinate 0, a y coordinate 80 pixels from other sprites, and increment incrementer
                    b4.rect.x = -200
                    b4.rect.y = 40 * q
                    q += 1
                    if b4.rect.y == 0 or b4.rect.y == 40:
                        b4.kill()

                # Bug Type 4's
                # Incrementer for space between sprites
                q = 0
                for i in range(1, 11):
                    # Create Bug Type 4
                    b4 = BugT4(1)
                    # Add sprites to all appropriate lists
                    asp.add(b4)
                    bug4.add(b4)
                    # Spawn at x coordinate 0, a y coordinate 80 pixels from other sprites, and increment incrementer
                    b4.rect.x = -400
                    b4.rect.y = 40 * q
                    q += 1
                    if b4.rect.y == 360 or b4.rect.y == 400:
                        b4.kill()

                # Bug Type 4's
                # Incrementer for space between sprites
                q = 0
                for i in range(1, 11):
                    # Create Bug Type 4
                    b4 = BugT4(1)
                    # Add sprites to all appropriate lists
                    asp.add(b4)
                    bug4.add(b4)
                    # Spawn at x coordinate 0, a y coordinate 80 pixels from other sprites, and increment incrementer
                    b4.rect.x = -600
                    b4.rect.y = 40 * q
                    q += 1
                    if b4.rect.y == 200 or b4.rect.y == 240:
                        b4.kill()

            # BACKGROUND CHANGE AT 1800
            # WAVE 6:
            if status["counter"] == 1800:
                # Bug Type 1's
                # Incrementer for space between sprites
                b = 1
                # Spawn 20 enemies
                for i in range(1, 21):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    b1.image = b1.images[2]
                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = 800
                    b1.rect.x += 10 * b
                    b1.rect.y = 40
                    b += 1

            # BOSS WAVE
            if status["counter"] == 2000:

                boss = Boss(65)
                asp.add(boss)
                boss1.add(boss)
                boss.rect.x = 250
                boss.rect.y = 0

                # Bug Type 1's
                # Incrementer for space between sprites
                b = 1
                # Spawn 20 enemies
                for i in range(1, 21):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    b1.image = b1.images[2]
                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x = -10 * b
                    b1.rect.y = 0
                    b += 1

                # Bug Type 1's
                # Incrementer for space between sprites
                b = 1
                # Spawn 20 enemies
                for i in range(1, 21):
                    # create a bug 1 type
                    b1 = BugT1(1)
                    # add it to all appropriate lists
                    asp.add(b1)
                    bug1.add(b1)
                    b1.image = b1.images[2]
                    # set its initial coordinates to (-80,0)
                    # Everytime a bug gets spawned, b is incremented by 1, so 80 pixels of space is made between each bug's x
                    b1.rect.x == 800
                    b1.rect.x += 10 * b
                    b1.rect.y = 0
                    b += 1

                for i in range(1, 11):
                    # Create Bug Type 3's
                    b3 = BugT3(1)
                    # Add them to appropriate lists
                    asp.add(b3)
                    bug3.add(b3)
                    # Chooses a random integer between 1,2
                    spawn = random.randint(1, 100)
                    # If > 60, spawn on left side of screen
                    if spawn > 60:
                        b3.rect.x = 0
                    # Else, spawn on right side of screen
                    else:
                        b3.rect.x = 760
                    # Set  (off screen)
                    b3.rect.y = -800

        # Calls the function to spawn the enemies
        spawn()

    #-----[ MUSIC FUNCTION ]-----
    def music():
        MUSIC_FILE = ("game_music.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play(-1)

    # Calls the music function
    music()

    #-----[ GAME LOGIC ]-----
    # Game loop for key controls, sprite collision, and calling earlier functions
    while run:

        # tracks mouse
        mouse = pygame.mouse.get_pos()

        #-----[ TROUBLESHOOTING TEXTS ]-----
        #print(status["counter"])
        #print(status["coop"])
        #print(mouse)
        #print(status["difficulty"])
        #print("POINTS: {}".format(status["points"]))
        #print("HEALTH: {}".format(player1.health))
        #print("HEALTH: {}".format(player2.health))
        #print("P1: {}".format(status["p1alive"]))
        #print("P2: {}".format(status["p2alive"]))
        #print(len(blasers))
        #print(len(ship))
        #print("STATUS: {}".format(status["difficulty"]))


        # Sets the game to reset at the desired frames per second
        clock.tick(FPS)

        #-----[ GAME EVENTS ]-----
        # Player closes window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Run is set to False; main loop stops
                run = False

            #-----[ PLAYERS LASER FIRE BUTTON ]-----
            if event.type == pygame.KEYDOWN:

                # PLAYER 1 FIRING:
                # If the player hits the fire button and has health remaining
                if event.key == pygame.K_LCTRL and status["p1alive"] == 1:
                    # Set laser variable to the Laser class
                    laser = Laser()
                    # Set laser to appear from player's coordinates
                    laser.rect.x = player1.rect.x + 26
                    laser.rect.y = player1.rect.y
                    # Add laser to the ALL SPRITES group as it's made
                    asp.add(laser)
                    # Add laser to the Lasers group as it's made
                    lasers.add(laser)
                    # play laser fire sound
                    pygame.mixer.Sound.play(FIRE)

                # PLAYER 2 FIRING:
                # If the player hits the fire button and has health remaining
                if event.key == pygame.K_RCTRL and status["p2alive"] == 1:
                    # Set laser variable to the Laser class
                    laser = Laser2()
                    # Set laser to appear from player's coordinates
                    laser.rect.x = player2.rect.x + 26
                    laser.rect.y = player2.rect.y
                    # Add laser to the ALL SPRITES group as it's made
                    asp.add(laser)
                    # Add laser to the Lasers group as it's made
                    lasers.add(laser)
                    # Play laser fire sound
                    pygame.mixer.Sound.play(FIRE)

        # -----[ SHIP LASERS / BUG 1 COLLISION ]-----
        # Create a list that removes laser and enemy once they collide
        # The boolean, if set to true, removes both sprites.
        for laser in lasers:
            bug1hit = pygame.sprite.spritecollide(laser, bug1, False)
            # If the player is hit
            for b1 in bug1hit:
                # Decrement health by 1 and display change (audio and visual)
                b1.health -= 1
                laser.kill()
                # If player has no health remaining
                if b1.health <= 0:
                    # Remove player from everything
                    b1.kill()
                    status["points"] += 1

        #-----[ SHIP LASERS / BUG 2 COLLISION ]-----
        # Create a list that removes laser and enemy once they collide
        # The boolean, if set to true, removes both sprites.
        for laser in lasers:
            bug2hit = pygame.sprite.spritecollide(laser, bug2, False)
            # If the player is hit
            for b2 in bug2hit:
                # Decrement health by 1 and display change (audio and visual)
                b2.health -= 1
                laser.kill()
                # If player has no health remaining
                if b2.health <= 0:
                    # Remove player from everything
                    b2.kill()
                    status["points"] += 2
                # If the player has health remaining:
                if b2.health > 0:
                    # Blit the player onto the screen
                    asp.add(b2)
                    bug2.add(b2)
                    pygame.mixer.Sound.play(BUZZ)

        # -----[ SHIP LASERS / BUG 3 COLLISION ]-----
        # Create a list that removes laser and enemy once they collide
        # The boolean, if set to true, removes both sprites.
        for laser in lasers:
            bug3hit = pygame.sprite.spritecollide(laser, bug3, False)
            # If the player is hit
            for b3 in bug3hit:
                # Decrement health by 1 and display change (audio and visual)
                b3.health -= 1
                laser.kill()
                # If player has no health remaining
                if b3.health <= 0:
                    # Remove player from everything
                    b3.kill()
                    status["points"] += 1

        # -----[ SHIP LASERS / BUG 4 COLLISION ]-----
        # Create a list that removes laser and enemy once they collide
        # The boolean, if set to true, removes both sprites.
        for laser in lasers:
            bug4hit = pygame.sprite.spritecollide(laser, bug4, False)
            # If the player is hit
            for b4 in bug4hit:
                # Decrement health by 1 and display change (audio and visual)
                b4.health -= 1
                laser.kill()
                # If player has no health remaining
                if b4.health <= 0:
                    # Remove player from everything
                    b4.kill()
                    status["points"] += 1

        # -----[ SHIP LASERS / BOSS COLLISION ]-----
        # Create a list that removes laser and enemy once they collide
        # The boolean, if set to true, removes both sprites.
        for laser in lasers:
            bosshit = pygame.sprite.spritecollide(laser, boss1, False)
            # If the player is hit
            for boss in bosshit:
                # Decrement health by 1 and display change (audio and visual)
                boss.health -= 1
                laser.kill()
                # If player has no health remaining
                if boss.health <= 0:
                    pygame.mixer.Sound.play(DEATH)
                    # Remove player from everything
                    boss.kill()
                    status["bossdead"] = 1
                    status["points"] += 100

        #-----[ BUG'S LASERS / PLAYER(S) COLLISION ]-----
        # SOLO:
        if status["coop"] == 0:
            # Collision between the Bug's lasers and the player
            for blaser in blasers:
                playerhit = pygame.sprite.spritecollide(blaser, ship, False)
                # If the player is hit
                for player1 in playerhit:
                    # Decrement health by 1 and display change (audio and visual)
                    player1.health -= 1
                    print("HEALTH: {}".format(player1.health))
                    pygame.mixer.Sound.play(HIT)
                    blaser.kill()
                    # If player has no health remaining
                    if player1.health <= 0:
                        # Remove player from everything
                        player1.kill()
                        # Set player1 alive boolean to false (0)
                        status["p1alive"] = 0
                    # If the player has health remaining:d
                    if player1.health > 0:
                        # Blit the player onto the screen
                        asp.add(player1)
                        ship.add(player1)
                        # 1000 msec = 1 sec
                        pygame.time.delay(100)
        # CO-OP:
        if status["coop"] == 1:
            # BUG LASERS/ PLAYER 1 COLLISION:
            for blaser in blasers:
                playerhit = pygame.sprite.spritecollide(blaser, ship1, False)
                # If the player is hit
                for player1 in playerhit:
                    # Decrement health by 1 and display change (audio and visual)
                    player1.health -= 1
                    print("HEALTH: {}".format(player1.health))
                    pygame.mixer.Sound.play(HIT)
                    blaser.kill()
                    # If player has no health remaining
                    if player1.health <= 0:
                        # Remove player from everything
                        player1.kill()
                        # Set player1 alive boolean to false (0)
                        status["p1alive"] = 0
                    # If the player has health remaining:
                    if player1.health > 0:
                        # Blit the player onto the screen
                        asp.add(player1)
                        ship1.add(player1)
                        # Input small delay for reaction time
                        pygame.time.delay(100)

            # BUG LASERS / PLAYER 2 COLLISION:
            for blaser in blasers:
                player2hit = pygame.sprite.spritecollide(blaser, ship2, False)
                for player2 in player2hit:
                    # Decrement health by 1 and display change (audio and visual)
                    player2.health -= 1
                    print("HEALTH: {}".format(player2.health))
                    pygame.mixer.Sound.play(HIT)
                    blaser.kill()
                    # If player has no health remaining
                    if player2.health <= 0:
                        # Remove player from everything
                        player2.kill()
                        # Set player1 alive boolean to false (0)
                        status["p2alive"] = 0
                    # If the player has health remaining:d
                    if player2.health > 0:
                        # Blit the player onto the screen
                        asp.add(player2)
                        ship2.add(player2)
                        # 1000 msec = 1 sec
                        # Input small delay for reaction time
                        pygame.time.delay(100)

        #-----[ BUG TYPE 1 / PLAYER SHIP COLLISION ]------
        # SOLO:
        if status["coop"] == 0:
            for b1 in bug1:
                crash = pygame.sprite.spritecollide(b1, ship, False)
                for player1 in crash:
                    asp.remove(b1)
                    bug1.remove(b1)
                    player1.health -= 1
                    print("HEALTH: {}".format(player1.health))
                    print("OUCH!")
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 360
        # CO-OP:
        if status["coop"] == 1:
            # BUG 1 / PLAYER 2 COLLISION:
            for b1 in bug1:
                crash2 = pygame.sprite.spritecollide(b1, ship2, False)
                for player2 in crash2:
                    asp.remove(b1)
                    bug1.remove(b1)
                    player2.health -= 1
                    print("HEALTH: {}".format(player2.health))
                    print("OUCH!")
                    pygame.mixer.Sound.play(HIT)
                    if player2.health <= 0:
                        player2.kill()
                        asp.remove(player2)
                        ship2.remove(player2)
                        status["p2alive"] = 0
                    if player2.health > 0:
                        asp.add(player2)
                        ship2.add(player2)
                        # Put player back at starting coordinates
                        player2.rect.x = 400
                        player2.rect.y = 360

            # BUG 1 / PLAYER 1 COLLISION:
            for b1 in bug1:
                crash = pygame.sprite.spritecollide(b1, ship1, False)
                for player1 in crash:
                    asp.remove(b1)
                    bug1.remove(b1)
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship1.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship1.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 360

        #-----[ BUG TYPE 2 / PLAYER SHIP COLLISION ]------
        # SOLO:
        if status["coop"] == 0:
            for b2 in bug2:
                crash = pygame.sprite.spritecollide(b2, ship, False)
                for player1 in crash:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    b2.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 360
                    if b2.health <= 0:
                        b2.kill()
                        status["points"] += 2
        # CO-OP:
        if status["coop"] == 1:
            # BUG 1 / PLAYER 2 COLLISION:
            for b2 in bug2:
                crash2 = pygame.sprite.spritecollide(b2, ship2, False)
                for player2 in crash2:
                    player2.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player2.health))
                    b2.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player2.health <= 0:
                        player2.kill()
                        asp.remove(player2)
                        ship2.remove(player2)
                        status["p2alive"] = 0
                    if player2.health > 0:
                        asp.add(player2)
                        ship2.add(player2)
                        # Put player back at starting coordinates
                        player2.rect.x = 400
                        player2.rect.y = 360
                    if b2.health <= 0:
                        b2.kill()
                        status["points"] += 2

            # BUG 1 / PLAYER 1 COLLISION:
            for b2 in bug2:
                crash = pygame.sprite.spritecollide(b2, ship1, False)
                for player1 in crash:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    b2.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship1.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship1.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 360
                    if b2.health <= 0:
                        b2.kill()
                        status["points"] += 2

        #-----[ BUG TYPE 3 / PLAYER SHIP COLLISION ]------
        # SOLO
        if status["coop"] == 0:
            for b3 in bug3:
                crash = pygame.sprite.spritecollide(b3, ship, False)
                for player1 in crash:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    asp.remove(b3)
                    bug3.remove(b3)
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 320
        # CO-OP
        if status["coop"] == 1:
            for b3 in bug3:
                crash = pygame.sprite.spritecollide(b3, ship1, False)
                for player1 in crash:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    b3.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship1.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship1.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 320
                    if b3.health <= 0:
                        b3.kill()
                        status["points"] += 3
            for b3 in bug3:
                crash2 = pygame.sprite.spritecollide(b3, ship2, False)
                for player2 in crash2:
                    player2.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player2.health))
                    b3.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player2.health <= 0:
                        player2.kill()
                        asp.remove(player2)
                        ship2.remove(player2)
                        status["p2alive"] = 0
                    if player2.health > 0:
                        asp.add(player2)
                        ship2.add(player2)
                        # Put player back at starting coordinates
                        player2.rect.x = 400
                        player2.rect.y = 320

        #-----[ BUG TYPE 4 / PLAYER SHIP COLLISION ]------
        # SOLO:
        if status["coop"] == 0:
            for b4 in bug4:
                crash = pygame.sprite.spritecollide(b4, ship, False)
                for player1 in crash:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    asp.remove(b4)
                    b4.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship.add(player1)
                    if b4.health <= 0:
                        b4.kill()
                        status["points"] += 4
        # CO-OP:
        if status["coop"] == 1:
            for b4 in bug4:
                crash = pygame.sprite.spritecollide(b4, ship1, False)
                for player1 in crash:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    b4.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship1.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship1.add(player1)

                    if b4.health <= 0:
                        b4.kill()
                        status["points"] += 3
            for b4 in bug4:
                crash2 = pygame.sprite.spritecollide(b4, ship2, False)
                for player2 in crash2:
                    player2.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player2.health))
                    b4.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player2.health <= 0:
                        player2.kill()
                        asp.remove(player2)
                        ship2.remove(player2)
                        status["p2alive"] = 0
                    if player2.health > 0:
                        asp.add(player2)
                        ship2.add(player2)
                    if b4.health <= 0:
                        b4.kill()
                        status["points"] += 3

        # -----[ BOSS / PLAYER SHIP COLLISION ]------
        # SOLO:
        if status["coop"] == 0:
            for boss in boss1:
                crash = pygame.sprite.spritecollide(boss, ship, False)
                for player1 in crash:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    boss.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 360
                    if boss.health <= 0:
                        pygame.mixer.Sound.play(DEATH)
                        boss.kill()
                        status["points"] += 100
        # CO-OP:
        if status["coop"] == 1:
            for boss in boss1:
                crash1 = pygame.sprite.spritecollide(boss, ship1, False)
                for player1 in crash1:
                    player1.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player1.health))
                    boss.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player1.health <= 0:
                        player1.kill()
                        asp.remove(player1)
                        ship1.remove(player1)
                        status["p1alive"] = 0
                    if player1.health > 0:
                        asp.add(player1)
                        ship1.add(player1)
                        # Put player back at starting coordinates
                        player1.rect.x = 400
                        player1.rect.y = 360
                    if boss.health <= 0:
                        pygame.mixer.Sound.play(DEATH)
                        boss.kill()
                        status["points"] += 100
            for boss in boss1:
                crash2 = pygame.sprite.spritecollide(boss, ship2, False)
                for player2 in crash2:
                    player2.health -= 1
                    print("OUCH!")
                    print("HEALTH: {}".format(player2.health))
                    boss.health -= 1
                    pygame.mixer.Sound.play(HIT)
                    if player2.health <= 0:
                        player2.kill()
                        asp.remove(player2)
                        ship2.remove(player2)
                        status["p2alive"] = 0
                    if player2.health > 0:
                        asp.add(player2)
                        ship2.add(player2)
                        # Put player back at starting coordinates
                        player2.rect.x = 400
                        player2.rect.y = 360
                    if boss.health <= 0:
                        boss.kill()
                        status["points"] += 100

        #-----[ PLAYER MOVEMENT ]-----
        # SOLO:
        if status["coop"] == 0:
            if status["p1alive"] == 1 and status["start"] == 1:
                player1.move()
        # CO-OP:
        if status["coop"] == 1:
            if status["p1alive"] == 1 and status["start"] == 1:
                player1.move()
            if status["p2alive"] == 1 and status["start"] == 1:
                player2.move()

        #-----[ TIMER/ITERATOR/INCREMENTER/COUNTER ]-----
        # A constantly iterating variable in place of a time module
        # spawns enemies and controls level progression
        # SOLO
        if status["coop"] == 0:
            # If player is alive, increment the counter
            if status["p1alive"] == 1 and status["start"] == 1:
                status["counter"] += 1
            # Otherwise, set the counter == 0 (So game can start again)
            else:
                status["counter"] == 0
        # COOP
        if status["coop"] == 1:
            # If both players are alive, increment the counter
            if (status["p1alive"] == 1 and status["p2alive"] == 1 and status["start"] == 1):
                    status["counter"] += 1
            # If one player is alive, increment the counter
            if (status["p1alive"] == 1 and status["p2alive"] == 0 and status["start"] == 1):
                    status["counter"] += 1
            if (status["p1alive"] == 0 and status["p2alive"] == 1 and status["start"] == 1):
                    status["counter"] += 1
            # If none of the players are alive, set counter == 0 (So game can start again)
            if (status["p1alive"] == 0 and status["p2alive"] == 0 and status["start"] == 1):
                    status["counter"] == 0

        # Makes sure player has health at beginning of game
        if status["counter"] == 0:
            player1.health = 3
            player2.health = 3


        # While the game is running, call the display function
        display(status)

#=====[ LAUNCH GAME ]=====
# Calls main loop
main()
