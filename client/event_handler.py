

# add our main folder as include dir
import sys
sys.path.append("../")

import engine.map
import engine.player
import function
import constants
from networking import event_serialize


def Server_Event_Hello(client, networker, game, state, event):
    # Stop saying hello
    networker.has_connected = True
    # TODO: Some version check using event.version and constants.GAME_VERSION_NUMBER
    # Set all the important values to the game
    game.servername = event.servername
    player_id = event.playerid
    game.maxplayers = event.maxplayers
    game.map = engine.map.Map(game, event.mapname)
    client.start_game(player_id, state)


def Server_Event_Player_Join(client, networker, game, state, event):
    newplayer = engine.player.Player(game, state, event.id)
    newplayer.name = event.name
    

def Server_Event_Changeclass(client, networker, game, state, event):
    player = state.players[event.playerid]
    player.nextclass = function.convert_class(event.newclass)


def Server_Event_Die(client, networker, game, state, event):
    player = state.players[event.playerid]
    character = state.entities[player.character_id]
    character.die(game, state)


def Server_Event_Spawn(client, networker, game, state, event):
    player = state.players[event.playerid]
    player.spawn(game, state)


def Server_Snapshot_Update(client, networker, game, state, event):
    for player in list(state.players.values()):
        player.deserialize_input(event.internalbuffer)
        
        try:
            character = state.entities[player.character_id]
            character.deserialize(state, event.internalbuffer)
        except KeyError:
            # Character is dead
            pass


def Server_Full_Update(client, networker, game, state, event):
    numof_players = event.internalbuffer.read("B")
    # FIXME: Unclean mixing
    # Full update is going to roll over everything anyway, might as well start anew
    game.rendering_time = event.time

    for index in range(numof_players):
        player = engine.player.Player(game, state, index)
        player.name, player_class, character_exists = event.internalbuffer.read("32pBB")
        player.nextclass = function.convert_class(player_class)
        
        if character_exists:
            player.spawn(game, state)


def Server_Event_Disconnect(client, networker, game, state, event):
    player = state.players[event.playerid]
    print((player.name + " has disconnected"))
    player.destroy(game, state)


def Server_Event_Fire_Primary(client, networker, game, state, event):
    player = state.players[event.playerid]
    try:
        character = state.entities[player.character_id]
        weapon = state.entities[character.weapon_id]
        weapon.fire_primary(game, state)
    except IndexError:
        # character is dead or something. Shouldn't happen, so print something
        print("Error: Firing event called for dead or non-existent character!")


def Server_Event_Fire_Secondary(client, networker, game, state, event):
    player = state.players[event.playerid]
    try:
        character = state.entities[player.character_id]
        weapon = state.entities[character.weapon_id]
        weapon.fire_secondary(game, state)
    except IndexError:
        # character is dead or something. Shouldn't happen, so print something
        print("Error: Firing event called for dead or non-existent character!")


def Server_Event_Change_Map(client, networker, game, state, event):
    state.map = engine.map.Map(game, event.mapname)


# Gather the functions together to easily be called by the event ID
eventhandlers = {constants.EVENT_HELLO: Server_Event_Hello, constants.EVENT_PLAYER_JOIN: Server_Event_Player_Join,
                 constants.EVENT_PLAYER_CHANGECLASS: Server_Event_Changeclass,
                 constants.EVENT_PLAYER_DIE: Server_Event_Die, constants.EVENT_PLAYER_SPAWN: Server_Event_Spawn,
                 constants.SNAPSHOT_UPDATE: Server_Snapshot_Update, constants.FULL_UPDATE: Server_Full_Update,
                 constants.EVENT_PLAYER_DISCONNECT: Server_Event_Disconnect,
                 constants.EVENT_FIRE_PRIMARY: Server_Event_Fire_Primary,
                 constants.EVENT_FIRE_SECONDARY: Server_Event_Fire_Secondary,
                 constants.EVENT_CHANGE_MAP: Server_Event_Change_Map}
