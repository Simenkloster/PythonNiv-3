import pygame as pg

def load_spritesheets(turretType: str, upgradeLevel: int):
    print("Hentet " + turretType + " med upgrade level " + str(upgradeLevel) + " sine sprites")
    sheets = pg.image.load(f'assets/images/turrets/{turretType}sprites_{upgradeLevel}.png')
    return [sheets]

