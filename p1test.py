import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('p1 test')

# set framerate
clock = pygame.time.Clock()
FPS = 60

class Spaceship1(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, health, missiles, character):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)

        self.character = character

        self.alive = True

        self.speed = speed

        self.shoot_cooldown = 0
        self.damage_cooldown = 0
        self.missiles = missiles

        # for health bar
        self.health = health
        self.max_health = self.health

        # load image and place in bounding box
        img = pygame.image.load(f'img/characters/{self.character}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # TODO: self.update_cooldowns for special powers
        self.check_alive()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

    def move(self, keys):
        # reset movement variables

        dy = 0
        dx = 0

        # assign movement values
        if keys[pygame.K_DOWN]:
            print('goin down')
            dy = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_LEFT]:
            dx = -self.speed

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, RED, self.rect, 1)


running = True
player = Spaceship1(100, 100, 1, 7, 10, 10, 'warrior_select')

while running:
    clock.tick(FPS)
    screen.fill((255, 0, 0))
    keys = pygame.key.get_pressed()
    player.draw(screen)
    player.update()
    player.move(keys)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
