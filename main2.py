import pygame
# CUSTOM MODULES
# controls state machine and main game loop
from control import Control
# object that holds properties shared by all states
from states import States
# button object that triggers events
from button import Button
# starting state and main menu
from start_menu import StartMenu
# supposed to allow player 1 to select a character
from selection_menu_1 import SelectionMenu1
# supposed to allow player 2 to select a character
from selection_menu_2 import SelectionMenu2
# main game
from game import Game
# handles game over scenario
from game_over import GameOver
# hold miscellaneous classes and functions
import players
import enemy
import world

pygame.init()

settings = {
    'size'  : (world.SCREEN_WIDTH, world.SCREEN_HEIGHT),
    'fps'   : 60
}

app = Control(**settings)
state_dict = {
    'start_menu': StartMenu(),
    'selection_menu_1': SelectionMenu1(),
    'selection_menu_2': SelectionMenu2(),
    'game': Game(),
    'game_over': GameOver(),
    'game': Game()
}

app.setup_states(state_dict, 'start_menu')
app.main_game_loop()
pygame.quit()
