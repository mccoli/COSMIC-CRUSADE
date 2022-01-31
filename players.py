import pygame
from states import States
import selection_menu_1
import selection_menu_2
import world
import game

# old player1 actions
moving_down1 = False
moving_up1 = False
moving_right1 = False
moving_left1 = False
shoot1 = False
missile1 = False
missile_shot1 = False

# old player2 actions
moving_down2 = False
moving_up2 = False
moving_right2 = False
moving_left2 = False
shoot2 = False
missile2 = False
missile_shot2 = False

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
        self.score = 0

        # for health bar
        self.health = health
        self.max_health = self.health

        # load image and place in bounding box
        img = pygame.image.load(f'img/characters/{self.character}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, keys):
        self.check_alive()

        # key controls
        if keys[pygame.K_RCTRL]:
            self.shoot()
        if keys [pygame.K_RSHIFT]:
            Missile(self.rect.centerx + 20, self.rect.centery, 1)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        # collision damage
        for player in world.player_group:
            if pygame.sprite.spritecollide(player, world.enemy_group_upper, False):
                if player.alive:
                    if self.damage_cooldown == 0:
                        self.damage_cooldown = 60
                        player.health -= 1

    def move(self, keys):
        # reset movement variables
        world.screen_scroll = 0
        dy = 0
        dx = 0

        # assign movement values
        if keys[pygame.K_DOWN]:
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

        # check collision
        if self.rect.bottom + dy > world.divider:
            self.rect.bottom = world.divider - dy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left + dx < 0:
            self.rect.left = 0

        # update scroll based on player position
        if (self.rect.right > world.SCREEN_WIDTH - world.SCROLL_THRESH):
            self.rect.x -= dx
            world.screen_scroll = -dx

        return world.screen_scroll

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            laser = PlayerLaser(self.rect.right + 3, self.rect.centery)
            world.laser_group_player.add(laser)

    def total_score(self):
        # counts dead enemies within player 1's zone
        for enemy in world.enemy_group_upper:
            if not enemy.alive:
                self.score += 1
        return self.score

class Spaceship2(Spaceship1):
    def __init__(self, x, y, scale, speed, health, missiles, character):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)

        self.character = character

        self.alive = True

        self.speed = speed

        self.shoot_cooldown = 0
        self.damage_cooldown = 0
        self.missiles = missiles
        self.score = 0

        # for health bar
        self.health = health
        self.max_health = self.health

        # load image and place in bounding box
        img = pygame.image.load(f'img/characters/{self.character}.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, keys):
        self.check_alive()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        for player in world.player_group:
            if pygame.sprite.spritecollide(player, world.enemy_group_lower, False):
                if player.alive:
                    if self.damage_cooldown == 0:
                        self.damage_cooldown = 60
                        player.health -= 1

        if keys[pygame.K_CAPSLOCK]:
            self.shoot()
        if keys[pygame.K_x]:
            Missile(self.rect.centerx + 20, self.rect.centery, 1)

    def move(self, keys):
        # reset movement variables
        world.screen_scroll = 0
        dy = 0
        dx = 0

        # assign movement values
        if keys[pygame.K_s]:
            dy = self.speed
        if keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_a]:
            dx = -self.speed

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # check collision
        if self.rect.bottom > world.SCREEN_HEIGHT:
            self.rect.bottom = world.SCREEN_HEIGHT
        if self.rect.top + dy < world.divider:
            self.rect.top = world.divider - dy
        if self.rect.left + dx < 0:
            self.rect.left = 0

        if (self.rect.right > world.SCREEN_WIDTH - world.SCROLL_THRESH):
            self.rect.x -= dx
            world.screen_scroll = -dx

        return world.screen_scroll

    def total_score(self):
        # counts dead enemies within player 1's zone
        for enemy in world.enemy_group_lower:
            if not enemy.alive:
                self.score += 1
        return self.score

class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('img/objects/laser.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # scroll
        self.rect.x += self.speed + world.screen_scroll

        # delete if off screen
        if self.rect.right > world.SCREEN_WIDTH:
            self.kill()

        # lasers affect enemies in all zones
        for enemy in world.enemy_group_upper:
            if pygame.sprite.spritecollide(enemy, world.laser_group_player, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()
        for enemy in world.enemy_group_lower:
            if pygame.sprite.spritecollide(enemy, world.laser_group_player, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 7
        self.image = pygame.image.load('img/objects/missile.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        # move missile
        self.rect.x += self.speed + world.screen_scroll

        # delete if off screen
        if self.rect.right > world.SCREEN_WIDTH:
            self.kill()

        # do damage
        for enemy in world.enemy_group_upper:
            if pygame.sprite.spritecollide(enemy, world.missile_group, False):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()
        for enemy in world.enemy_group_lower:
            if pygame.sprite.spritecollide(enemy, world.missile_group, False):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()
