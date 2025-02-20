# import sfml.graphics
import json
import os.path
import pygame
import constants

# this file has been converted to pygame.

pygame.init()


# manages client, switches handlers
class ClientManager(object):
    def __init__(self, handler):
        # set display mode
        # self.window = sfml.graphics.RenderWindow(sfml.window.VideoMode(800, 600), title = "PyGG2 - Not Connected")

        self.window_surface = pygame.display.set_mode((800, 600))
        self.window = pygame.display
        self.clock = pygame.time.Clock()
        self.window.set_caption("PyGG2 - Not Connected")

        self.load_config()
        self.framerate_limit = self.config.setdefault('framerate_limit', 80)  # prevent 100% cpu usage
        # # self.window.vertical_synchronization = constants.VSYNC_ENABLED
        self.quitting = False
        self.newhandler = None
        self.newhandler_args = []
        self.newhandler_kwargs = {}

        self.handler = handler(self.window, self)

    def load_config(self):
        if os.path.exists('client_cfg.json'):
            with open('client_cfg.json', 'r') as fp:
                self.config = json.load(fp)
        else:
            self.config = {}

    def save_config(self):
        with open('client_cfg.json', 'w') as fp:
            json.dump(self.config, fp, indent=4)

    def run(self):
        while self.handler.step() and not self.quitting:
            if self.newhandler:
                self.handler.clearup()
                self.handler = self.newhandler(self.window, self, *self.newhandler_args, **self.newhandler_kwargs)
                self.newhandler = None
            self.clock.tick(self.framerate_limit)
            self.window.flip()  # Update window
        self.clearup()

    def switch_handler(self, handler, *args, **kwargs):
        self.newhandler = handler
        self.newhandler_args = args
        self.newhandler_kwargs = kwargs

    def quit(self):
        self.quitting = True

    def clearup(self):
        self.window.quit()
        self.save_config()


# handler base class, implements dummy handler
class Handler(object):
    def __init__(self, window, manager):
        self.manager = manager
        self.window = window

    # if the handler returns a non-true value, the game exits
    def step(self):
        return True

    # run when handler is about to be destroyed
    def clearup(self):
        pass
