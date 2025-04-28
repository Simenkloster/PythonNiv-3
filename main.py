import pygame as pg
import json
from enemy import Enemy
from world import World
from turret import Turret
from button import Button
import constants as c
from turret_data import TURRETS_LIST
from load_spritesheet import load_spritesheets


#initialise pygame
pg.init()

#create clock
clock = pg.time.Clock()

#create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tower Defence")

#game variables
game_over = False
game_outcome = 0# -1 is loss & 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
menu_active = False



### LASTER INN BILDER, LYDER OG DATA TIL SPILLET ###


#load images
#map


map_image = pg.image.load('levels/level1/map 1.png').convert_alpha()
#load json data for level
with open('levels/level1/map 1.tmj') as file:
  world_data = json.load(file)



#turret spritesheets
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
  turret_sheet = pg.image.load(f'assets/images/turrets/turret_{x}.png').convert_alpha()
  turret_spritesheets.append(turret_sheet)

#individual turret image for mouse cursor
cursor_turret = pg.image.load('assets/images/turrets/cursor_turret.png').convert_alpha()
cursor_pancake = pg.image.load('assets/images/turrets/cursor_pancake.png').convert_alpha()
cursor_shooter = pg.image.load('assets/images/turrets/cursor_gunner.png').convert_alpha()
cursor_stabber = pg.image.load('assets/images/turrets/cursor_stabber.png').convert_alpha()

scale_factor = 2.3  # Adjust this to your liking


# Get original sizes
pancake_size = cursor_pancake.get_size()
shooter_size = cursor_shooter.get_size()
stabber_size = cursor_stabber.get_size()

# Scale images up
cursor_pancake = pg.transform.smoothscale(cursor_pancake, (int(pancake_size[0] * scale_factor), int(pancake_size[1] * scale_factor)))
cursor_shooter = pg.transform.smoothscale(cursor_shooter, (int(shooter_size[0] * scale_factor), int(shooter_size[1] * scale_factor)))
cursor_stabber = pg.transform.smoothscale(cursor_stabber, (int(stabber_size[0] * scale_factor), int(stabber_size[1] * scale_factor)))





#enemies
enemy_images = {
  "weak": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
  "medium": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
  "strong": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
  "elite": pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
}
#buttons
buy_turret_image = pg.image.load('assets/images/buttons/buy_turret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/buttons/cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets/images/buttons/upgrade_turret.png').convert_alpha()
begin_image = pg.image.load('assets/images/buttons/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/buttons/restart.png').convert_alpha()
fast_forward_image = pg.image.load('assets/images/buttons/fast_forward.png').convert_alpha()
#gui
heart_image = pg.image.load("assets/images/gui/heart.png").convert_alpha()
coin_image = pg.image.load("assets/images/gui/coin.png").convert_alpha()
logo_image = pg.image.load("assets/images/gui/logo.png").convert_alpha()

#load sounds
shot_fx = pg.mixer.Sound('assets/audio/shot.wav')
shot_fx.set_volume(0.5)



#load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)










### Funksjoner som vi trenger




#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def display_data():
  #draw panel
  pg.draw.rect(screen, "maroon", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
  pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 400), 2)
  screen.blit(logo_image, (c.SCREEN_WIDTH, 400))
  #display data
  draw_text("LEVEL: " + str(world.level), text_font, "grey100", c.SCREEN_WIDTH + 10, 10)
  screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 35))
  draw_text(str(world.health), text_font, "grey100", c.SCREEN_WIDTH + 50, 40)
  screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 65))
  draw_text(str(world.money), text_font, "grey100", c.SCREEN_WIDTH + 50, 70)
  

def create_turret(mouse_pos, turret_type):

  turret_spritesheets = load_spritesheets(turret_type)

  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  #calculate the sequential number of the tile

  mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
  #check if that tile is grass
  if world.tile_map[mouse_tile_num] == 14:

    #check that there isn't already a turret there
    space_is_free = True
    for turret in turret_group:
      if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
        space_is_free = False

    #if it is a free space then create turret
    if space_is_free == True:
      new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, shot_fx, turret_type)
      turret_group.add(new_turret)
      #deduct cost of turret
      world.money -= c.BUY_COST





def select_turret(mouse_pos):
  mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
  mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
  for turret in turret_group:
    if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
      return turret

def clear_selection():
  for turret in turret_group:
    turret.selected = False

def show_menu(screen, turret_images):
  
  global menu_active

  menu_active = True

  menu_width, menu_height = 300, 150

  menu_x, menu_y = (screen.get_width() - menu_width) // 2, (screen.get_height() - menu_height) // 2

  menu_surface = pg.Surface((menu_width, menu_height), pg.SRCALPHA )

  menu_surface.fill((0, 0, 0, 180))

  screen.blit(menu_surface, (menu_x, menu_y))




  button_width, button_height = 80, 80
  button_spacing = 20
  button_x = menu_x + 15
  button_y = menu_y + 35

  button_rects = []

  for i, turret in enumerate(TURRETS_LIST):
    btn_rect = pg.Rect(button_x + i * (button_width + button_spacing), button_y, button_width, button_height)
    pg.draw.rect(screen, (200, 200, 200), btn_rect, border_radius=5)
    screen.blit(turret_images[turret["name"]], btn_rect.topleft)
    
    button_rects.append((btn_rect, turret["name"]))
  


  pg.display.update()
  
  return button_rects


def check_menu_click(button_rects, mouse_pos):
  for rect, turret_type in button_rects:
    if rect.collidepoint(mouse_pos):
      return turret_type
  return None



def hide_menu():
  global menu_active
  menu_active = False







#create world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()
world.level = 15


#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()




#create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 50, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 5, 180, upgrade_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 60, 300, begin_image, True)
restart_button = Button(310, 300, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 50, 300, fast_forward_image, False)

#game loop
run = True
while run:

  clock.tick(c.FPS)

  menu_buttons = []

  #########################
  # UPDATING SECTION
  #########################

  if game_over == False:
    #check if player has lost
    if world.health <= 0:
      game_over = True
      game_outcome = -1 #loss
    #check if player has won
    if world.level > c.TOTAL_LEVELS:
      game_over = True
      game_outcome = 1 #win

    #update groups
    enemy_group.update(world)
    turret_group.update(enemy_group, world)

    #highlight selected turret
    if selected_turret:
      selected_turret.selected = True






  #########################
  # DRAWING SECTION
  #########################

  #draw level
  world.draw(screen)

  #draw groups
  enemy_group.draw(screen)
  for turret in turret_group:
    turret.draw(screen)

  display_data()




  #################################
  ###HVIS SPILLET FORTSATT PÅGÅR###
  #################################
  if game_over == False:
    #check if the level has been started or not
    if level_started == False:
      if begin_button.draw(screen):
        print("starter level" + str(world.level))
        level_started = True
    else:
      #fast forward option
      world.game_speed = 1
      if fast_forward_button.draw(screen):
        world.game_speed = 2
      #spawn enemies
      if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
        if world.spawned_enemies < len(world.enemy_list):
          enemy_type = world.enemy_list[world.spawned_enemies]
          enemy = Enemy(enemy_type, world.waypoints, enemy_images)
          enemy_group.add(enemy)
          world.spawned_enemies += 1
          last_enemy_spawn = pg.time.get_ticks()

    #check if the wave is finished
    if world.check_level_complete() == True:
      world.money += c.LEVEL_COMPLETE_REWARD
      world.level += 1
      level_started = False
      last_enemy_spawn = pg.time.get_ticks()
      world.reset_level()
      world.process_enemies()




    #draw buttons
    #button for placing turrets
    #for the "turret button" show cost of turret and draw the button
    draw_text(str(c.BUY_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 135)
    screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 130))

    if turret_button.draw(screen):
      menu_active = True


    if menu_active:
      menu_buttons = show_menu(screen, {
        "pancake": cursor_pancake,
        "shooter": cursor_shooter,
        "stabber": cursor_stabber
      })


    #if placing turrets then show the cancel button as well
    if placing_turrets == True:
      #show cursor turret
      cursor_rect = cursor_turret.get_rect()
      cursor_pos = pg.mouse.get_pos()
      cursor_rect.center = cursor_pos
      if cursor_pos[0] <= c.SCREEN_WIDTH:
        screen.blit(cursor_turret, cursor_rect)
      if cancel_button.draw(screen):
        placing_turrets = False
    #if a turret is selected then show the upgrade button
    
    
    
    if selected_turret:
      #if a turret can be upgraded then show the upgrade button
      if selected_turret.upgrade_level < c.TURRET_LEVELS:
        #show cost of upgrade and draw the button
        draw_text(str(c.UPGRADE_COST), text_font, "grey100", c.SCREEN_WIDTH + 215, 195)
        screen.blit(coin_image, (c.SCREEN_WIDTH + 260, 190))
        if upgrade_button.draw(screen):
          if world.money >= c.UPGRADE_COST:
            selected_turret.upgrade()
            world.money -= c.UPGRADE_COST





    #################################
    ###   HVIS DET ER GAME OVER   ###
    #################################          
  else:
    pass




  selected_turret_type = ""

  #event handler
  for event in pg.event.get():
    #quit program
    if event.type == pg.QUIT:
      run = False

    #mouse click
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mouse_pos = pg.mouse.get_pos()

      if menu_active:
        selected = check_menu_click(menu_buttons, mouse_pos)


        if selected:
          selected_turret_type = selected

          cost = next((t["cost"] for t in TURRETS_LIST if t["name"] == selected_turret_type), None)

          if world.money >= cost:
            placing_turrets = True
            hide_menu()

            if selected_turret_type == "pancake":
              cursor_turret = cursor_pancake
            if selected_turret_type == "shooter":
              cursor_turret = cursor_shooter
            if selected_turret_type == "stabber":
              cursor_turret = cursor_stabber
          continue

        else:
          menu_active = False






      #check if mouse is on the game area
      if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
        #clear selected turrets
        selected_turret = None
        clear_selection()
        if placing_turrets == True:
          #check if there is enough money for a turret
          if world.money >= c.BUY_COST:
            create_turret(mouse_pos, selected)
            placing_turrets = False
        else:
          selected_turret = select_turret(mouse_pos)

  


  #update display
  pg.display.flip()

pg.quit()