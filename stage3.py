import pygame

pygame.init()

# screen window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('stage3')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
BG = (28, 8, 89)

# draw background
def draw_bg():
    screen.fill(BG)

# load images
bullet_img = pygame.image.load(img/objects/bullet.png).convert_alpha()

# player actions
moving_down = False
moving_up = False
moving_left = False
moving_right = False

class spaceship(pygame.sprite.Sprite):
    def __init__(self, character, x, y, scale, v_speed, h_speed):
        # initialise the dprite
        pygame.sprite.Sprite.__init__(self)
        self.character = character

        # set vertical and horizontal speeds
        self.v_speed = v_speed
        self.h_speed = h_speed

        # load image and place in bounding box
        img = pygame.image.load(f'characters/{self.character}/ship.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_down, moving_up, moving_left, moving_right):
        # reset movement variables
        dy = 0
        dx = 0

        # assign movement values
        if moving_down:
            dy = self.v_speed
        if moving_up:
            dy = -self.v_speed
        if moving_left:
            dx = -self.h_speed
        if moving_right:
            dx = self.h_speed

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.rotate(self.image, -90), self.rect)

player1 = spaceship('player', 200, 200, 0.15, 7, 7)
enemy = spaceship('enemy', 400, 200, 0.1, 7, 7)

running = True

while running:
    clock.tick(FPS)

    draw_bg()

    player1.draw()
    player1.move(moving_down, moving_up, moving_left, moving_right)

    enemy.draw()

    for event in pygame.event.get():
        # quit pygame
        if event.type == pygame.QUIT:
            running = False

        # key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                moving_down = True
            if event.key == pygame.K_UP:
                moving_up = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                running = False

        # key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                moving_down = False
            if event.key == pygame.K_UP:
                moving_up = False
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False

    pygame.display.update()

pygame.quit()

# def main():

# if __name__ == "__main__":
    # main()
