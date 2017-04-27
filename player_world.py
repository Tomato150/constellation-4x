# The file for the handling of game code.
import json
import jsonpickle
from datetime import datetime

from game_code.game_logic import player_event_handlers

from game_code.game_logic.stellar_objects import galaxy


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
        self.galaxy = galaxy.Galaxy(self)

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

    def game_loop(self):
        pass
