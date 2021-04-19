"""
Colin: Made it using Tech with Tim's version of a space game. However, I don't plan on
using a complete copy of his code. If we're going to add a bunch more sprites and functions,
I'd rather use classes, where we can show off our knowledge of inheritance, polymorphism;
the whole shebang. It could get messy, and will definitely be lots of lines of code,
but I think it's better than having a function for each sprite on the screen.
If none of this code makes sense, just watch the video: https://www.youtube.com/watch?v=jO6qQDNa2UY
"""
# Import pygame
import pygame
# initialize the pygame module
pygame.init()

#=====[ SOME VARIABLES ]=====
# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# PIX is short for "pixels" and it's a constant variable to represent the player's speed of 5 pixels
PIX = 5
# PROJ is short for "projectile" and it's a constant variable that represents the projectile's speed of 7
PROJ = 7
# BG is short for "background" and it's a constant variable that houses the image for space
BG = pygame.image.load("space.jpg")
# grabs image for player
PLAYER = pygame.image.load("GalagaShip.png")
# adjusts the image to fit onto the screen with desired (width, height)
PLAYER = pygame.transform.scale(PLAYER, (55,40))

#======[ CREATE THE WINDOW ]=====
# constant variable for the window's Width and Height for the RPi
SIZE = 800, 400
# makes the window
WIN = pygame.display.set_mode(SIZE)
# window's name
pygame.display.set_caption("Test")

# =====[ CLASSES AND OTHER FUNCTIONS ]=====
# Function that corresponds a key press to the player's movement, and only works if player is in between
# the window's borders
def player_mov(keys_pressed, player):
    if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT] and player.x - PIX > 0:
        player.x -= PIX
    if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT] and player.x + PIX + player.width < 799:
        player.x += PIX

# Function that is used to handle projectiles, however, it lacks collision at the moment
def projectiles(player_proj):
    for proj in player_proj:
        proj.y -= PROJ
    # ADD A THING HERE FOR COLLISION

# Function that draws things on the window and updates them at 60 FPS
def draw_window(player,player_proj):
    # Fills window with a single background image/color
    WIN.blit(BG, (0,0))
    # Use blit to put text or an object or an image onto the screen
    # Blits player onto (x,y) coordinates
    WIN.blit(PLAYER, (player.x,player.y))
    # CREATE Projectiles
    for proj in player_proj:
        pygame.draw.rect(WIN, RED, proj)
    # Updates the window so frames can play out
    pygame.display.update()

# =====[ MAIN GAME LOOP ]=====
def main():
    # Create a rectangle for the player to be at (x,y,player_width,player_height)
    player = pygame.Rect(400,360,55,40)
    player_proj = []

    clock = pygame.time.Clock()
    # boolean variable, if false, game closes
    run = True
    while run:
        # sets frame rate, resets 35 times a second so RPi doesn't stutter
        clock.tick(35)
        for event in pygame.event.get():
            # If user closes out the window
            if event.type == pygame.QUIT:
                # boolean variable set to false...
                run = False
                # closes window
                pygame.quit()
            # Tracking player's projectiles
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL: #"""and len(player_proj) < MAX_PROJ"""
                    # Projectile is set to be inside the player's x image and have a width of 5 and height of 5
                    proj = pygame.Rect(player.x + player.width/2, player.y ,5,5)
                    player_proj.append(proj)

        # variable for pressing keys
        keys_pressed = pygame.key.get_pressed()
        # Calls function for player's movement
        player_mov(keys_pressed,player)
        # Calls function for player's projectiles
        projectiles(player_proj)
        # Calls function to update and draw everything on the screen
        draw_window(player,player_proj)

# calls the main() function
main()