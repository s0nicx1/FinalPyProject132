import pygame


pygame.init()

SIZE = 800, 400

WIN = pygame.display.set_mode(SIZE)

pygame.display.set_caption("Galaga test")

WIDTH = WIN.get_width()

HEIGHT = WIN.get_height()

BG = pygame.image.load("space.jpg")

background_color = (255, 255, 255)

button_color = (100, 100, 100)

button_color_2 = (200, 200, 200)

font = pygame.font.Font('8-BitMadness.ttf', 40)

text = font.render('quit', True, background_color)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()

    WIN.blit(BG, (0,0))

    mouse = pygame.mouse.get_pos()

    if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
        pygame.draw.rect(WIN, button_color, [WIDTH / 2, HEIGHT / 2, 140, 40])

    else:
        pygame.draw.rect(WIN, button_color_2, [WIDTH / 2, HEIGHT / 2, 140, 40])

    WIN.blit(text, (WIDTH/2+44, HEIGHT/2+6))

    pygame.display.update()


