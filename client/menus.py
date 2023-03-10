import sys
import webbrowser
import socket
import uuid
import struct
import random

# this file has been mostly converted to pygame

# import sfml

import pygame
from pygame.constants import *
from . import Sprite as s

import constants
import function
from .handler import Handler
from .spritefont import SpriteFont
from .main import GameClientHandler


# generic menu handler
class MenuHandler(Handler):
    menuitems = []
    offsetx = 30
    offsety = 30
    spacing = 30

    def __init__(self, window, manager):
        self.manager = manager
        self.window = window

        self.font = SpriteFont(bold=True)
        self.prevleft = None

        self.window_focused = True
        self.joke_counter = 0

        self.window.set_caption('PyGG2 - ??? FPS:')

    def draw(self, hoveritem=None):
        x = self.offsetx
        y = self.offsety
        for item in self.menuitems:
            if item is hoveritem:
                width, height = self.font.stringSize(item[0])
                rect = pygame.Rect((x, y), (width, height))
                pygame.draw.rect(self.window, pygame.Color(255, 0, 0), rect)
            self.font.renderString(item[0], self.window, x, y)
            y += self.spacing

        self.window.flip()  # used to be display(), I think it does the same thing as flip

    def step(self):

        # check if user exited the game
        pressed = pygame.key.get_pressed()
        open = pygame.mouse.get_focused()
        if not open or pressed[K_ESCAPE]:
            return False
        for event in pygame.event.get():
            if event.type == QUIT:  # Press the 'x' button
                return False
            elif event.type == KEYDOWN:  # Key handler
                if event.key == K_ESCAPE:
                    return False
            if not pygame.mouse.get_focused():
                self.window_focused = False
            elif pygame.mouse.get_focused():
                self.window_focused = True

        if self.window_focused:
            # handle input
            mousepress = pygame.mouse.get_pressed(num_buttons=3)
            leftmouse = mousepress[0]
            mouse_x, mouse_y = pygame.mouse.get_pos()
        else:
            leftmouse = False
            mouse_x, mouse_y = (0, 0)
        x = self.offsetx
        y = self.offsety
        hoveritem = None
        for item in self.menuitems:
            width, height = self.font.stringSize(item[0])
            # are we hovering over this item?
            if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                hoveritem = item
                if leftmouse and not self.prevleft and item[1]:
                    args = [] if len(item) < 3 else item[2]
                    kwargs = {} if len(item) < 4 else item[3]
                    item[1](self, *args, **kwargs)
            y += self.spacing
        self.prevleft = leftmouse

        # draw stuff
        self.draw(hoveritem)

        return True


# handler for main menu
class MainMenuHandler(MenuHandler):
    def item_start_game(self):
        self.manager.switch_handler(GameClientHandler)

    def item_go_github(self):
        webbrowser.open('http://github.com/PyGG2/PyGG2')

    def item_go_lobby(self):
        self.manager.switch_handler(LobbyHandler)

    def item_quit(self):
        self.manager.quit()

    menuitems = [
        ('Start test client', item_start_game),
        ('Lobby', item_go_lobby),
        ("Go to Github", item_go_github),
        ('Quit', item_quit)
    ]

    offsetx = 10
    offsety = 120
    spacing = 30

    def __init__(self, window, manager):
        super(MainMenuHandler, self).__init__(window, manager)

        self.menubg = s.Sprite(function.load_texture(
            constants.SPRITE_FOLDER + "gameelements/menubackgrounds/%s.png" % random.randint(0, 2)))
        self.menubg.setx(200)
        self.color = tuple(self.manager.config.setdefault('menu_color', [0.7, 0.25, 0]))
        self.color = pygame.Color(self.color[0] * 255, self.color[1] * 255, self.color[2] * 255)

    def draw(self, hoveritem):
        self.menubg.draw(self.window)
        rect = pygame.Rect((0, 0), (200, 600))  # The (0,0) position might be problematic
        pygame.draw.rect(self.window, rect, self.color)

        super(MainMenuHandler, self).draw(hoveritem)


# handler for lobby
# noinspection PyTypeChecker
class LobbyHandler(MenuHandler):
    def join_server(self, host, port):
        self.manager.switch_handler(GameClientHandler, host, port)

    def display_info(self, url):
        webbrowser.open(url)

    def go_back(self):
        self.manager.switch_handler(MainMenuHandler)

    offsetx = 210
    offsety = 120
    spacing = 30

    def __init__(self, window, manager):
        super(LobbyHandler, self).__init__(window, manager)

        self.menuitems = [
            ('Back to Main Menu', LobbyHandler.go_back),
            ('', None)
        ]

        self.menubg = s.Sprite(function.load_texture(constants.SPRITE_FOLDER + "gameelements/menubackgrounds/0.png"))
        self.menubg.setx(200)
        self.menubg.setx(200)
        self.color = tuple(self.manager.config.setdefault('menu_color', [0.7, 0.25, 0]))
        self.color = pygame.Color(self.color[0] * 255, self.color[1] * 255, self.color[2] * 255)

        self.sendbuf = b''

        self.lobbysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.num_servers = -1
        self.servers_read = 0

        self.lobbysocket.connect((constants.LOBBY_HOST, constants.LOBBY_PORT))
        lobbyuuid = uuid.UUID(constants.LOBBY_MESSAGE_TYPE_LIST).get_bytes()
        self.protocoluuid = uuid.UUID(constants.GG2_LOBBY_UUID).get_bytes()
        self.send_all(lobbyuuid + self.protocoluuid)
        self.compatuuid = uuid.UUID(constants.PYGG2_COMPATIBILITY_PROTOCOL).get_bytes()

    def send_all(self, buf):
        while len(buf) > 0:
            sent = self.lobbysocket.send(buf)
            buf = buf[sent:]

    def recv_all(self, size):
        buf = b''
        while len(buf) < size:
            buf += self.lobbysocket.recv(size - len(buf))
        return buf
        # return self.lobbysocket.recv(size)

    def step(self):
        if self.num_servers == -1:
            num = self.recv_all(4)
            num = struct.unpack('>I', num)[0]
            self.num_servers = num
        elif self.servers_read < self.num_servers:
            length = self.recv_all(4)
            length = struct.unpack('>I', length)[0]
            if length > 100000:
                print('Server data block from lobby is too large')
                sys.exit(0)
            datablock = self.recv_all(length)
            server = {}
            items = struct.unpack('>BHBBBB18xHHHHH', datablock[:1 + 2 + 1 + 1 + 1 + 1 + 18 + 2 + 2 + 2 + 2 + 2])
            datablock = datablock[1 + 2 + 1 + 1 + 1 + 1 + 18 + 2 + 2 + 2 + 2 + 2:]
            server['protocol'], server['port'] = items[:2]
            server['ip'] = '.'.join([str(octet) for octet in items[2:6]])
            server['slots'], server['players'], server['bots'] = items[6:9]
            server['private'] = bool(items[9] & 1)
            infolen = items[10]
            server['infos'] = {}
            for i in range(infolen):
                keylen = struct.unpack('>B', datablock[0])[0]
                datablock = datablock[1:]
                key = datablock[:keylen]
                datablock = datablock[keylen:]
                datalen = struct.unpack('>H', datablock[:2])[0]
                datablock = datablock[2:]
                data = datablock[:datalen]
                datablock = datablock[datalen:]
                if key == 'protocol_id':
                    same_protocol_id = (data == self.compatuuid)
                server['infos'][key] = data
            server['compatible'] = (server['protocol'] == 1 and server['port'] > 0 and same_protocol_id)
            if server['bots']:
                playercount = '%s+%s' % (server['players'], server['bots'])
            else:
                playercount = str(server['players'])
            server['playerstring'] = '%s/%s' % (playercount, server['slots'])
            server['name'] = server['infos']['name']
            self.servers_read += 1

            if server['compatible']:
                label = '{0} - [{1}]'.format(server['name'], server['playerstring'])
                # noinspection PyTypeChecker
                self.menuitems.append((label, LobbyHandler.join_server, [server['ip'], server['port']]))
            else:
                label = '[INCOMPATIBLE: {0} {1}]: {2}'.format(server['infos']['game_short'],
                                                              server['infos']['game_ver'], server['name'])
                # noinspection PyTypeChecker
                self.menuitems.append((label, LobbyHandler.display_info, [server['infos']['game_url']]))
        return super(LobbyHandler, self).step()

    def draw(self, hoveritem):
        self.menubg.draw(self.window)
        rect = pygame.Rect((0, 0), (200, 600))  # (0,0) position might be problematic
        pygame.draw.rect(self.window, rect, self.color)

        super(LobbyHandler, self).draw(hoveritem)
