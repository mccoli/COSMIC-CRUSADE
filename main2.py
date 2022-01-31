import pygame
# custom modules
from control import Control
from states import States
from button import Button
from start_menu import StartMenu
from selection_menu_1 import SelectionMenu1
from selection_menu_2 import SelectionMenu2
from game import Game
import players
import enemy
import world

pygame.init()

# load images
# screens
p1_select_warrior_img = pygame.image.load('img/background/player1_select_oriel.png').convert_alpha()
game_over_img = pygame.image.load('img/background/game_over.png').convert_alpha()


# create buttons
#restart_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, restart_img, 4)

#cosmos = Cosmos()

# # stuff every state uses
# def draw_text(text, text_colour, x, y):
#     font = pygame.font.Font('img/Heytext.ttf', 30)
#     img = font.render(text, True, text_colour)
#     screen.blit(img, (x, y))

settings = {
    'size'  : (800, 640),
    'fps'   : 60
}

app = Control(**settings)
state_dict = {
    'start_menu': StartMenu(),
    'selection_menu_1': SelectionMenu1(),
    'selection_menu_2': SelectionMenu2(),
    'game': Game()
}

app.setup_states(state_dict, 'start_menu')
app.main_game_loop()
pygame.quit()
running = False
while running:
    if restarts == 3:
        game_over = True

    if game_over == True:
        restart_game()
        # display game over and winner or tie
        screen.blit(game_over_img, (0, 0))
        draw_text(f'PLAYER 1 KILLS: {death_record_upper}', font, BLACK, 200, 300)
        draw_text(f'PLAYER 2 KILLS: {death_record_lower}', font, BLACK, 200, 400)
        draw_text('a game by Olivia McCallum. special thanks to Witty Wong and Leo Pettik', font, BLACK, 200, 600)
        if death_record_upper > death_record_lower:
            draw_text('PLAYER 1 WINS!', font, BLACK, 400, 200)
        elif death_record_lower > death_record_upper:
            draw_text('PLAYER 2 WINS!', font, BLACK, 400, 200)
        else:
            draw_text('YOU TIED!', font, BLACK, 350, 200)
