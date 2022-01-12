import pygame
# TODO: SPRITE ANIMATION + eoSHOOTING BULLETS
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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# define font
# TODO: install appropriate font
font = pygame.font.SysFont('Futura', 30)

# draw text
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))

# draw background
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, divider), (SCREEN_WIDTH, divider))

# load images
# laser
laser_img = pygame.image.load('img/objects/laser.png').convert_alpha()
# missile
missile_img = pygame.image.load('img/missile/missile0.png').convert_alpha()
# pick up orbs
health_orb_img = pygame.image.load('img/objects/health_orb.png').convert_alpha()
powerup_orb_img = pygame.image.load('img/objects/powerup_orb.png').convert_alpha()
missile_orb_img = pygame.image.load('img/objects/missile_orb.png').convert_alpha()
item_orbs = {
    'Health'    : health_orb_img,
    'Powerup'   : powerup_orb_img,
    'Missile'   : missile_orb_img,
}

# player actions
moving_down = False
moving_up = False
moving_left = False
moving_right = False
shoot = False
missile = False
missile_shot = False

# for both players and enemy ships
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, character, x, y, scale, v_speed, h_speed, health, missiles):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.alive = True

        # set vertical and horizontal speeds
        self.v_speed = v_speed
        self.h_speed = h_speed
        self.direction = 1

        self.shoot_cooldown = 0
        self.missiles = missiles
        self.health = health

        # for health bar
        self.max_health = self.health

        # ai specific variables
        #self.move_vertical = 0

        # load image and place in bounding box
        img = pygame.image.load(f'img/characters/{self.character}/ship.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # self.update_animation()
        # TODO: self.update_cooldowns for special powers
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

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
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

    def draw(self):
        screen.blit(pygame.transform.rotate(self.image, -90), self.rect)
        # show rects
        pygame.draw.rect(screen, RED, self.rect, 1)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            laser = Laser(self.rect.right + 3, self.rect.centery)
            laser_group.add(laser)

    # ! TODO - logical error
    def ai(self):
        if self.alive and player1.alive:
            ai_moving_left = True
            ai_moving_right = False

            if self.direction == 1:
                ai_moving_up = True
            else:
                ai_moving_up = False
            ai_moving_down = not ai_moving_up

            if self.rect.top < 0:
                self.direction *= -1
                print(self.direction)

            self.move(ai_moving_down, ai_moving_up, ai_moving_left, ai_moving_right)
            #self.move_vertical += 1

class ItemOrb(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_orbs[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # check if player has picked up orb
        if pygame.sprite.collide_rect(self, player1):
            # check orb type
            if self.item_type == 'Health':
                player1.health += 25
                if player1.health > player1.max_health:
                    player1.health = player1.max_health
            elif self.item_type == 'Missile':
                player1.missiles += 1
            # elif self.item_type == 'Powerup':
            #     player1.powers

            # delete item_orb
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

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

        # check collision with characters
        # TODO: make sprite rects smaller
        # TODO: account for both players
        if pygame.sprite.spritecollide(player1, laser_group, False):
            # if player1.alive: TAB
            player1.health -= 5
            self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, laser_group, False):
                # if enemy.alive: TAB
                enemy.health -= 25
                print(enemy.health)
                self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.images = []
        for num in range(2):
            img = pygame.image.load(f'img/missile/missile{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # move missile
        self.rect.x += self.speed

        # run animation
        animation_speed = 6
        self.counter += 1

        if self.counter >= animation_speed:
            self.counter = 0
            self.frame_index += 1

            if self.frame_index >= len(self.images):
                self.frame_index = 0

        self.image = self.images[self.frame_index]

        # delete if off screen
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, missile_group, False):
                # if enemy.alive: TAB
                enemy.health -= 50
                print(enemy.health)
                self.kill()

# create sprite groups
enemy_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
item_orb_group = pygame.sprite.Group()

# temp - create item orbs
item_orb = ItemOrb('Health', 100, 150)
item_orb_group.add(item_orb)
item_orb = ItemOrb('Powerup', 150, 250)
item_orb_group.add(item_orb)
item_orb = ItemOrb('Missile', 125, 215)
item_orb_group.add(item_orb)

player1 = Spaceship('player', 200, 200, 0.15, 7, 7, 100, 3)
health_bar = HealthBar(10, 10, player1.health, player1.health)

enemy = Spaceship('enemy', 400, 200, 0.1, 7, 7, 100, 0)
enemy2 = Spaceship('enemy', 300, 100, 0.1, 7, 7, 100, 0)
enemy_group.add(enemy)
enemy_group.add(enemy2)

running = True

while running:
    clock.tick(FPS)

    draw_bg()
    # for size reference
    #pygame.draw.rect(screen, WHITE, (400, 400, 16, 16))
    # show player health
    health_bar.draw(player1.health)
    # show missile count
    draw_text('MISSILES: ', font, WHITE, 10, 35)
    for x in range(player1.missiles):
        screen.blit(missile_img, (125 + (x * 40), 40))
    # TODO: show health as hearts
    draw_text(f'HEALTH: {player1.health}', font, WHITE, 10, 60)

    player1.update()
    player1.draw()
    player1.move(moving_down, moving_up, moving_left, moving_right)

    for enemy in enemy_group:
        #enemy.ai()
        enemy.update()
        enemy.draw()

    # update and draw groups
    laser_group.update()
    missile_group.update()
    item_orb_group.update()
    laser_group.draw(screen)
    missile_group.draw(screen)
    item_orb_group.draw(screen)

    # update player actions
    if player1.alive:
        if shoot:
            player1.shoot()
        elif missile and missile_shot == False and player1.missiles > 0:
            missile = Missile(player1.rect.centerx + 20, player1.rect.centery, 4)
            missile_group.add(missile)
            player1.missiles -= 1
            missile_shot = True
            #print(player1.missiles)

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
            if event.key == pygame.K_RCTRL:
                shoot = True
            if event.key == pygame.K_RSHIFT:
                missile = True
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
            if event.key == pygame.K_RCTRL:
                shoot = False
            if event.key == pygame.K_RSHIFT:
                missile = False
                missile_shot = False

    pygame.display.update()

pygame.quit()
