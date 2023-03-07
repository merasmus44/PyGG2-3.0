

import struct


#import sfml

import pygame
from pygame.constants import *
from . import Sprite as s

import function
import networking.databuffer
import networking.event_serialize

class InputHandler(object):
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.leftmouse = False
        self.middlemouse = False
        self.rightmouse = False
        self.aimdirection = 0
        
        self.keys = {}
        self.oldkeys = {}
    
    def gather_input(self, window, game):
        pressed = pygame.key.get_pressed()
        self.keys = {
                "up": pressed[K_w],
                "down": pressed[K_s],
                "left": pressed[K_a],
                "right": pressed[K_d]
            }
        
        self.up = self.keys["up"]
        self.down = self.keys["down"]
        self.left = self.keys["left"]
        self.right = self.keys["right"]
        pygame.event.get()
        mousepress = pygame.mouse.get_pressed(num_buttons=3)
        self.leftmouse = mousepress[0]
        self.middlemouse = mousepress[2]
        self.rightmouse = mousepress[1]
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.aimdirection = function.point_direction(window.width / 2, window.height / 2, mouse_x, mouse_y)
        
        inputbuffer = networking.databuffer.Buffer()
        self.serialize_input(inputbuffer)
        event = networking.event_serialize.ClientEventInputstate(inputbuffer)
        game.sendbuffer.append(event)


    def serialize_input(self, packetbuffer):
        keybyte = 0
        
        keybyte |= self.left << 0
        keybyte |= self.right << 1
        keybyte |= self.up << 2
        keybyte |= self.leftmouse << 3
        keybyte |= self.rightmouse << 4
        
        aim = int(round((self.aimdirection % 360) / 360 * 65535))
        
        packetbuffer.write("BH", (keybyte, aim))