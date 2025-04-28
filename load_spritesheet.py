import pygame as pg

def load_spritesheets(turretType: str):
    sheets = pg.image.load(f'assets/images/turrets/{turretType}sprites.png')
    return [sheets]

