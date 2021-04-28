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
- Bug Type 3
- Final Boss?
- Music exlusive to main menu?
- Arcade button compatibility
- A box to put it all in
"""

"""
4/26 Change Log [TL;DR]: 
- Added Bug Type 2 (testing firing and movement)
- Added Bug Laser Class (with disliked collision) 
- Bug Type 1 can now fire lasers
- Added health variable for Player Sprite (ineffective)
- Moved sprites' groups list to the top of file (access them as pre-defined variables)
- Converted laserfire.mp3 to laserfire.wav (RPi compatibility) 

COLIN:
- Added and currently am testing another bug type (BUG TYPE 2). It fires a laser at certain coordinates as it moves down
  the screen. After shooting for so long, it moves off screen (I'll look into despawning it later)
- Bug Type 1 now fires lasers. It fires down whenever its coordinates can cleanly be modulated by 75 for a remainder of 0.
  I think I should make it a constant variable that goes up with difficulty. But know that I think about it, if we spawn
  multiples of those sprites, they'd be shooting in the exact same place. not very good at the start, but I guess it 
  could be fun later on.
- Added Bugs' Laser class and collision with the player. I don't like the collision though
- Made a health instance variable for the player. It cannot fire lasers after running out of health by getting hit 
  by laser fire. HOWEVER, if the player has more than 1 health, the sprite will automatically be removed by the 
  collision type, but still able to shoot lasers. I have to find a collision type that doesn't automatically remove the
  targetted sprite (Unless it's bug type 1 of course. Those guys are small fries.)
- Moved sprite lists to the top of the game so they're predefined
- Converted laserfire.mp3 to laserfire.wav. RPi didn't like it for some reason, but it accepted game_music.mp3. 
  As it should
  
4/27 Change Log [TL;DR]:
- Attempted to make enemies spawn in waves. (WIP)
- Finished movement chart for Bug Type 1 (Messy)

COLIN:
- Been messing around with adding enemy sprites as waves. Doesn't work exactly how I want it to. I'll look into it
"""
# Import pygame
import pygame
import random
# Initialize the pygame module
pygame.init()


#=====[ IMAGES & AUDIO ]=====
# COLIN: Here, we can put other images for enemies and a possible player 2
# Grabs image for the player sprite
PLAYER = pygame.image.load("GalagaShip.png")
# Adjusts the image to fit onto the screen with desired (width, height)
PLAYER = pygame.transform.scale(PLAYER, (55, 40))

# Grabs and adjusts image for the first bug type
BUG1 = pygame.image.load("b1.png")
BUG1 = pygame.transform.scale(BUG1, (55, 40))

# Grabs and adjusts second bug type
BUG2 = pygame.image.load("b2.png")
BUG2 = pygame.transform.scale(BUG2, (65, 80))

# Grab image for background
BG = pygame.image.load("space.jpg")

# Grab music for game audio
MUSIC = pygame.mixer.music.load("game_music.mp3")

# Grabs sound for laser fire
FIRE = pygame.mixer.Sound("laserfire.wav")

#=====[ CREATE WINDOW ]======
# Constant variable for window's width (800) and height (400); RPi screen size
SIZE = 800, 400
# Constant variable for pygame creating the window
WIN = pygame.display.set_mode(SIZE)
# Sets caption for upper left corner of window
pygame.display.set_caption("Test")

#=====[ VARIABLES AND LISTS]=====
# Constant variable representing a movement speed of 5 pixels for the player sprite
PIX = 5
# The following constant variables represent RGB values for the lasers
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0,255,0)
# This list represents the amount of time the Bug Type 2 has fired, and its limits can be adjusted accordingly to match
# level difficulty
b2lasers = []
# This constant variable represents the amount of pixels Bug Type 1's travel per frame.
# This can be adjusted per difficulty. However, I think it'd be best to make it where the bugs get faster the
# longer they're alive
BUG1_MOV1 = 5
BUG1_MOV2 = 10

# These constant variables represent the x-coordinates where the Bug Type 1 should bounce off of.
R_EDGE = 745
L_EDGE = -5

# This constant variable represents the number the Bug Type 1s' coordinates can be modulated by to fire.
# Basically, it's the bug's fire rate. The lower the number, the faster it fires. This can be adjusted per difficulty
"""COLIN: BUG TYPE 1 WILL NOT FIRE once movement speed is updated if this remains == 110"""
BUG1_FIRE = 110

# Lists that contain amount of enemies to spawn per wave
spawn1 = []
spawn2 = []

#=====[ SPRITE GROUPS ]=====
# This creates a pygame group for (A)LL (SP)RITES
asp = pygame.sprite.Group()
# This creates a pygame group for player(s)
ship = pygame.sprite.Group()
# This creates a pygame group for enemies
enemy = pygame.sprite.Group()
# This creates a pygame group for the player's projectiles
lasers = pygame.sprite.Group()
# This creates a pygame group for the bugs' projectiles
blasers = pygame.sprite.Group()

#=====[ CLASSES AND FUNCTIONS ]=====
#-----[ PLAYER SPRITE CLASS ]-----
class Player(pygame.sprite.Sprite):
    # Constructor for Player Sprite
    def __init__(self, health):
        # Call the fancy pygame sprite parent class
        super().__init__()
        # instance variable to grab player image
        self.image = PLAYER
        # Creates the hitbox and tracks coordinates for the player
        self.rect = self.image.get_rect()
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

#-----[ PLAYERS LASER SPIRTE CLASS ]-----
class Laser(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Creates a rectangle with width and height of 4 and fills it with predefined color RED
        self.image = pygame.Surface([4,4])
        self.image.fill(RED)
        # Creates a rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()

    # Updates the sprite's movements
    def update(self):
        # Move the sprite up
        self.rect.y -= 7

#------[ BUG TYPE 1 SPRITE CLASS ]------
class BugT1(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Grabs the predefined variable from up top that represents the bug's image
        self.image = BUG1
        # Creates rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()
        # Instance variable that acts as a boolean for the for loop below
        self.move = 1
        self.shoot = 1

    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Update the sprite's movement
    def update(self):
        for i in range(self.move):
            print("x = {}".format(self.rect.x))
            #print("y = {}".format(self.rect.y))

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
                # If x coordinate > 840, remove sprite from game
                if self.rect.x <= -40:
                    self.kill()

        if (self.rect.x % BUG1_FIRE == 0):
            #print("x = {}".format(self.rect.x))
            blaser = B1Laser()
            self.shoot += 1
            # Set laser to appear from player's coordinates
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
        self.image.fill(RED)
        # Creates a rectangle (hitbox) for the sprite and tracks its coordinates
        self.rect = self.image.get_rect()

    # Updates the sprite's movements
    def update(self):
        # Move the sprite up
        self.rect.y += 7

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
        # Go down to y = 100
        if self.rect.y != 200 and len(b2lasers) != 10:
            self.rect.y += 1
        # Attempt to get it to shoot.
        if self.rect.y == 50 or self.rect.y == 100 or self.rect.y == 200:
            blaser = B2Laser()
            # Set laser to appear from player's coordinates
            blaser.rect.x = self.rect.x + 28
            blaser.rect.y = self.rect.y + 60
            # Add laser to the ALL SPRITES group as it's made
            asp.add(blaser)
            # Add laser to the Lasers group as it's made
            blasers.add(blaser)
            b2lasers.append("1")
        if self.rect.y == 200 and len(b2lasers) > 80:
            self.rect.y +=1

#-----[ BUG TYPE 2 LASER SPRITE CLASS ]-----
# Class for Bug Type 2's Laser fire (B and L are capitalized!!)
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
    player = Player(1)
    asp.add(player)
    ship.add(player)
    player.rect.x = 400
    player.rect.y = 360

    # Wave 1
    def wave1():
        # Spawns 3 of Bug Type 1's
        spawn1 = ["1", "2", "3"]
        for i in range(len(spawn1)):
            # create a bug 1 type
            b1 = BugT1()
            # add it to the all sprites list
            asp.add(b1)
            # add it to the enemy sprite list
            enemy.add(b1)
            # set its initial coordinates to (-80,0)
            b1.rect.x = -80
            b1.rect.y = 0
            # Add to the list
            spawn1.append("1")
            for j in range(len(spawn1)):
                # Put some space between the sprites
                """COLIN: Currently, this just makes the whole list of enemies back up an ungodly amount."""
                b1.rect.x -= 80

        # Spawns 5 of Bug Type 2's
        spawn2 = ["1","2","3", "4", "5"]
        # Create Bug Type 2's and add them to appropriate lists
        for i in range(len(spawn2)):
            b2 = BugT2()
            asp.add(b2)
            enemy.add(b2)
            # Place Bugs at random intervals between 200 and 600, and make spawn them off screen
            for c in range(len(spawn2)):
                b2.rect.x = random.randint(200,600)
                b2.rect.y = -200

            # TROUBLESHOOTING: print("Spawn 2 = {}".format(spawn2))

    """# Wave 2 
    def wave2():
        spawn2 =["1","2","3","4","5","6","7","8","9","10"]
        for i in range(len(spawn2)):
            b2 = BugT2()
            asp.add(b2)
            enemy.add(b2)
            for c in range(len(spawn2)):
                b2.rect.x = random.randint(100,600)
                b2.rect.y = -200
            #print("Spawn 2 = {}".format(spawn2))
            for j in range(len(spawn2)):
                b2.rect.x -= 60"""

    # Calls the wave functions
    """COLIN: Let's take things one at a time, and I may have to import time so there's a delay between calling the two
    functions. """
    wave1()
    # wave2()

    #-----[ DISPLAY FUNCTION ]----
    # This function, nested into the main loop, displays everything
    def display():
        # Blit (draw an object) the background at coordinates (0,0)
        WIN.blit(BG, (0,0))
        # Draws all of the sprites in the ALL SPRITES group
        asp.draw(WIN)
        # Calls the update function from any sprites in the ALL SPRITES group
        asp.update()
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
                if event.key == pygame.K_SPACE and player.health > 0:
                    # Set laser variable to the Laser class
                    laser = Laser()
                    # Set laser to appear from player's coordinates
                    laser.rect.x = player.rect.x + 24
                    laser.rect.y = player.rect.y
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
                lasers.remove(laser)
                asp.remove(laser)
                print("HIT!")


        #-----[ BUG'S LASERS / PLAYER(S) COLLISION ]-----
        # Collision between the Bug's lasers and the player
        for blaser in blasers:
            playerhit = pygame.sprite.spritecollide(blaser,ship, True)
            for blaser in playerhit:
                blasers.remove(blaser)
                asp.remove(blaser)
                player.health -= 1
                print("OUCH!")


        #-----[ PLAYER MOVEMENT ]-----
        # Tracks keys being pressed and restricts player from exiting window
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and player.rect.x - PIX > 0:
            player.moveLeft(PIX)
        if keys_pressed[pygame.K_d] and player.rect.x + PIX + 55 < 799:
            player.moveRight(PIX)
        if keys_pressed[pygame.K_w] and player.rect.y > 0:
            player.moveUp(PIX)
        if keys_pressed[pygame.K_s] and player.rect.y < 360:
            player.moveDown(PIX)

        # Calls the display function
        display()

#=====[ LAUNCH GAME ]=====
# Calls main loop
main()



