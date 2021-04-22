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

#=====[ VARIABLES ]=====
# Constant variable representing a movement speed of 5 pixels for the player sprite
PIX = 5


#=====[ CREATE WINDOW ]======
# Constant variable for window's width (800) and height (400); RPi screen size
SIZE = 800, 400
# Constant variable for pygame creating the window
WIN = pygame.display.set_mode(SIZE)
# Sets caption for upper left corner of window
pygame.display.set_caption("Test")

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
        pass

#=====[ MAIN GAME LOOP ]=====
# Here is where the game is run.
# It sets up the foundation of the pygame, then refers to several
# classes and functions to display the pygame.
def main():
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

        if wave == 0:
            b1.draw(WIN)
            b1.mov()

        pygame.display.update()

    # Game loop for key controls
    while run:
        clock.tick(FPS)
        display()
        # Player closes window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Run is set to False; main loop stops
                run = False
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and player.x - PIX > 0:
            player.x -= PIX
        if keys_pressed[pygame.K_d] and player.x + PIX + 55 < 799:
            player.x += PIX

#=====[ LAUNCH GAME ]=====
# Calls main loop
main()



