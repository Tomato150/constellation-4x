from game_modules import utility_functions

from game_data.constants import galaxy_generation_constants as constants, general_constants

import random


class Star:
	def __init__(self, star_id, x, y, galaxy, **kwargs):
		# System General information
		self.galaxy = galaxy
		self.ids = {'self': star_id}
		self.name = utility_functions.name_creator(random.randint(2, 3), random.randint(3, 5), random.randint(1, 2))

		# System Location Information
		self.coordinates = [int(x), int(y)]

		# Star type information
		star = random.choice(constants.STARS[0])
		self.star_type = star[0]
		self.file_path = random.choice(star[1])

		# System Contents information:
		self.planets = {}  # A dict of {id's: instances} of planet keys.

		# Update kwargs
		self.__dict__.update(kwargs)

		galaxy.world_objects['stars'][self.ids['self']] = self

	def generate_planets(self, galaxy, amount='random'):
		if amount == 'random':
			amount = random.randint(3, 8)
		for i in range(0, amount):
			galaxy.create_new_planet(self, self.name, len(self.planets))

	def serialize(self):
		dictionary = dict(self.__dict__)
		dictionary['planets'] = dict()
		del dictionary['galaxy']
		return dictionary
