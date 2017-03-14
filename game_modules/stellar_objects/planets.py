class TerrestrialBody:
	def __init__(self, planet_id, name, orbit_index, star_instance, galaxy, **kwargs):
		# Planet Location and General Information
		self.galaxy = galaxy
		self.name = name

		# Parents
		self.parent_star = star_instance

		self.ids = {
			'self': planet_id,

			'star': star_instance.ids['self']
		}

		self.orbit_index = orbit_index  # 0, 1, 2 ... n
		self.orbital_distance = 1.4  # Radius from the center.
		self.eccentricity = 0

		# Planet Type information
		self.planet_type = 'terrestrial'
		self.file_path = '/path/to/file.png'

		# Planet contents information
		self.colonies = {}  # A dict of {id's: instances} of planet objects.
		self.resources = {
			'water': {
				'amount': 999999999999,  # 999,999,999,999
				'availability': 1
			},
			'build_materials': {
				'amount': 999999999999,  # 999,999,999,999
				'availability': 1
			},
		}

		# **kwarg update
		self.__dict__.update(kwargs)

		star_instance.planets[self.ids['self']] = self

	def serialize(self):
		dictionary = dict(self.__dict__)
		dictionary['colonies'] = dict()
		del dictionary['galaxy']
		del dictionary['parent_star']
		return dictionary
