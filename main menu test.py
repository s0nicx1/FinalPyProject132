import pygame


pygame.init()

SIZE = 800, 400

WIN = pygame.display.set_mode(SIZE)

pygame.display.set_caption("Galaga test")

WIDTH = WIN.get_width()

HEIGHT = WIN.get_height()

BG = pygame.image.load("space.jpg")

# Text color (WHITE)
text_color = (255, 255, 255)
# Default button color (LIGHT GREY)
button_color = (200, 200, 200)
# Secondary button color (highlighted) (DARK GREY)
button_color_2 = (100, 100, 100)

# Text font and size
font = pygame.font.Font('8-BitMadness.ttf', 40)

# QUIT text
quit_text = font.render('quit', True, text_color)
# 1-Player text
one_player_text = font.render('1-Player', True, text_color)

#=====[ MAIN LOOP ]=====
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

    # Blit background image
    WIN.blit(BG, (0,0))

    # track mouse
    mouse = pygame.mouse.get_pos()

    #-----[ OTHER BUTTON ]-----
    pygame.draw.rect(WIN, button_color, [WIDTH / 2, 150, 140, 40])

    # OTHER BUTTON (HIGHLIGHT)
    if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and 150 < mouse[1] < 190:
        pygame.draw.rect(WIN, button_color_2, [WIDTH / 2, 150, 140, 40])
        if ev.type == pygame.MOUSEBUTTONDOWN:
            print("THIS IS A BUTTON")


    #-----[ QUIT BUTTON ]-----
    # Blit it on screen, default color, x = 400, y = 200, w = 140, h = 40
    pygame.draw.rect(WIN, button_color, [WIDTH / 2, HEIGHT / 2, 140, 40])

    # QUIT BUTTON (HIGHLIGHT)
    # If 400 < mouse x coordinate < 540 and 200 < mouse y coordinate < 240
    if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
        # Draw the same button, but use secondary color
        pygame.draw.rect(WIN, button_color_2, [WIDTH / 2, HEIGHT / 2, 140, 40])
        # If button is pressed while over QUIT BUTTON, Exit game
        if ev.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()



    #-----[ BUTTON TEXTS ]-----
    """Must be called after button color changes, as it must appear OVER THEM"""
    # QUIT TEXT
    WIN.blit(quit_text, (WIDTH / 2 + 40, HEIGHT / 2 + 6))
    # 1-PLAYER TEXT
    WIN.blit(one_player_text, (WIDTH / 2 , 156))

    # Displays mouse's coordinates for troubleshooting purposes
    #print(mouse)
    pygame.display.update()


