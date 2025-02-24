import pygame as pg

class Turret(pg.sprite.Sprite):
    def __init__(self, image, pos):
        pg.sprite.Sprite._init_(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos