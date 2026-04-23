import pygame

class Player:
    def __init__(self, x, y):
        
        self.image = pygame.image.load("MyProjects\\game\\player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, 60, 60)