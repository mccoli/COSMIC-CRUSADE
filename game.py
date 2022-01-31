import pygame
from states import States, draw_text
from button import Button
import world
import players
import enemy

#where lol
#restart_img = pygame.image.load('img/icons/restart_img.png').convert_alpha()

# GLOBAL VARIABLES
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

# for manipulating player instances
player1 = None
player2 = None
health_bar1 = None
health_bar2 = None

# secret missile hehe
missile = players.Missile(-10, -10, 0)

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game_over'
        # counters for generative functions
        self.init_gen = 0
        self.cont_gen = 0
        # for game over
        self.restarts = 0
        # for high scores
        self.death_record_upper = 0
        self.death_record_lower = 0

    def cleanup(self):
        print('cleaning up game state')

    def startup(self):
        print('loading game state')

    # reset game
    def restart_game(self):
        world.player_group.empty()
        world.enemy_group_upper.empty()
        world.enemy_group_lower.empty()
        world.laser_group_enemy.empty()
        world.laser_group_player.empty()
        world.missile_group.empty()
        world.item_orb_group.empty()

    def initialise(self):
        global player1
        global player2
        global health_bar1
        global health_bar2

        if self.init_gen < 1:
            player1, player2, health_bar1, health_bar2 = world.cosmos.initial_gen()
            self.init_gen += 1

        return self.init_gen, player1, player2, health_bar1, health_bar2

    def draw(self, screen):
        pass

    def update(self, screen, dt):
        self.init_gen, player1, player2, health_bar1, health_bar2 = self.initialise()

        if self.init_gen == 1:
            screen.fill(world.BLACK)
            pygame.draw.line(screen, world.WHITE, (0, world.divider), (world.SCREEN_WIDTH, world.divider))
            # show healths
            health_bar1.update(player1.health)
            health_bar2.update(player2.health)

            # show missile counts
            draw_text('MISSILES: ', world.WHITE, 10, 35, screen)
            draw_text('MISSILES: ', world.WHITE, 10, (35 + world.divider), screen)
            #missile_img = pygame.image.load('img/objects/missile.png').convert_alpha()

            for x in range(player1.missiles):
                screen.blit(missile.image, (125 + (x * 40), 40))
            draw_text(f'HEALTH: {player1.health}', world.WHITE, 10, 60, screen)

            for x in range(player2.missiles):
                screen.blit(missile.image, (125 + (x * 40), (40 + world.divider)))
            draw_text(f'HEALTH: {player2.health}', world.WHITE, 10, (60 + world.divider), screen)

            for player in world.player_group:
                player.update()
                player.draw(screen)

            # updating and drawing enemy groups
            for enemy_upper in world.enemy_group_upper:
                enemy_upper.update()
                enemy_upper.draw(screen)
                enemy_upper.ai()
                if not enemy_upper.alive:
                    self.death_record_upper += 1

            for enemy_lower in world.enemy_group_lower:
                enemy_lower.update()
                enemy_lower.draw(screen)
                enemy_lower.ai()
                if not enemy_lower.alive:
                    self.death_record_lower += 1

            # update and draw groups
            world.laser_group_player.update()
            world.laser_group_enemy.update()
            world.missile_group.update()
            world.item_orb_group.update()
            world.laser_group_player.draw(screen)
            world.laser_group_enemy.draw(screen)
            world.missile_group.draw(screen)
            world.item_orb_group.draw(screen)


    def get_event(self, event):
        self.init_gen, player1, player2, health_bar1, health_bar2 = self.initialise()

        # player1 actions
        global moving_down1
        global moving_up1
        global moving_right1
        global moving_left1
        global shoot1
        global missile1
        global missile_shot1

        # player2 actions
        global moving_down2
        global moving_up2
        global moving_right2
        global moving_left2
        global shoot2
        global missile2
        global missile_shot2

        if self.init_gen == 1:
            #print('game is running')

            if self.cont_gen < 2:
                world.cosmos.continuous_gen()
                self.cont_gen += 1

            for player in world.player_group:
                player.update()

            # update player1 actions
            if player1.alive:
                # p1 controls screen scrolling as long as they're alive
                if world.scroll_ctrl == True:
                    world.screen_scroll = player1.move(moving_down1, moving_up1, moving_right1, moving_left1)
                else:
                    player1.move(moving_down1, moving_up1, moving_right1, moving_left1)
                if player1.rect.x < player2.rect.x:
                    world.scroll_ctrl = False
                else:
                    world.scroll_ctrl = True
                if shoot1:
                    player1.shoot()
                elif missile1 and missile_shot1 == False and player1.missiles > 0:
                    missile = Missile(player1.rect.centerx + 20, player1.rect.centery, 1)
                    missile_group.add(missile)
                    player1.missiles -= 1
                    missile_shot1 = True
            else:
                world.scroll_ctrl = False

            # update player2 actions
            if player2.alive:
                if world.scroll_ctrl == False:
                    world.screen_scroll = player2.move(moving_down2, moving_up2, moving_right2, moving_left2)
                else:
                    player2.move(moving_down2, moving_up2, moving_right2, moving_left2)
                if shoot2:
                    player2.shoot()
                elif missile2 and missile_shot2 == False and player2.missiles > 0:
                    missile = Missile(player2.rect.centerx + 20, player2.rect.centery, 1)
                    missile_group.add(missile)
                    player2.missiles -= 1
                    missile_shot2 = True
            else:
                world.scroll_ctrl = True

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
                pygame.quit()

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


        if not player1.alive and not player2.alive:
            #restart_button = Button(world.SCREEN_WIDTH // 2 - 150, world.SCREEN_HEIGHT // 2 - 100, restart_img, 4, restart_game())
            world.screen_scroll = 0
            self.init_gen = 0
            self.cont_gen = 0
            # TEMP - testing
            self.restarts += 3
            if self.restarts == 3:
                switch_state()

        pygame.event.pump()
