from turtle import speed

import pygame

class Enemy:
    def __init__(self, x, y, image_path, speed, descent):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (55, 55))
        self.x = x
        self.y = y
        self.speed = speed
        self.descent = descent
        self.direction = 1

    def move(self):
        self.x += self.speed * self.direction
        if self.x < 10 or self.x > 740:
            self.direction *= -1
            self.y += 20
        self.y += self.descent

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, 55, 55)