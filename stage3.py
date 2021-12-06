import pygame

pygame.init()

# screen window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
divider = SCREEN_HEIGHT / 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('stage3')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
BG = (28, 8, 89)
RED = (255, 0, 0)

# draw background
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, divider), (SCREEN_WIDTH, divider))

# load images
laser_img = pygame.image.load('img/objects/laser.png').convert_alpha()

# player actions
moving_down = False
moving_up = False
moving_left = False
moving_right = False
shoot = False

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, character, x, y, scale, v_speed, h_speed):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)
        self.character = character

        # set vertical and horizontal speeds
        self.v_speed = v_speed
        self.h_speed = h_speed

        # load image and place in bounding box
        img = pygame.image.load(f'img/characters/{self.character}/ship.png').convert_alpha()
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

        # check collision
        if self.rect.bottom + dy > divider:
            self.rect.bottom = divider - dy
        if self.rect.left < 0:
            self.rect.left = 0


    def draw(self):
        screen.blit(pygame.transform.rotate(self.image, -90), self.rect)

    def shoot(self):
        laser = Laser(self.rect.right - 20, self.rect.centery)
        laser_group.add(laser)

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # move laser
        self.rect.x += self.speed
        # delete if off screen
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# create sprite groups
laser_group = pygame.sprite.Group()

player1 = Spaceship('player', 200, 200, 0.15, 7, 7)
enemy = Spaceship('enemy', 400, 200, 0.1, 7, 7)

running = True

while running:
    clock.tick(FPS)

    draw_bg()

    player1.draw()
    player1.move(moving_down, moving_up, moving_left, moving_right)

    enemy.draw()

    # update and draw groups
    laser_group.update()
    laser_group.draw(screen)

    if shoot:
        player1.shoot()
        # TODO: enemy.shoot() direction needs to be left not right

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
            if event.key == pygame.K_l:
                shoot = True
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
            if event.key == pygame.K_l:
                shoot = False

    pygame.display.update()

pygame.quit()

# def main():

# if __name__ == "__main__":
    # main()
