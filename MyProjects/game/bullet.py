import pygame

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (0, 255, 200)


    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, 5, 15))

    def rect(self):
        return pygame.Rect(self.x, self.y, 5, 15)