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

    def load_game(self, save_name):
        save_file = save_name + '.sav'
        with open(save_file, 'r') as savefile:
            unpickled_world = jsonpickle.decode(''.join(line.rstrip() for line in savefile))
        print("Game loaded")

    def save_game(self, save_name):
        pickled_world = jsonpickle.encode(self)
        save_file = save_name + '.sav'
        with open(save_file, 'w') as savefile:
            savefile.write(json.dumps(json.loads(pickled_world), indent=4, sort_keys=True))
        print("Save Completed, File Name:", save_file)

if __name__ == "__main__":
    pw = PlayerWorld()
    pw.generate_mock_game()
    date1 = datetime.datetime.now()
    pw.save_game('dank_meme')
    date2 = datetime.datetime.now()
    print(date2 - date1)
    pw.load_game('dank_meme')
    print(datetime.datetime.now() - date2)
