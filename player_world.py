# The file for the handling of game code.
from game_code.game_logic import player_event_handlers

from game_code.game_logic.stellar_objects import galaxy


class PlayerWorld:
    def __init__(self):
        # The Galaxy Object is the base container for all other objects in the game.
        self.galaxy = galaxy.Galaxy()
        self.galaxy.generate_galaxy()
        self.player_command_mapping = {
            'start_construction_project': player_event_handlers.start_construction_project,
        }

    def generate_mock_game(self):
        empire = self.galaxy.create_new_empire('Player Faction')
        planet_id = str(self.galaxy.world_objects_id['planets'])
        self.galaxy.world_objects['stars']['0'].generate_planets(self.galaxy)
        self.galaxy.create_new_colony('Earth', self.galaxy.world_objects['stars']['0'].planets[planet_id], empire)

        print(self.galaxy.world_objects['stars']['0'].planets)

    def handle_player_input(self, name, target_object_ids, args):
        return self.player_command_mapping[name](self.galaxy, target_object_ids, args)
