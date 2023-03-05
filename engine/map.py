#!/usr/bin/env python



import function

class Map(object):
    def __init__(self, game, mapname):
        self.set_map(mapname)
    
    def set_map(self, mapname):
        self.mapname = mapname
        
        self.collision_mask = function.load_mask("maps/"+mapname+"/wallmask.png")
        x, y = self.collision_mask.get_size()
        self.collision_mask = self.collision_mask.scale(x*6, y*6)
        
        self.width, self.height = self.collision_mask.get_size()