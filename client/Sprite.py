import pygame

# This should be used inplace of normal sfml sprites

class Sprite:
    def __init__(self, image, texture_rect):
        self.image = image
        self.texture_rectangle = texture_rect
        self.position = (0,0)
        if not self.texture_rectangle:
            self.texture_rectangle = self.image.get_rect()

    def setx(self, x):
        self.position = list(self.position)
        self.position[0] = x
        self.position = tuple(self.position)

    def sety(self, y):
        self.position = list(self.position)
        self.position[1]= y
        self.position = tuple(self.position)

    def draw(self, window):
        self.texture_rectangle.x, self.texture_rectangle.y = self.position[0], self.position[1]
        window.blit(self.image, self.texture_rectangle)
        self.update_values()