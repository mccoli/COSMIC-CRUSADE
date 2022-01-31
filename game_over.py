import pygame
from states import States, draw_text
from button import Button
import world
import players
import enemy
import control
from game import Game
game = Game()

class GameOver(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        # button images
        exit_img = pygame.image.load('img/icons/exit_img.png').convert_alpha()
        # create buttons
        self.exit_button = Button(world.SCREEN_WIDTH // 2 - 71, 500, exit_img, 2, command=self.quit_game)

    def cleanup(self):
        print('cleaning up game_over state')

    def startup(self):
        print('loading game_over state')
        # empyting groups for restart
        world.player_group.empty()
        world.enemy_group_upper.empty()
        world.enemy_group_lower.empty()
        world.laser_group_enemy.empty()
        world.laser_group_player.empty()
        world.missile_group.empty()
        world.item_orb_group.empty()

    def draw(self, screen):
        # background
        game_over_img = pygame.image.load('img/background/game_over.png').convert_alpha()
        screen.blit(game_over_img, (0, 0))
        # collecting scores
        player1_score, player2_score = game.check_score(screen)
        BLACK = world.BLACK

        self.exit_button.draw(screen)

        draw_text(f'PLAYER 1 KILLS: {player1_score}', BLACK, 200, 300, screen)
        draw_text(f'PLAYER 2 KILLS: {player2_score}', BLACK, 200, 400, screen)
        draw_text('a game by Olivia McCallum. special thanks to Witty Wong and Leo Pettik for their design help', BLACK, 30, 610, screen)
        if player1_score > player2_score:
            draw_text('PLAYER 1 WINS!', BLACK, 400, 200, screen)
        elif player2_score > player1_score:
            draw_text('PLAYER 2 WINS!', BLACK, 400, 200, screen)
        else:
            draw_text('YOU TIED!', BLACK, 370, 200, screen)

        # stopping movement and generative functions
        world.screen_scroll = 0
        game.init_gen = 0
        game.cont_gen = 0

    def get_event(self, event):
        self.exit_button.get_event(event)

    def update(self, screen, dt, keys):
        self.draw(screen)
