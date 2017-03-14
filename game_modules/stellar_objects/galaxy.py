from game_modules.stellar_objects import stars, planets
from game_modules.faction_objects import empires, colonies, construction_project

from game_modules import utility_functions

import random
import math


class Galaxy:
	# Note; Don't think of this as just the stars, but everything inside the galaxy.
	def __init__(self):
		# Constants to change to fuck with the shape of the galaxy
		self.galaxy_creation_parameters = {
			'num_of_stars': 50000,
			'num_of_arms': 6,
			'arms_offset_max': 0.5,
			'rotation_factor': 3,
			'size_of_canvas': 6000,
			'x_y_rand_offset': 20,
			'galactic_center_cutoff': 0,
		}

		self.star_quadrants = {}

		# Dicts of {id's: instances} for stars and empires.
		self.world_objects = {
			'stars': {},
			'empires': {}
		}

		self.world_objects_id = {
			'stars': 0,
			'planets': 0,
			'empires': 0,
			'colonies': 0,
			'installations': 0,
			'construction_projects': 0,
			'fleets': 0,
			'ships': 0
		}

	def generate_galaxy(self):
		bounds = [int(self.galaxy_creation_parameters['size_of_canvas'] / 20 * -1), int(self.galaxy_creation_parameters['size_of_canvas'] / 20)]
		for x in range(bounds[0], bounds[1]):
			self.star_quadrants[str(x)] = {}
			for y in range(bounds[0], bounds[1]):
				self.star_quadrants[str(x)][str(y)] = {}
		arm_separation = (2 * math.pi) / self.galaxy_creation_parameters['num_of_arms']
		while True:

			# Get distance from galactic center
			distance = random.random() ** 2

			if not distance < self.galaxy_creation_parameters['galactic_center_cutoff']:

				# Get angle based on unit circle
				angle = random.random() * 2 * math.pi
				arm_offset = random.random() * self.galaxy_creation_parameters['arms_offset_max']
				arm_offset -= self.galaxy_creation_parameters['arms_offset_max'] / 2
				arm_offset *= (1 / distance)

				if self.world_objects_id['stars'] % 2 == 0 or self.world_objects_id['stars'] % 3 == 0:
					squared_arm_offset = arm_offset ** 2 + (random.uniform(-1, 1) / 5)
				else:
					squared_arm_offset = arm_offset ** 2
				if arm_offset < 0:
					squared_arm_offset *= -1
				arm_offset = squared_arm_offset

				rotation = distance * self.galaxy_creation_parameters['rotation_factor']

				angle = int((angle / arm_separation)) * arm_separation + arm_offset + rotation

				# Translate to cartesian coordinates
				star_x = int(math.cos(angle) * distance * (self.galaxy_creation_parameters['size_of_canvas'] / 50 * 49) / 2)
				star_y = int(math.sin(angle) * distance * (self.galaxy_creation_parameters['size_of_canvas'] / 50 * 49) / 2)

				# Random Offset
				if self.world_objects_id['stars'] % self.galaxy_creation_parameters['x_y_rand_offset'] == 0:
					offset_star_x = 20 * self.galaxy_creation_parameters['x_y_rand_offset'] * random.uniform(-1, 1)
					offset_star_y = 20 * self.galaxy_creation_parameters['x_y_rand_offset'] * random.uniform(-1, 1)
				else:
					offset_star_x = self.galaxy_creation_parameters['x_y_rand_offset'] * random.uniform(-1, 1)
					offset_star_y = self.galaxy_creation_parameters['x_y_rand_offset'] * random.uniform(-1, 1)

				star_x += offset_star_x
				star_y += offset_star_y

				# Ensuring that no bounds are overstepped from the random element
				half_canvas = self.galaxy_creation_parameters['size_of_canvas'] / 2
				if star_x < half_canvas * -1:
					star_x = half_canvas * -1 + 1
				elif star_x > half_canvas:
					star_x = half_canvas - 1

				if star_y < half_canvas * -1:
					star_y = half_canvas * -1 + 1
				elif star_y > half_canvas:
					star_y = half_canvas - 1

				if self.world_objects_id['stars'] == 0:
					star_x = 0
					star_y = 0

				star_x = int(star_x)
				star_y = int(star_y)

				quadrant_x = int(star_x / 10)
				quadrant_y = int(star_y / 10)
				star_collision = False

				for star_id, star in self.star_quadrants[str(quadrant_x)][str(quadrant_y)].items():
					coordinates = star.coordinates
					if -1 <= coordinates[0] - star_x <= 1 and -1 <= coordinates[1] - star_y <= 1:
						star_collision = True

				if -200 <= quadrant_x < 200 and -200 <= quadrant_y < 200 and not star_collision:

					for quad_x in range(quadrant_x - 1, quadrant_x + 2):
						if quad_x in range(bounds[0], bounds[1]) and not star_collision:

							for quad_y in range(quadrant_y - 1, quadrant_y + 2):
								if quad_y in range(bounds[0], bounds[1]) and not star_collision:

									for star_id, star in self.star_quadrants[str(quad_x)][str(quad_y)].items():
										coordinates = star.coordinates
										if -1 <= coordinates[0] - star_x <= 1 and -1 <= coordinates[1] - star_y <= 1:
											star_collision = True

								else:
									continue

						else:
							continue

				# Appending to right dictionary
				if not star_collision:
					if star_x == 0 and star_y == 0:
						star_object = stars.Star(str(self.world_objects_id['stars']), star_x, star_y, self, name='Sol')
					else:
						star_object = stars.Star(str(self.world_objects_id['stars']), star_x, star_y, self)
					self.star_quadrants[str(quadrant_x)][str(quadrant_y)][str(self.world_objects_id['stars'])] = star_object
					self.world_objects['stars'][str(self.world_objects_id['stars'])] = star_object

					self.world_objects_id['stars'] += 1
					if self.world_objects_id['stars'] % 10000 == 0:
						print(self.world_objects_id['stars'])

					if self.world_objects_id['stars'] == self.galaxy_creation_parameters['num_of_stars']:
						break
		print('Done: Galaxy Generation')
		print('Count: ' + str(self.world_objects_id['stars']))

	# All will map the instance to the desired object/dict.
	def create_new_planet(self, star_instance, star_name, orbit_index):
		planet_name = star_name + ' ' + utility_functions.toRoman(orbit_index + 1)
		planet = planets.TerrestrialBody(str(self.world_objects_id['planets']), planet_name, orbit_index, star_instance, self)
		self.world_objects_id['planets'] += 1
		return planet

	def create_new_empire(self, name):
		empire = empires.Empire(str(self.world_objects_id['empires']), name, self)
		self.world_objects_id['empires'] += 1
		self.world_objects['empires'][empire.ids['self']] = empire
		return empire

	def create_new_colony(self, name, planet_instance, empire_instance):
		colony = colonies.Colony(str(self.world_objects_id['colonies']), name, planet_instance, empire_instance, self)
		self.world_objects_id['colonies'] += 1
		return colony

	def create_new_construction_project(self, project_building, project_runs, num_of_factories, colony_instance):
		construction_project = construction_project.ConstructionProject(str(self.world_objects_id['construction_projects']), project_building, project_runs, num_of_factories, colony_instance, self)
		self.world_objects_id['construction_projects'] += 1
		return construction_project

	def get_object_by_id(self, object_type, object_ids, is_self=False):
		if is_self:
			if object_type == 'star':
				return self.world_objects['stars'][object_ids['self']]
			elif object_type == 'planet':
				return self.world_objects['stars'][object_ids['star']].planets[object_ids['self']]
			elif object_type == 'empire':
				return self.world_objects['empires'][object_ids['self']]
			elif object_type == 'colony':
				return self.world_objects['empires'][object_ids['empire']].colonies[object_ids['self']]
			elif object_type == 'construction_project':
				return self.world_objects['empires'][object_ids['empire']].colonies[object_ids['self']].construction_projects[object_ids['self']]
		elif not is_self:
			if object_type == 'star':
				return self.world_objects['stars'][object_ids['star']]
			elif object_type == 'planet':
				return self.world_objects['stars'][object_ids['star']].planets[object_ids['planet']]
			elif object_type == 'empire':
				return self.world_objects['empires'][object_ids['empire']]
			elif object_type == 'colony':
				return self.world_objects['empires'][object_ids['empire']].colonies[object_ids['colony']]

	def get_objects_by_category(self, object_type):
		objects = {}
		if object_type in ['stars', 'planets']:
			for star_id, star_instance in self.world_objects['stars'].items():
				if object_type == 'planets':
					for planet_id, planet_instance in star_instance.planets.items():
						objects[planet_id] = planet_instance
				elif object_type == 'stars':
					objects[star_id] = star_instance

		elif object_type in ['empires', 'colonies', 'construction_projects']:
			for empire_id, empire_instance in self.world_objects['empires'].items():
				if object_type in ['colonies', 'construction_projects']:
					for colony_id, colony_instance in empire_instance.colonies.items():
						if object_type == 'construction_projects':
							for construction_project_id, construction_project_instance in colony_instance.construction_projects.items():
								objects[construction_project_id] = construction_project_instance
						elif object_type == 'colonies':
							objects[colony_id] = colony_instance
				elif object_type == 'empires':
					objects[empire_id] = empire_instance

		return objects

	# GETTERS
	def get_galaxy_creation_parameters(self, objects='all'):
		if type(objects) == str:
			if objects.lower() == 'all':
				return self.galaxy_creation_parameters
			else:
				return self.galaxy_creation_parameters[objects]
		else:
			return_dict = {}
			for object_wanted in objects:
				return_dict[object_wanted] = self.galaxy_creation_parameters[object_wanted]
			return return_dict
