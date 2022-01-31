import pygame
import game
import random
from selection_menu_1 import SelectionMenu1
from selection_menu_2 import SelectionMenu2
from players import Spaceship1, Spaceship2, PlayerLaser, Missile
from enemy import EnemyShip, EnemyLaser

# screen window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
divider = SCREEN_HEIGHT / 2

# general game variables
SCROLL_THRESH = 200
screen_scroll = 0
scroll_ctrl = True
TILE_SIZE = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('COSMIC CRUSADE')

# define colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self):
        # draw outline and 'empty' health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))

    def update(self, health):
        # update with new health
        self.health = health
        # calculate health ratio
        ratio = self.health / self.max_health
        # cover 'empty' health with current health value
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

class ItemOrb(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type

        # item images
        health_orb_img = pygame.image.load('img/objects/health_orb.png').convert_alpha()
        powerup_orb_img = pygame.image.load('img/objects/powerup_orb.png').convert_alpha()
        missile_orb_img = pygame.image.load('img/objects/missile_orb.png').convert_alpha()
        # dict to hold item options
        item_orbs = {
            'Health'    : health_orb_img,
            'Powerup'   : powerup_orb_img,
            'Missile'   : missile_orb_img,
        }
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
                self.kill()

# create sprite groups
player_group = pygame.sprite.Group()
enemy_group_upper = pygame.sprite.Group()
enemy_group_lower = pygame.sprite.Group()
laser_group_player = pygame.sprite.Group()
laser_group_enemy = pygame.sprite.Group()
missile_group = pygame.sprite.Group()
item_orb_group = pygame.sprite.Group()

# holds functions for world generation
class Cosmos():
    def __init__(self):
        pass

    def initial_gen(self):
        # calling to access selection dictionaries
        p1select = SelectionMenu1()
        p2select = SelectionMenu2()

        # default characters
        p1character = 'warrior_select'
        p2character = 'mage_select'

        # ERROR dict keys not changing
        for key in p1select.options_dict.keys():
            #print(key)
            if key == 'selected':
                p1character = key
                #print('selected found')
            else:
                pass
                #print('none selected')

        for key in p2select.options_dict.keys():
            if key == 'selected':
                p2character = key
                #print('selected found')
            else:
                pass
                #print('none selected')

        # create instances of players and their health bars
        player1 = Spaceship1(50, 150, 1.5, 7, 100, 3, p1character)
        health_bar1 = HealthBar(10, 10, player1.health, player1.health)
        player2 = Spaceship2(50, (divider + 150), 1.5, 7, 100, 3, p2character)
        health_bar2 = HealthBar(10, (divider + 10), player2.health, player2.health)
        health_bar1.draw()
        health_bar2.draw()
        player_group.add(player1)
        player_group.add(player2)

        # create first item orbs
        for x in range(random.randint(1, 2)):
            item_orb = ItemOrb('Health', random.randint(100, SCREEN_WIDTH - 10), random.randint(100, SCREEN_HEIGHT - 10))
            item_orb_group.add(item_orb)
            item_orb = ItemOrb('Powerup', random.randint(100, SCREEN_WIDTH - 10), random.randint(100, SCREEN_HEIGHT - 10))
            item_orb_group.add(item_orb)
            item_orb = ItemOrb('Missile', random.randint(100, SCREEN_WIDTH - 10), random.randint(100, SCREEN_HEIGHT - 10))
            item_orb_group.add(item_orb)

        # create first enemies
        for x in range(random.randint(1, 2)):
            # above divider
            enemy = EnemyShip('enemy', random.randint(400, SCREEN_WIDTH - 10), random.randint(150, divider - 10), 0.1, 5, 30, 0)
            # below divider
            enemy2 = EnemyShip('enemy', random.randint(300, SCREEN_WIDTH - 10), random.randint(divider + 10, SCREEN_HEIGHT - 10), 0.1, 5, 30, 0)
            enemy_group_upper.add(enemy)
            enemy_group_lower.add(enemy2)

        return player1, player2, health_bar1, health_bar2

    def continuous_gen(self):
        # generate more enemies off screen
        num_of_enemies = len(enemy_group_upper) + len(enemy_group_lower)
        min_enemy_x = 300
        max_enemy_x = 2000
        # gives each enemy a spawning 'zone'
        enemy_x_range = max_enemy_x - min_enemy_x
        enemy_zone_width = enemy_x_range - num_of_enemies
        # gives a gap between enemies
        pixel_buffer = 50
        # above divider or below divider
        y1 = random.randint(pixel_buffer, divider + pixel_buffer)
        y2 = random.randint(divider + pixel_buffer, SCREEN_HEIGHT + pixel_buffer)

        for i in range(num_of_enemies):
            min_x = min_enemy_x + enemy_zone_width * i + pixel_buffer / 2
            max_x = min_enemy_x + enemy_zone_width * (i + 1) - pixel_buffer / 2
            n = random.randint(1, 2)
            if n == 1:
                e = EnemyShip('enemy', random.randrange(min_x, max_x), y1, 0.1, 5, 30, 0)
                enemy_group_upper.add(e)
            if n == 2:
                e = EnemyShip('enemy', random.randrange(min_x, max_x), y2, 0.1, 5, 30, 0)
                enemy_group_lower.add(e)

        # generate more item orbs off screen
        num_of_orbs = len(item_orb_group)
        min_orb_x = 300
        max_orb_x = 2000
        # gives each item a spawning 'zone'
        orb_x_range = max_orb_x - min_orb_x
        orb_zone_width = orb_x_range - num_of_orbs
        # gives a gap between items
        pixel_buffer = 150
        # above divider or below divider
        y1 = random.randint(pixel_buffer, divider + pixel_buffer)
        y2 = random.randint(divider + pixel_buffer, SCREEN_HEIGHT + pixel_buffer)

        for i in range(num_of_orbs):
            min_x = min_orb_x + orb_zone_width * i + pixel_buffer / 2
            max_x = min_orb_x + orb_zone_width * (i + 1) - pixel_buffer / 2
            r = random.randint(1, 2)
            n = random.randint(1, 3)
            # generate above divider
            if r == 1:
                if n == 1:
                    o = ItemOrb('Health', random.randrange(min_x, max_x), y1)
                    item_orb_group.add(o)
                elif n == 2:
                    o = ItemOrb('Missile', random.randrange(min_x, max_x), y1)
                    item_orb_group.add(o)
                elif n == 3:
                    o = ItemOrb('Powerup', random.randrange(min_x, max_x), y1)
                    item_orb_group.add(o)
            # generate below divider
            if r == 2:
                if n == 1:
                    o = ItemOrb('Health', random.randrange(min_x, max_x), y2)
                    item_orb_group.add(o)
                elif n == 2:
                    o = ItemOrb('Missile', random.randrange(min_x, max_x), y2)
                    item_orb_group.add(o)
                elif n == 3:
                    o = ItemOrb('Powerup', random.randrange(min_x, max_x), y2)
                    item_orb_group.add(o)

cosmos = Cosmos()
