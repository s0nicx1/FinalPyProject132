"""
COLIN: So far this version of our project contains:
- Player movement
- A player sprite
- A type of enemy sprite
- basic projectile and collision
COLIN: But it also lacks:
- A main menu with game options
- Player lives {and health?}
- Co-op and Versus???
- Enemy variations, movements, attacks, spawning, and health
- Music for menu?git 
- Arcade button compatibility
- A box to put it all in

"""

# Import pygame
import pygame
import time

# Initialize the pygame module
pygame.init()


#=====[ IMAGES & AUDIO ]=====
# COLIN: Here, we can put other images for enemies and a possible player 2
# Grabs image for the player sprite
PLAYER = pygame.image.load("GalagaShip.png")
# Adjusts the image to fit onto the screen with desired (width, height)
PLAYER = pygame.transform.scale(PLAYER, (55, 40))

BUG1 = pygame.image.load("b1.png")
BUG1 = pygame.transform.scale(BUG1, (55, 40))

# Grab image for background
BG = pygame.image.load("space.jpg")

# Grab music for game audio
MUSIC = pygame.mixer.music.load("game_music.mp3")
FIRE = pygame.mixer.Sound("laserfire.mp3")

#=====[ CREATE WINDOW ]======
# Constant variable for window's width (800) and height (400); RPi screen size
SIZE = 800, 400
# Constant variable for pygame creating the window
WIN = pygame.display.set_mode(SIZE)
# Sets caption for upper left corner of window
pygame.display.set_caption("Test")

#=====[ VARIABLES ]=====
# Constant variable representing a movement speed of 5 pixels for the player sprite
PIX = 5
RED = (255, 0, 0)

#=====[ CLASSES AND FUNCTIONS ]=====
#------[ PLAYER CLASS ]-------
class Player(pygame.sprite.Sprite):
    # Constructor for Player Sprite
    def __init__(self):
        # Call the fancy pygame sprite parent class
        super().__init__()
        # instance variable to grab player image
        self.image = PLAYER
        # Creates the hitbox and tracks coordinates for the player
        self.rect = self.image.get_rect()

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

    # Function that draws Player Sprite onto screen
    def draw(self,window):
        window.blit(self.image, (self.rect.x,self.rect.y))

# Class for the laser sprite
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

#------[ BUG TYPE 1 CLASS ]------
class BugT1(pygame.sprite.Sprite):
    def __init__(self):
        # Calls pygame's sprite class
        super().__init__()
        # Grabs the predefined variable from up top that represents the bug's image
        self.image = BUG1
        # Creates rectangle for the sprite and tracks coordinates
        self.rect = self.image.get_rect()
        # Instance variable that acts as a boolean for the for loop below
        self.move = 1

    # Function that draws the Bug Type 1 onto the screen at given coordinates
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    # Update the sprite's movement
    def update(self):
        for i in range(self.move):
            #print("x = {}".format(self.rect.x))
            #print("y = {}".format(self.rect.y))
            if self.rect.x != 745 and self.rect.y == 0:
                self.rect.x += 5
            if self.rect.x == 745 and self.rect.y < 40:
                self.rect.y += 5
            if self.rect.x != 0 and self.rect.y == 40:
                self.rect.x -= 5
            if self.rect.x == 0 and self.rect.y < 80:
                self.rect.y += 5
            if self.rect.x < 745 and self.rect.y == 80:
                self.rect.x += 5

#=====[ MAIN GAME LOOP ]=====
# COLIN: Here is where the game is run. It sets up the foundation of the pygame, then refers to several
# classes and functions to display the pygame.
def main():
    # Run set to True so the game doesn't end
    run = True
    # Sets the Frame Rate
    FPS = 35
    # Creates a clock that makes sure computer runs program at desired FPS
    clock = pygame.time.Clock()

    #-----[ SPRITES ]-----
    # This creates a pygame group for (A)LL (SP)RITES
    asp = pygame.sprite.Group()
    # This creates a pygame group for enemies
    enemy  = pygame.sprite.Group()
    # This creates a pygame group for the player's projectiles
    lasers = pygame.sprite.Group()
    # create player at desired coordinates (400, 360)
    player = Player()
    asp.add(player)
    player.rect.x = 400
    player.rect.y = 360
    # Testing the bugs spawn at (0,0)
    b1 = BugT1()
    asp.add(b1)
    enemy.add(b1)
    b1.rect.x = 0
    b1.rect.y = 0


    # This function, nested into the main loop, displays everything
    def display():
        # Blit (draw an object) the background at coordinates (0,0)
        WIN.blit(BG, (0,0))
        # Refreshes the surfaces that pygame is displaying
        player.draw(WIN)

        # Draws all of the sprites in the ALL SPRITES group
        asp.draw(WIN)
        # Calls the update function from any sprites in the ALL SPRITES group
        asp.update()
        # Updates the window
        pygame.display.update()

    def music():
        MUSIC_FILE = ("game_music.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play()

    music()
    # Game loop for key controls
    while run:
        # Sets the game to reset at the desired frames per second
        clock.tick(FPS)

        # Player closes window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Run is set to False; main loop stops
                run = False
            # Player presses left control to fire (will be fixed with arcade GPIO)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
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

        # Collision between Player's lasers and enemies
        for laser in lasers:
            # Create a list that removes laser and enemy once they collide
            enemyhit = pygame.sprite.spritecollide(laser, enemy, True)
            for laser in enemyhit:
                lasers.remove(laser)
                asp.remove(laser)
                print("HIT!")

        # Tracks keys being pressed
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and player.rect.x - PIX > 0:
            player.moveLeft(PIX)
        if keys_pressed[pygame.K_d] and player.rect.x + PIX + 55 < 799:
            player.moveRight(PIX)
        if keys_pressed[pygame.K_w] and player.rect.y > 0:
            player.moveUp(PIX)
        if keys_pressed[pygame.K_s] and player.rect.y < 360:
            player.moveDown(PIX)

        #Calls the display function
        display()

#=====[ LAUNCH GAME ]=====
# Calls main loop
main()



