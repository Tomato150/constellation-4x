# The file for the handling of game code.
import json
import jsonpickle
import datetime

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
        self.game_time = datetime.datetime(1000, 1, 1)

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

    def update_game_state_by_day(self):
        self.game_time += datetime.timedelta(1)
        for empire in self.galaxy.world_objects['empires'].values():
            # print('Example event for empire here')
            for colony in empire.colonies.values():
                # print('Example Colony event here')
                for construction_project in colony.construction_projects.values():
                    construction_project.construction_tick()
                # print('Example Colony event after construction project here')
                colony.delete_construction_projects()
            # print('Example event for empire after colony here')