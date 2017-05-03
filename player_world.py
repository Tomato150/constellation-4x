# The file for the handling of game code.
import json
import jsonpickle
from datetime import datetime

from game_code.game_logic import player_event_handlers

from game_code.game_logic.stellar_objects import galaxies


class PlayerWorld:
    """
    The game state, but contains more data than just the raw game values. Integrated with the UI and Game logic. 
    """
    def __init__(self):
        """
        Initialize the player's world.       
        """
        # The Galaxy Object is the base container for all other objects in the game.
        self.player_empire = None
        self.galaxy = galaxies.Galaxy(self)
        self.game_speed = 1  # Game speed in seconds, represents how long a day is currently.

        self.to_delete_from_dict = list()

        # Change this eventually to be constructed from a load/new game
        self.set_up_world()

    def set_up_world(self):
        """
        Create stars for the galaxy. Created in a separate function in case the world is loaded in
        """
        self.galaxy.generate_galaxy()

    def generate_mock_game(self):
        """
        Generate a mock empire at the center of the universe for debugging purposes.
        """
        empire = self.galaxy.create_new_empire(
            name='Player Faction',
            flags={'player_faction': True}
        )

        planets = self.galaxy.world_objects['stars']['0'].generate_planets()
        self.galaxy.create_new_colony(
            name='Earth',
            flags={'capital': True},
            planet_instance=next(iter(planets.values())),  # Pick an arbitrary value, doesn't matter too much.
            empire_instance=empire
        )

        self.player_empire = self.galaxy.world_objects['empires']['0']

        print(self.galaxy.world_objects['stars']['0'].planets)

    def update_game_state(self, time_delta):
        game_time_delta = time_delta / self.game_speed  # Gives how many days have passed.
        for empire in self.galaxy.world_objects['empires'].values():
            # print('Example event for empire here')
            for colony in empire.colonies.values():
                # print('Example Colony event here')
                for construction_project in colony.construction_projects.values():
                    construction_project.construction_tick(game_time_delta)
                # print('Example Colony event after construction project here')
            # print('Example event for empire after colony here')

        for obj in self.to_delete_from_dict:
            del obj[0][obj[1]]
            self.to_delete_from_dict.remove(obj)
