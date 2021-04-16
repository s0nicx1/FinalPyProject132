# Import pygame
import pygame
# initialize the pygame module
pygame.init()

# constant variable for the window's Width and Height for the RPi
SIZE = 800, 400
# makes the window
WIN = pygame.display.set_mode(SIZE)
# window's name
pygame.display.set_caption("Test")

# =====[ CLASSES AND OTHER FUNCTIONS ]=====
# They go here

# =====[ MAIN GAME LOOP ]=====
def main():
    clock = pygame.time.Clock()
    # boolean variable, if false, game closes
    run = True
    while run:
        # sets frame rate, resets 60 times a second
        clock.tick(60)
        for event in pygame.event.get():
            # If user closes out the window
            if event.type == pygame.QUIT:
                # boolean variable set to false...
                run = False
                # closes window
                pygame.quit()
# calls the main() function
main()