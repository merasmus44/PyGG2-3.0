import pygame

# This should be used inplace of normal sfml sprites

class Sprite:
    def __init__(self, image, texture_rect):
        self.image = image
        self.texture_rectangle = texture_rect
        self.position = (0,0)
        self.image.convert_alpha()
        self.rotation = 0
        self.color = pygame.Color(0,0,0,0)
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

    def transparency(self):
        alpha_surface = pygame.Surface(self.get_size(), pygame.SRCALPHA)
        alpha_surface.fill((255, 255, 255, self.color.a))
        self.image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def apply_rotation(self):
        return pygame.transform.rotate(self.image, self.rotation)# Rotates counterclockwise in the positives

    def draw(self, window):
        self.texture_rectangle.x, self.texture_rectangle.y = self.position[0], self.position[1]
        window.blit(self.apply_rotation(), self.texture_rectangle)
        self.transparency()