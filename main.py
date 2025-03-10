import pygame as pg
import json
from enemy import Enemy 
import constants as c
from turret import Turret
from world import World
#initialise pygame 
pg.init()

#create clock
clock = pg.time.Clock()
#induvidual turret img for mouse cursor
cursour_turret = pg.image.load('assets/images/turrets/cursour_turret.png').convert_alpha()
#create game window 
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")
#load images
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

waypoints = [
    (100, 100),
    (400, 200),
    (400, 100),
    (200, 300)
]

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)

def create_turret(mouse_pos):
        mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
        mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        if world.tile_map[mouse_tile_num] == 7:
            space_is_free = True
            for turret in turret_group:
               if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                   space_is_free = False
            if space_is_free == True:
                new_turret = Turret(cursour_turret,  mouse_tile_x,  mouse_tile_y)
                turret_group.add(new_turret)
           

#game loop
run = True
while run:


    #map koden her, ned under dette lol

        clock.tick(c.FPS)

        screen.fill("grey100")
        
        #update groups
        enemy_group.update()

        #draw groups
        enemy_group.draw(screen)
        turret_group.draw(screen)


        #event handler
        for event in pg.event.get():
            #quit program
            if event.type == pg.QUIT:
                run = False
            #mouse click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos() 
                create_turret(mouse_pos)
            #check if mouse is on the game area
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                pass
            

    #update display
        pg.display.flip()

pg.quit()




