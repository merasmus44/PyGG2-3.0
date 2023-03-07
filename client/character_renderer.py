

import constants
import math

import pygame

# This file has been mostly converted to pygame

import function
from . import spritefont

class ClassRenderer(object):
    def __init__(self):
        
        pass

    def render(self, renderer, game, state, character):
        anim_frame = int(character.animoffset)

        if not character.onground(game, state):
            anim_frame = 1

        if character.intel:
            anim_frame += 2

        sprite = self.sprites[anim_frame]
        
        if character.flip:
            sprite.ratio = pygame.math.Vector2(-1, 1)
            sprite.origin = self.spriteoffset_flipped
        else:
            sprite.ratio = pygame.math.Vector2(1, 1)
            sprite.origin = self.spriteoffset

        sprite.position = renderer.get_screen_coords(character.x, character.y)

        renderer.window.draw(sprite)
        
        # toggle masks
        if game.toggle_masks:
            rect_location = renderer.get_screen_coords(character.x, character.y)
            
            rect_size= character.collision_mask.get_size()
            rect_mask = pygame.Rect((0,0), rect_size)
            
            rect_mask.fill_color = (pygame.Color(255,0,0,125))
            rect_mask.position = (rect_location)

            renderer.window.draw(rect_mask) # we need to make sure we are drawing the correct class
        

def load_class_sprites(path):
    sprites = []
    for i in range(4):
        try:
            sprites.append(pygame.image.load((constants.SPRITE_FOLDER + f"{path}{i}.png")))
        except FileNotFoundError:
            pass
    return sprites


class ScoutRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/scoutreds/')

        self.spriteoffset = (24, 30)
        self.spriteoffset_flipped = (35, 30)

class PyroRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/pyroreds/')

        self.spriteoffset = (24, 30)
        self.spriteoffset_flipped = (35, 30)


class SoldierRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/soldierreds/')

        self.spriteoffset = (24, 30)
        self.spriteoffset_flipped = (35, 30)


class HeavyRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/heavyreds/')

        self.spriteoffset = (14, 30)
        self.spriteoffset_flipped = (26, 30)


class DemomanRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/demomanreds/')

        self.spriteoffset = (24, 30)
        self.spriteoffset_flipped = (35, 30)


class MedicRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/medicreds/')

        self.spriteoffset = (23, 30)
        self.spriteoffset_flipped = (36, 30)


class EngineerRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/engineerreds/')

        self.spriteoffset = (26, 30)
        self.spriteoffset_flipped = (36, 30)


class SpyRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/spyreds/')

        self.spriteoffset = (22, 30)
        self.spriteoffset_flipped = (33, 30)

    def render(self, renderer, game, state, character):
        if not character.cloaking:
            ClassRenderer.render(self, renderer, game, state, character)
            # FIXME: Why is the character still getting drawn on the screen if cloaked?


class QuoteRenderer(ClassRenderer):
    def __init__(self):
        self.depth = 0
        self.sprites = load_class_sprites('characters/quotereds/')

        self.spriteoffset = (16, -1)
        self.spriteoffset_flipped = (16, -1)
