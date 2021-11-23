import pygame

pygame.init()

# screen window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('shooting')

# sprite
x = 200
y = 200
scale = 0.5
img = pygame.image.load('ship.png')
img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
rect = img.get_rect()

running = True
while running:
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y -= 1
    if pressed[pygame.K_DOWN]: y += 1
    if pressed[pygame.K_LEFT]: x -= 1
    if pressed[pygame.K_RIGHT]: x += 1

    # boundaries - use rect not x, y
    if x <= 0:
        x = 0
    elif x >= SCREEN_WIDTH:
        x = SCREEN_WIDTH
    if y >= SCREEN_HEIGHT:
         y = SCREEN_HEIGHT
    elif y <= 0:
         y = 0

    # rect.center = (x, y)

    screen.blit(img, rect)

    for event in pygame.event.get():
        # quit pygame
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()
