import pygame
from states import States
from button import Button

class StartMenu(States):
    def __init__(self):
        States.__init__(self)
        self.next = 'selection_menu_1'
        # button images
        start_img = pygame.image.load('img/icons/start_img.png').convert_alpha()
        exit_img = pygame.image.load('img/icons/exit_img.png').convert_alpha()
        controls_img = pygame.image.load('img/icons/controls_img.png').convert_alpha()
        # create buttons
        self.start_button = Button(410, 440, start_img, 2.5, command=self.switch_state)
        self.controls_button = Button(7, 125, controls_img, 2.5, command=self.switch_state)
        self.exit_button = Button(7, 235, exit_img, 2.5, command=pygame.QUIT)

    def cleanup(self):
        print('cleaning up start menu state')

    def startup(self):
        print('loading start menu state')

    def draw(self, screen):
        # background
        main_menu_img = pygame.image.load('img/background/main_menu.png').convert_alpha()
        screen.blit(main_menu_img, (0, 0))

        self.start_button.draw(screen)
        self.controls_button.draw(screen)
        self.exit_button.draw(screen)

    def get_event(self, event):
        # when clicked, trigger command
        self.start_button.get_event(event)
        self.controls_button.get_event(event)
        self.exit_button.get_event(event)

    def update(self, screen, dt, keys):
        self.draw(screen)
