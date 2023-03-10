#!/usr/bin/env python


import os

# import sfml

# This file has been mostly converted to pygame

import pygame

from . import Sprite as s

import function


class MapRenderer(object):
    def __init__(self, renderer, mapname):
        self.set_map(mapname)

    def set_map(self, mapname):
        # Get all the layers of the background
        self.bgs = []
        layer_list = os.listdir("maps/"+mapname+"/background")
        layer_list.sort()
        for layer in layer_list:
            self.bgs.append(s.Sprite(function.load_texture("maps/"+mapname+"/background/"+layer)))
        
        # Scale all maps 6x
        for background in self.bgs:
            background.ratio = pygame.math.Vector2(6, 6)
    
    def parallax_map(self, renderer, mapsprites):
        # the list passed to this function are the sprites between the foreground and background
        speed_increment = 1.0/(len(mapsprites)+1)
        for iteration, background in enumerate(mapsprites):
            multiplier = speed_increment * (iteration+1)
            background.position = (-renderer.xview * multiplier, -renderer.yview * ((multiplier + 3.0)/4))
            background.draw(renderer.window)  # Hopfully a Sprite class is passed here
    
    def render(self, renderer, state):
        # Background (Sky)
        self.bgs[0].position = renderer.get_screen_coords(0, 0)
        self.bgs[0].draw(renderer.window)
        
        # Backgrounds in between
        parallaxed_maps = self.bgs[1:-1]
        self.parallax_map(renderer, parallaxed_maps)
        
        # Foreground
        self.bgs[-1].position = renderer.get_screen_coords(0, 0)
        self.bgs[-1].draw(renderer.window)
    
