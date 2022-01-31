import pygame
import control
from states import States
from button import Button
from selection_menu_1 import SelectionMenu1

class SelectionMenu2(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'game'
        # button images
        healer_select_img = pygame.image.load('img/icons/healer_select.png').convert_alpha()
        rogue_select_img = pygame.image.load('img/icons/rogue_select.png').convert_alpha()
        warrior_select_img = pygame.image.load('img/icons/oriel_select.png').convert_alpha()
        mage_select_img = pygame.image.load('img/icons/zinta_select.png').convert_alpha()
        # create buttons
        self.options_dict = {
            'healer_select': Button(5, 240, healer_select_img, 1, command=self.switch_state),
            'rogue_select': Button(205, 240, rogue_select_img, 1, command=self.switch_state),
            'warrior_select': Button(405, 240, warrior_select_img, 1, command=self.switch_state),
            'mage_select': Button(605, 240, mage_select_img, 1, command=self.switch_state)
        }

    def cleanup(self):
        print('cleaning up selection menu 2 state')

    def startup(self):
        print('loading selection menu 2 state')

    def draw(self, screen):
        # background
        player2_select_img = pygame.image.load('img/background/player2_select.png').convert_alpha()
        screen.blit(player2_select_img, (0, 0))

        for value in self.options_dict.values():
            value.draw(screen)

    def get_event(self, event):
        for key, value in self.options_dict.items():
            value.get_event(event)
            key = 'selected'

    def update(self, screen, dt):
        self.draw(screen)
