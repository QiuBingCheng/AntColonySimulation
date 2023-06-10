import pygame


class Button:
    def __init__(self, position, size, image, callback):
        self.position = position
        self.size = size
        self.image = image
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect(topleft=position)
        self.callback = callback

    def change_image(self, image):
        self.image = image
        self.image = pygame.transform.scale(image, self.size)
        self.rect = self.image.get_rect(topleft=self.position)

    def on_click(self, pos):
        if self.rect.collidepoint(pos):
            print("call back is called")
            self.callback()
