import pygame
from states import States
from button import Button
import world

class SelectionMenu1(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'selection_menu_2'
        # button images
        healer_select_img = pygame.image.load('img/icons/healer_select.png').convert_alpha()
        rogue_select_img = pygame.image.load('img/icons/rogue_select.png').convert_alpha()
        warrior_select_img = pygame.image.load('img/icons/oriel_select.png').convert_alpha()
        mage_select_img = pygame.image.load('img/icons/zinta_select.png').convert_alpha()
        # create dictionary to hold buttons
        self.options_dict = {
            'healer_select': Button(5, 240, healer_select_img, 1, command=self.switch_state),
            'rogue_select': Button(205, 240, rogue_select_img, 1, command=self.switch_state),
            'warrior_select': Button(405, 240, warrior_select_img, 1, command=self.switch_state),
            'mage_select': Button(605, 240, mage_select_img, 1, command=self.switch_state)
        }
        # dictionary with altered keys
        self.selected_dict = {
            'healer_selected': Button(5, 240, healer_select_img, 1, command=self.switch_state),
            'rogue_selected': Button(205, 240, rogue_select_img, 1, command=self.switch_state),
            'warrior_selected': Button(405, 240, warrior_select_img, 1, command=self.switch_state),
            'mage_selected': Button(605, 240, mage_select_img, 1, command=self.switch_state)
        }

    def cleanup(self):
        print('cleaning up selection menu 1 state')

    def startup(self):
        print('loading selection menu 1 state')

    def draw(self, screen):
        # background
        player1_select_img = pygame.image.load('img/background/player1_select.png').convert_alpha()
        screen.blit(player1_select_img, (0, 0))

        # draw buttons to screen
        for key, value in self.options_dict.items():
            value.draw(screen)

    def select(self, key):
        # change key to 'selected' if event is triggered
        self.options_dict['selected'] = self.options_dict.pop(key)

    def get_event(self, event):
        # trigger event if button is clicked
        for key, value in self.options_dict.items():
            value.get_event(event)

        self.select(key)

    def update(self, screen, dt, keys):
        self.draw(screen)
