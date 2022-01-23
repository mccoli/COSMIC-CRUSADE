import pygame
import random

pygame.init()

# screen window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
divider = SCREEN_HEIGHT / 2
SCROLL_THRESH = 200
screen_scroll = 0
TILE_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('COSMIC CRUSADE')

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
font = pygame.font.SysFont('Futura', 30)

# draw text
def draw_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))

def draw_bg():
    BG = pygame.image.load('img/background/test_scroll.png').convert_alpha()
    screen.blit(BG, (0, 0))
    pygame.draw.line(screen, WHITE, (0, divider), (SCREEN_WIDTH, divider))

# load images
BG = pygame.image.load('img/background/test_scroll.png').convert_alpha()
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

# player1 actions
moving_down1 = False
moving_up1 = False
moving_right1 = False
moving_left1 = False
shoot1 = False
missile1 = False
missile_shot1 = False

# player2 actions
moving_down2 = False
moving_up2 = False
moving_right2 = False
moving_left2 = False
shoot2 = False
missile2 = False
missile_shot2 = False

# for both players and enemy ships
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, character, x, y, scale, speed, health, missiles):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.alive = True

        # set vertical and horizontal speeds
        self.speed = speed

        self.shoot_cooldown = 0
        self.damage_cooldown = 0
        self.missiles = missiles

        # for health bar
        self.health = health
        self.max_health = self.health

        # enemy specific
        self.vision = pygame.Rect(0, 0, 300, 80)
        self.direction = 1
        self.move_counter = 0

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

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        for player in player_group:
            if pygame.sprite.spritecollide(player, enemy_group, False):
                if player.alive:
                    if self.damage_cooldown == 0:
                        self.damage_cooldown = 60
                        player.health -= 5

    def move(self, moving_down, moving_up, moving_right, moving_left):
        # reset movement variables
        screen_scroll = 0
        dy = 0
        dx = 0

        # assign movement values
        if moving_down:
            dy = self.speed
        if moving_up:
            dy = -self.speed
        if moving_right:
            dx = self.speed
        if moving_left:
            dx = -self.speed

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # check collision
        if self.rect.bottom + dy > divider:
            self.rect.bottom = divider - dy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left + dx < 0:
            self.rect.left = 0

        # update scroll based on player position? which player? or automatic
        if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH):
            self.rect.x -= dx
            screen_scroll = -dx

        return screen_scroll

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()

    def draw(self):
        screen.blit(self.image, self.rect)
        # show rects
        pygame.draw.rect(screen, RED, self.rect, 1)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            laser = PlayerLaser(self.rect.right + 3, self.rect.centery)
            laser_group_player.add(laser)

class Spaceship2(Spaceship):
    def move(self, moving_down, moving_up, moving_right, moving_left):
        # reset movement variables
        dy = 0
        dx = 0

        # assign movement values
        if moving_down:
            dy = self.speed
        if moving_up:
            dy = -self.speed
        if moving_right:
            dx = self.speed
        if moving_left:
            dx = -self.speed

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # check collision
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top + dy < divider:
            self.rect.top = divider - dy
        if self.rect.left + dx < 0:
            self.rect.left = 0

class EnemyShip(Spaceship):
    def move(self, moving_down, moving_up):
        # reset movement variables
        dy = 0
        dx = 0

        # assign movement values
        if moving_down:
            dy = self.speed
            self.direction = 1
        if moving_up:
            dy = -self.speed
            self.direction = -1

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # collision
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        # delete if they go off screen
        if self.rect.left < 0:
            self.kill()

    def update(self):
        # scroll
        self.rect.x += screen_scroll

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 40
            laser = EnemyLaser(self.rect.left + 5, self.rect.centery)
            laser_group_enemy.add(laser)

    def ai(self):
        # TODO - figure out how to apply to both players
        # check if near the player
        if self.vision.colliderect(player1.rect):
            # stop moving and shoot
            self.shoot()
        else:
            # automatic movement
            if self.direction == 1:
                ai_moving_down = True
            else:
                ai_moving_down = False
            ai_moving_up = not ai_moving_down

            self.move(ai_moving_down, ai_moving_up)
            self.move_counter += 1

            # update ai vision with movement
            self.vision.center = (self.rect.centerx - 100 ,self.rect.centery)
            pygame.draw.rect(screen, RED, self.vision)

            if self.move_counter > TILE_SIZE:
                self.direction *= -1
                self.move_counter *= -1


class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = laser_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        pygame.draw.rect(screen, RED, self.rect, 1)
        self.rect.x += self.speed + screen_scroll

        # delete if off screen
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, laser_group_player, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()

class EnemyLaser(PlayerLaser):
    def update(self):
        self.rect.x -= self.speed - screen_scroll

        # delete if off screen
        if self.rect.left < 0:
            self.kill()

        # do damage
        for player in player_group:
            if pygame.sprite.spritecollide(player, laser_group_enemy, False):
                if player.alive:
                    player.health -= 1
                    self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.images = []
        # missile animation
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
        self.rect.x += self.speed + screen_scroll

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

        # do damage
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, missile_group, False):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()

class ItemOrb(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_orbs[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        # check if player has picked up orb
        for player in player_group:
            if pygame.sprite.collide_rect(self, player):
                # check orb type
                if self.item_type == 'Health':
                    player.health += 25
                    if player.health > player.max_health:
                        player.health = player.max_health
                elif self.item_type == 'Missile':
                    player.missiles += 1
                # elif self.item_type == 'Powerup':
                #     player.powers

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

# create sprite groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
laser_group_player = pygame.sprite.Group()
laser_group_enemy = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
item_orb_group = pygame.sprite.Group()

# initial item orb generation
for x in range(random.randint(1, 2)):
    item_orb = ItemOrb('Health', random.randint(100, SCREEN_WIDTH - 10), random.randint(100, SCREEN_HEIGHT - 10))
    item_orb_group.add(item_orb)
    item_orb = ItemOrb('Powerup', random.randint(100, SCREEN_WIDTH - 10), random.randint(100, SCREEN_HEIGHT - 10))
    item_orb_group.add(item_orb)
    item_orb = ItemOrb('Missile', random.randint(100, SCREEN_WIDTH - 10), random.randint(100, SCREEN_HEIGHT - 10))
    item_orb_group.add(item_orb)

# initial enemy generation
for x in range(random.randint(1, 2)):
    # above divider
    enemy = EnemyShip('enemy', random.randint(400, SCREEN_WIDTH - 10), random.randint(150, divider - 10), 0.1, 5, 100, 0)
    # below divider
    enemy2 = EnemyShip('enemy', random.randint(300, SCREEN_WIDTH - 10), random.randint(divider + 10, SCREEN_HEIGHT - 10), 0.1, 5, 100, 0)
    enemy_group.add(enemy)
    enemy_group.add(enemy2)

# generate more enemies off screen
def enemy_generation():
    # TEMP - should be dependant on level length - don't generate on top of each other
    x1 = random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 400)
    y1 = random.randint(0, divider)
    x2 = random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 400)
    y2 = random.randint(divider, SCREEN_HEIGHT)
    for i in range(random.randint(1, 2)):
        if i == 1:
            e = EnemyShip('enemy', x1, y1, 0.1, 5, 100, 0)
            enemy_group.add(e)
        if i == 2:
            e = EnemyShip('enemy', x2, y2, 0.1, 5, 100, 0)
            enemy_group.add(e)

# TODO - item_orb generation off screen
#def item_orb_generation():

player1 = Spaceship('player', 50, 150, 0.15, 7, 100, 3)
health_bar1 = HealthBar(10, 10, player1.health, player1.health)
player2 = Spaceship2('player', 50, (divider + 150), 0.15, 7, 100, 3)
health_bar2 = HealthBar(10, (divider + 10), player2.health, player2.health)
player_group.add(player1)
player_group.add(player2)

running = True
i = 0

while running:
    clock.tick(FPS)
    time = clock.get_time()

    #draw_bg()
    screen.blit(BG, (0, 0))

    #world_gen()

    pygame.draw.line(screen, WHITE, (0, divider), (SCREEN_WIDTH, divider))

    # show players health
    health_bar1.draw(player1.health)
    health_bar2.draw(player2.health)

    # show missile count for player1
    draw_text('MISSILES: ', font, WHITE, 10, 35)
    # show missile count for player2
    draw_text('MISSILES: ', font, WHITE, 10, (35 + divider))

    for x in range(player1.missiles):
        screen.blit(missile_img, (125 + (x * 40), 40))
    # TODO: show health as hearts
    draw_text(f'HEALTH: {player1.health}', font, WHITE, 10, 60)

    for x in range(player2.missiles):
        screen.blit(missile_img, (125 + (x * 40), (40 + divider)))
    # TODO: show health as hearts
    draw_text(f'HEALTH: {player2.health}', font, WHITE, 10, (60 + divider))

    for player in player_group:
        player.update()
        player.draw()
    screen_scroll = player1.move(moving_down1, moving_up1, moving_right1, moving_left1)
    # bg_scroll -= screen_scroll
    player2.move(moving_down2, moving_up2, moving_right2, moving_left2)

    # TEMP - should be dependant on level length
    while i < 8:
        enemy_generation()
        i += 1

    for enemy in enemy_group:
        enemy.update()
        enemy.draw()
        if enemy.alive:
            enemy.ai()
        else:
            enemy.kill()

    # update and draw groups
    laser_group_player.update()
    laser_group_enemy.update()
    missile_group.update()
    item_orb_group.update()
    laser_group_player.draw(screen)
    laser_group_enemy.draw(screen)
    missile_group.draw(screen)
    item_orb_group.draw(screen)

    # update player1 actions
    if player1.alive:
        if shoot1:
            player1.shoot()
        elif missile1 and missile_shot1 == False and player1.missiles > 0:
            missile = Missile(player1.rect.centerx + 20, player1.rect.centery, 1)
            missile_group.add(missile)
            player1.missiles -= 1
            missile_shot1 = True

    # update player2 actions
    if player2.alive:
        if shoot2:
            player2.shoot()
        elif missile2 and missile_shot2 == False and player2.missiles > 0:
            missile = Missile(player2.rect.centerx + 20, player2.rect.centery, 1)
            missile_group.add(missile)
            player2.missiles -= 1
            missile_shot2 = True

    keys = pygame.key.get_pressed()

    # player 1 key presses
    if keys [pygame.K_DOWN]:
        moving_down1 = True
    if keys [pygame.K_UP]:
        moving_up1 = True
    if keys [pygame.K_RIGHT]:
        moving_right1 = True
    if keys [pygame.K_LEFT]:
        moving_left1 = True
    if keys [pygame.K_RCTRL]:
        shoot1 = True
    if keys [pygame.K_RSHIFT]:
        missile1 = True
    # player 2 key presses
    if keys [pygame.K_s]:
        moving_down2 = True
    if keys [pygame.K_w]:
        moving_up2 = True
    if keys [pygame.K_d]:
        moving_right2 = True
    if keys [pygame.K_a]:
        moving_left2 = True
    if keys [pygame.K_CAPSLOCK]:
        shoot2 = True
    if keys [pygame.K_x]:
        missile2 = True
    # quit with esc
    if keys [pygame.K_ESCAPE]:
        running = False

    # player 1 key releases
    if not keys [pygame.K_DOWN]:
        moving_down1 = False
    if not keys [pygame.K_UP]:
        moving_up1 = False
    if not keys [pygame.K_RIGHT]:
        moving_right1 = False
    if not keys [pygame.K_LEFT]:
        moving_left1 = False
    if not keys [pygame.K_RCTRL]:
        shoot1 = False
    if not keys [pygame.K_RSHIFT]:
        missile1 = False
        missile_shot1 = False
    # player 2 key releases
    if not keys [pygame.K_s]:
        moving_down2 = False
    if not keys [pygame.K_w]:
        moving_up2 = False
    if not keys [pygame.K_d]:
        moving_right2 = False
    if not keys [pygame.K_a]:
        moving_left2 = False
    if not keys [pygame.K_CAPSLOCK]:
        shoot2 = False
    if not keys [pygame.K_x]:
        missile2 = False
        missile_shot2 = False

    for event in pygame.event.get():
        # quit pygame
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
