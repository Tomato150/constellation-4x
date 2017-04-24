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
        self.player_empire = None

        # Change this eventually to be constructed from a load/new game
        self.set_up_world()

    def set_up_world(self):
        self.galaxy.generate_galaxy()
        self.player_empire = self.galaxy.world_objects['empires']['0']

    def generate_mock_game(self):
        empire = self.galaxy.create_new_empire(
            name='Player Faction',
            flags={'player_faction': True}
        )
        planets = self.galaxy.world_objects['stars']['0'].generate_planets()
        self.galaxy.create_new_colony(
            name='Earth',
            flags={'capital': True},
            planet_instance=next(iter(planets.values())),
            empire_instance=empire
        )

        print(self.galaxy.world_objects['stars']['0'].planets)

    def get_capitals(self):
        return self.player_empire.colonies['0'].parent_planet.parent_star, self.player_empire.colonies['0']
