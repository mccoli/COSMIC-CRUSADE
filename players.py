import pygame
from states import States
from selection_menu_1 import SelectionMenu1
from selection_menu_2 import SelectionMenu2
import world
import game

class Spaceship1(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, health, missiles, character):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)

        self.character = character

        selection1 = SelectionMenu1()
        for key in selection1.options_dict.keys():
            if key == 'selected':
                self.character = key

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

        for player in world.player_group:
            if pygame.sprite.spritecollide(player, world.enemy_group_upper, False):
                if player.alive:
                    if self.damage_cooldown == 0:
                        self.damage_cooldown = 60
                        player.health -= 1
            if pygame.sprite.spritecollide(player, world.enemy_group_lower, False):
                if player.alive:
                    if self.damage_cooldown == 0:
                        self.damage_cooldown = 60
                        player.health -= 1

    def move(self, moving_down, moving_up, moving_right, moving_left):
        # reset movement variables
        world.screen_scroll = 0
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
        #pygame.draw.rect(screen, RED, self.rect, 1)

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            laser = PlayerLaser(self.rect.right + 3, self.rect.centery)
            world.laser_group_player.add(laser)

class Spaceship2(Spaceship1):
    def __init__(self, x, y, scale, speed, health, missiles, character):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)

        self.character = character

        selection2 = SelectionMenu2()
        for key in selection2.options_dict.keys():
            if key == 'selected':
                self.character = key

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

    def move(self, moving_down, moving_up, moving_right, moving_left):
        # reset movement variables
        world.screen_scroll = 0
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

class PlayerLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = pygame.image.load('img/objects/laser.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        #pygame.draw.rect(screen, RED, self.rect, 1)
        self.rect.x += self.speed + world.screen_scroll

        # delete if off screen
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

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
        if self.rect.right > SCREEN_WIDTH:
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
