from Color import Color
import pygame


class Element:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.color = Color.BLUE

    def change_image(self, image):
        self.image = image
        self.image = pygame.transform.scale(image, (self.rect.width,self.rect.height))

    def draw(self, surface):
       # pygame.draw.rect(screen, self.color, self.rect)
       surface.blit(self.image, self.rect)

    def plot_image(self, surface):
        surface.blit(self.image, self.rect)
