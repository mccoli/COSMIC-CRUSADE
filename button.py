import pygame
import states
import control

class Button(object):
    def __init__(self, x, y, image, scale, command):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.hovered = False
        self.clicked = False
        self.command = command
        self.call_on_release = True

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    # ERROR the mouses movement is an event, not just the click itself
    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            #if user is still within button rect upon mouse release
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
        else:
            self.hovered = False

    def update(self):
        pass
