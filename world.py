import pygame as pg

class World():
    def __init__(self, data, map_image):
        self.level_data = data
        self.image = map_image

    def process_data(self):
        #look throught data to extract relevant info
        for layer in self.level_data["layers"]:
            if layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoints_data = obj["polyline"]
                    print(waypoints_data)
    
    def process_waypoints(self, data):           

    
        def draw(self, surface):
            surface.blit(self.image,  (0, 0))