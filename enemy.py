import pygame
import random
import world
from players import Spaceship1, PlayerLaser

class EnemyShip(Spaceship1):
    def __init__(self, character, x, y, scale, speed, health, missiles):
        # initialise the sprite
        pygame.sprite.Sprite.__init__(self)

        self.character = character
        self.alive = True
        self.speed = speed
        self.shoot_cooldown = 0
        self.damage_cooldown = 0
        self.missiles = missiles
        self.health = health
        self.max_health = self.health
        self.direction = 1
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 400, 200)

        # load image and place in bounding box
        img = pygame.image.load(f'img/characters/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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
        if self.rect.bottom > world.SCREEN_HEIGHT:
            self.rect.bottom = world.SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        # delete if they go off screen
        if self.rect.left < 0:
            self.kill()

    def update(self):
        self.check_alive()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # scroll
        self.rect.x += world.screen_scroll

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            laser = EnemyLaser(self.rect.left + 5, self.rect.centery)
            world.laser_group_enemy.add(laser)

    def ai(self):
        if self.alive:
            if self.idling == False and random.randint(1, 50) == 1:
                self.idling = True
                self.idling_counter = 50
                self.moving_up = False
                self.moving_down = False
            for player in world.player_group:
                if self.vision.colliderect(player.rect):
                    self.shoot()
            else:
                if self.idling == False:
                    # automatic movement
                    if self.direction == 1:
                        ai_moving_down = True
                    else:
                        ai_moving_down = False
                    ai_moving_up = not ai_moving_down

                    self.move(ai_moving_down, ai_moving_up)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx - 200, self.rect.centery)
                    #pygame.draw.rect(screen, RED, self.vision, 1)

                    if self.move_counter > world.TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

class EnemyLaser(PlayerLaser):
    def update(self):
        self.rect.x -= self.speed - world.screen_scroll

        # delete if off screen
        if self.rect.left < 0:
            self.kill()

        # do damage
        for player in world.player_group:
            if pygame.sprite.spritecollide(player, world.laser_group_enemy, False):
                if player.alive:
                    player.health -= 1
                    self.kill()
