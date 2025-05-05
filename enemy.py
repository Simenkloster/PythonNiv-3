
import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
  def __init__(self, enemy_type, waypoints, images):
    pg.sprite.Sprite.__init__(self)
    self.waypoints = waypoints
    self.pos = Vector2(self.waypoints[0])
    self.target_waypoint = 1
    self.health = ENEMY_DATA.get(enemy_type)["health"]
    self.speed = ENEMY_DATA.get(enemy_type)["speed"]
    self.angle = 0
    self.enemy_type = enemy_type
    self.original_image = images.get(enemy_type)
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def update(self, world):
    self.move(world)
    self.rotate()
    self.check_alive(world)

  def move(self, world):
    #define a target waypoint
    if self.target_waypoint < len(self.waypoints):
      self.target = Vector2(self.waypoints[self.target_waypoint])
      self.movement = self.target - self.pos
    else:
      #enemy has reached the end of the path
      self.kill()
      world.health -= 1
      world.missed_enemies += 1

    #calculate distance to target
    dist = self.movement.length()
    #check if remaining distance is greater than the enemy speed
    if dist >= (self.speed * world.game_speed):
      self.pos += self.movement.normalize() * (self.speed * world.game_speed)
    else:
      if dist != 0:
        self.pos += self.movement.normalize() * dist
      self.target_waypoint += 1

  def rotate(self):
    #calculate distance to next waypoint
    dist = self.target - self.pos
    #use distance to calculate angle
    self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
    #rotate image and update rectangle
    self.image = pg.transform.rotate(self.original_image, self.angle)
    self.rect = self.image.get_rect()
    self.rect.center = self.pos

  def check_alive(self, world):
    if self.health <= 0:
      world.killed_enemies += 1
      world.money += c.KILL_REWARD
      self.kill()


  def draw(self, surface):
    surface.blit(self.image, self.rect)

    bar_width = self.rect.width * 0.4
    bar_height = 5
    bar_x = self.rect.centerx - bar_width//2
    bar_y = self.rect.top + 5

    health_percent = self.health / ENEMY_DATA.get(self.enemy_type)["health"]

    if health_percent > 0.6:
      bar_color = (0, 255, 0)
    elif health_percent > 0.35:
      bar_color = (255, 255, 0)
    else:
      bar_color = (255, 0, 0)

    pg.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=3)

    pg.draw.rect(surface, bar_color, (bar_x, bar_y, int(bar_width * health_percent), bar_height), border_radius=3)


