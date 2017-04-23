# The file for the handling of game code.
import json
import jsonpickle
import datetime

from game_code.game_logic import player_event_handlers

from game_code.game_logic.stellar_objects import galaxy


class PlayerWorld:
    def __init__(self):
        # The Galaxy Object is the base container for all other objects in the game.
        self.galaxy = galaxy.Galaxy()
        self.galaxy.generate_galaxy()

    def generate_mock_game(self):
        empire = self.galaxy.create_new_empire('Player Faction')
        planet_id = str(self.galaxy.world_objects_id['planets'])
        self.galaxy.world_objects['stars']['0'].generate_planets()
        self.galaxy.create_new_colony('Earth', self.galaxy.world_objects['stars']['0'].planets[planet_id], empire)

        print(self.galaxy.world_objects['stars']['0'].planets)
