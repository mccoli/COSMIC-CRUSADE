import pygame

class States(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

    def switch_state(self):
        self.done = True

    def quit_game(self):
        self.quit = True

# stuff every state uses
def draw_text(text, text_colour, x, y, screen):
    font = pygame.font.Font('img/Heytext.ttf', 30)
    img = font.render(text, True, text_colour)
    screen.blit(img, (x, y))
