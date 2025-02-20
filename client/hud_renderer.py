import math

import function
from . import spritefont
# import sfml

import pygame

# This file has been mostly converted to pygame

from . import Sprite as s

import engine.weapon
import constants


class HudRenderer(object):
    hud_sprite_istop = False

    def render(self, renderer, game, state):
        self.hudsprite.position = self.sprite_location
        self.hudsprite.ratio = pygame.math.Vector2(2, 2)
        if self.hud_sprite_istop:
            renderer.hud_sprites_top.append(self.hudsprite)
        else:
            renderer.hud_sprites_low.append(self.hudsprite)


class HealthRenderer(HudRenderer):
    hud_sprite_istop = True

    def __init__(self, renderer, game, state, character_id):
        self.sprite_location = (10, renderer.view_height - 75)
        character = state.entities[character_id]
        my_class_type = type(character)
        my_class_number = str(function.convert_class(my_class_type))

        self.hudsprite = s.Sprite(function.load_texture \
                                      (constants.SPRITE_FOLDER + "huds/characterhud/ " + my_class_number + ".png"))
        # function.load_texture calls pygame.image.load, no need to call it twice

        self.health_box_background = None
        self.health_box = None

        self.health_text = HealthText()
        self.health_text.health_location = (56, renderer.view_height - 52)
        self.health_text.health_size = (36, 36)

    def render(self, renderer, game, state, character_id):
        super(HealthRenderer, self).render(renderer, game, state)

        character = state.entities[character_id]
        character_hp = int(round(character.hp))

        character_maxhp = character.maxhp
        # always have at least 1 percent, can't divide by zero!
        health_percentage = max(0.01, (character_hp / character_maxhp))

        self.health_text.text = str(character_hp)

        # The black background behind green health
        self.health_box_background = DrawRectangle()
        self.health_box_background.location = (52, (renderer.view_height - 53))
        self.health_box_background.size = (40, 39)
        self.health_box_background.color = (0, 0, 0)
        renderer.hud_overlay.append(self.health_box_background)

        # The Green Health
        self.health_box = DrawRectangle()
        self.health_box.location = \
            (52, min((renderer.view_height - 12), (renderer.view_height - 53) + (39 - 39 * abs(health_percentage))))
        self.health_box.size = (40, max(0, int(39 * health_percentage)))

        if health_percentage > 0.5:
            exponent = 2  # The higher this will be, the quicker will the change happen, and the flatter will the
            # curve be
            # Color it green-yellow
            self.health_box.color = pygame.Color(int(((1 - 2 * (health_percentage - 0.5)) ** exponent) * 220), 220, 0,
                                                 255)  #
            # Pygame colors do not like floats
        else:
            exponent = 3  # The higher this will be, the quicker will the change happen, and the flatter will the
            # curve be
            # Color it yellow-red
            self.health_box.color = pygame.Color(255, int(((2 * health_percentage) ** exponent) * 255), 0, 255)
            # Pygame colors do not like floats
        renderer.hud_overlay.append(self.health_box)
        renderer.hud_overlay.append(self.health_text)


class AmmoRenderer(HudRenderer):
    hud_sprite_istop = False

    def initialize(self, renderer, game, state, character_id, spritepath):
        character = state.entities[character_id]
        if character.team == constants.TEAM_RED:
            team = "0"
        else:
            team = "1"
        self.hudsprite = s.Sprite(
            function.load_texture(constants.SPRITE_FOLDER + "huds/ammo/" + spritepath + "/" + team + ".png"))
        self.background_bar.location = self.bar.location
        self.background_bar.color = pygame.Color(0, 0, 0, 255)
        self.bar.color = pygame.Color(217, 217, 183, 255)

    def render(self, renderer, game, state, character_id):
        super(AmmoRenderer, self).render(renderer, game, state)

        character = state.entities[character_id]
        weapon = state.entities[character.weapon_id]

        scalar = 1 - weapon.reloadalarm / weapon.reloadtime
        self.bar.size = (int(scalar * self.background_bar.size[0]), self.background_bar.size[1])

        renderer.hud_overlay.append(self.background_bar)
        renderer.hud_overlay.append(self.bar)


# TODO: Fine-tune the self.sprite_location constants everywhere
class ScattergunAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "scattergunammos")


class FlamethrowerAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "flamethrowerammos")


class RocketlauncherAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        # TODO
        self.sprite_location = (renderer.view_width - 70, renderer.view_height - 75)
        self.initialize(renderer, game, state, character_id, "flamethrowerammos")


class MinigunAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "minigunammos")


class MinegunAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "minegunammos")


class NeedleAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "needleammos")


class ShotgunAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "shotgunammos")


class RevolverAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "revolverammos")


class BladeAmmoRenderer(AmmoRenderer):
    def __init__(self, renderer, game, state, character_id):
        self.bar = DrawRectangle()
        self.background_bar = DrawRectangle()
        self.sprite_location = (renderer.view_width - 120, renderer.view_height - 55)
        self.bar.location = (self.sprite_location[0] + 32, self.sprite_location[1] + 24)
        self.background_bar.size = (51, 8)
        self.initialize(renderer, game, state, character_id, "bladeammos")


def create_ammo_renderer(renderer, game, state, character_id):
    renderers = {
        engine.weapon.Scattergun: ScattergunAmmoRenderer,
        engine.weapon.Flamethrower: FlamethrowerAmmoRenderer,
        engine.weapon.Rocketlauncher: RocketlauncherAmmoRenderer,
        engine.weapon.Minigun: MinigunAmmoRenderer,
        engine.weapon.Minegun: MinegunAmmoRenderer,
        engine.weapon.Medigun: NeedleAmmoRenderer,
        engine.weapon.Shotgun: ShotgunAmmoRenderer,
        engine.weapon.Revolver: RevolverAmmoRenderer,
        engine.weapon.Blade: BladeAmmoRenderer,
    }
    character = state.entities[character_id]
    weapon = state.entities[character.weapon_id]
    return renderers[type(weapon)](renderer, game, state, character_id)


class DrawRectangle(object):
    def render(self, renderer, game, state):
        rect = pygame.Rect(self.location, self.size)
        # TO DRAW RECTS WE NEED TO USE pygame.draw.rect(window, color_list[color_var], rectangle)
        pygame.draw.rect(renderer.window, self.color, rect)


class HealthText(object):
    def __init__(self):
        self.font = spritefont.SpriteFont(bold=True)

    def render(self, renderer, game, state):
        tw, th = self.font.stringSize(self.text)
        tx = self.health_location[0] + (self.health_size[0] - tw) / 2
        ty = self.health_location[1] + (self.health_size[1] - th) / 2
        self.font.renderString(self.text, renderer.window, tx, ty, )
