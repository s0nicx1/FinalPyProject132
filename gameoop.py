"""
COLIN: So far this version of our project contains:
- Player movement to the left and right
- Function for the player firing red projectiles upwards
- A player sprite
- A type of enemy sprite
COLIN: But it also lacks:
- A main menu with game options
- Player lives {and health?}
- Enemy variations, movements, attacks, spawning, and health
- Music for menu and game
- Arcade button compatibility
- A box to put it all in
"""

# Import pygame
import pygame

# Initialize the pygame module
pygame.init()

#=====[ IMAGES ]=====
# COLIN: Here, we can put other images for enemies and a possible player 2
# Grabs image for the player sprite
PLAYER = pygame.image.load("GalagaShip.png")
# Adjusts the image to fit onto the screen with desired (width, height)
PLAYER = pygame.transform.scale(PLAYER, (55, 40))

BUG1 = pygame.image.load("b1.png")
BUG1 = pygame.transform.scale(BUG1, (55, 40))

# Grab image for background
BG = pygame.image.load("space.jpg")

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
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = PLAYER

    def draw(self,window):
        window.blit(self.image, (self.x,self.y))

#------[ BUG TYPE 1 CLASS ]------
class Bug1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = BUG1
        self.health = 1

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def mov(self):
        for i in range(self.health):
            if self.x != 745 and self.y == 0:
                #print("x = {}".format(self.x))
                #print("y = {}".format(self.y))
                self.x += 5
            if self.x == 745 and self.y < 40:
                self.y += 5
            if self.x != 0 and self.y == 40:
                self.x -= 5
            if self.x == 0 and self.y < 80:
                self.y += 5
            if self.x < 745 and self.y == 80:
                self.x += 5


# Standalone function for the player's projectiles
def projectiles(player_proj):
    # For every instance of a projectile added to the list of projectiles
    for proj in player_proj:
        # Send a projectile 7 pixels up
        proj.y -= 7

#=====[ MAIN GAME LOOP ]=====
# COLIN: Here is where the game is run. It sets up the foundation of the pygame, then refers to several
# classes and functions to display the pygame.
def main():
    player_proj = []
    # This is a counter for the amount of waves the player has gone through
    wave = 0
    # Run set to True so the game doesn't end
    run = True
    # Sets the Frame Rate
    FPS = 35
    # Creates a clock that makes sure computer runs program at desired FPS
    clock = pygame.time.Clock()

    # create player at desired coordinates (400, 360)
    player = Player(400, 360)
    # Testing the bugs spawn at (0,0)
    b1 = Bug1(0,0)

    # This function, nested into the main loop, displays everything
    def display():
        # Blit (draw an object) the background at coordinates (0,0)
        WIN.blit(BG, (0,0))
        # Refreshes the surfaces that pygame is displaying
        player.draw(WIN)

        # For every instance of a projectile in the player's list of projectiles:
        for proj in player_proj:
            # draw it as a red rectangle
            pygame.draw.rect(WIN, RED, proj)

        if wave == 0:
            b1.draw(WIN)
            b1.mov()
            """b1.move_down()"""
        # Updates the window
        pygame.display.update()

    # Game loop for key controls
    while run:
        clock.tick(FPS)
        # Calls the above display function to update the pygame's surfaces

        display()
        # Player closes window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Run is set to False; main loop stops
                run = False
            # Player presses left control to fire (will be fixed with arcade GPIO)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print("FIRE!\n") COLIN: This was just to test to make sure the player was firing

                    # Projectile is set to be inside the player's x image and have a width of 5 and height of 5
                    proj = pygame.Rect(player.x + 55 / 2, player.y, 5, 5)
                    # Projectile is added to the player's list of projectiles
                    player_proj.append(proj)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and player.x - PIX > 0:
            player.x -= PIX
        if keys_pressed[pygame.K_d] and player.x + PIX + 55 < 799:
            player.x += PIX

        # Calls the projectiles function from the main loop
        projectiles(player_proj)

#=====[ LAUNCH GAME ]=====
# Calls main loop
main()



