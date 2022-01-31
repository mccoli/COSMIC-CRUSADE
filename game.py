import pygame
from states import States, draw_text
from button import Button
import world
import players
import enemy
import control

# for manipulating player instances
player1 = None
player2 = None
health_bar1 = None
health_bar2 = None
player1_score = 0
player2_score = 0

class Game(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game_over'
        # counters for generative functions
        self.init_gen = 0
        self.cont_gen = 0

    def cleanup(self):
        print('cleaning up game state')

    def startup(self):
        print('loading game state')

    def initialise(self):
        # declaring as global so i can pass the values between functions
        global player1
        global player2
        global health_bar1
        global health_bar2

        # initial world generation
        if self.init_gen < 1:
            player1, player2, health_bar1, health_bar2 = world.cosmos.initial_gen()
            self.init_gen += 1

        return self.init_gen, player1, player2, health_bar1, health_bar2

    def draw(self, screen):
        pass

    def check_score(self, screen):
        # declaring as global so i can change in another functon
        global player1_score
        global player2_score
        # updating and drawing enemy groups
        for enemy_upper in world.enemy_group_upper:
            enemy_upper.update()
            enemy_upper.draw(screen)
            enemy_upper.ai()
            player1.total_score()
            if not enemy_upper.alive:
                player1_score += 1

        for enemy_lower in world.enemy_group_lower:
            enemy_lower.update()
            enemy_lower.draw(screen)
            enemy_lower.ai()
            player2.total_score()
            if not enemy_lower.alive:
                player2_score += 1

        return player1_score, player2_score

    def update(self, screen, dt, keys):
        self.init_gen, player1, player2, health_bar1, health_bar2 = self.initialise()

        # hidden missile for drawing missile count
        missile = players.Missile(-10, -10, 0)

        if self.init_gen == 1:
            # background
            screen.fill(world.BLACK)
            pygame.draw.line(screen, world.WHITE, (0, world.divider), (world.SCREEN_WIDTH, world.divider))

            # show healths
            health_bar1.update(player1.health)
            health_bar2.update(player2.health)

            # show missile counts
            draw_text('MISSILES: ', world.WHITE, 10, 35, screen)
            draw_text('MISSILES: ', world.WHITE, 10, (35 + world.divider), screen)
            for x in range(player1.missiles):
                screen.blit(missile.image, (125 + (x * 40), 40))
            draw_text(f'HEALTH: {player1.health}', world.WHITE, 10, 60, screen)
            for x in range(player2.missiles):
                screen.blit(missile.image, (125 + (x * 40), (40 + world.divider)))
            draw_text(f'HEALTH: {player2.health}', world.WHITE, 10, (60 + world.divider), screen)

            # draw and update players
            for player in world.player_group:
                player.update(keys)
                player.draw(screen)
            self.check_score(screen)

            # update player1 actions
            if player1.alive:
                if world.scroll_ctrl == True:
                    world.screen_scroll = player1.move(keys)
                else:
                    player1.move(keys)
                if player1.rect.x < player2.rect.x:
                    world.scroll_ctrl = False
                else:
                    world.scroll_ctrl = True

                if players.missile1 and players.missile_shot1 == False and player1.missiles > 0:
                    missile = players.Missile(player1.rect.centerx + 20, player1.rect.centery, 1)
                    world.missile_group.add(missile)
                    player1.missiles -= 1
                    players.missile_shot1 = True
            else:
                world.scroll_ctrl = False

            # update player2 actions
            if player2.alive:
                if world.scroll_ctrl == False:
                    world.screen_scroll = player2.move(keys)
                else:
                    player2.move(keys)

                if players.missile2 and players.missile_shot2 == False and player2.missiles > 0:
                    missile = players.Missile(player2.rect.centerx + 20, player2.rect.centery, 1)
                    world.missile_group.add(missile)
                    player2.missiles -= 1
                    players.missile_shot2 = True
            else:
                world.scroll_ctrl = True

            # if there are no more enemies, it's game over
            if (len(world.enemy_group_lower) + len(world.enemy_group_upper)) < 0:
                self.switch_state()

            # if both players have died, it's game over
            if not player1.alive and not player2.alive:
                self.switch_state()

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

        if self.init_gen == 1:

            # continue generating for x amount of iterations
            if self.cont_gen < 5:
                world.cosmos.continuous_gen()
                self.cont_gen += 1

            # quit with esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
