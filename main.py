import pygame as pg
import json
from enemy import Enemy 
import constants as c
from turret import Turret
#initialise pygame 
pg.init()

#create clock
clock = pg.time.Clock()
#induvidual turret img for mouse cursor
cursour_turret = pg.image.load('assets/images/turrets/cursour_turret.png').convert_alpha
#create game window 
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defense")
#load images
enemy_image = pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha()










#NYTT!!!
#(#buttons
buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png')
upgrade_turret_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()

#create buttons 
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)

)




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

#game loop
run = True
while run:

    def create_turret(mouse_pos):

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







#create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True )




