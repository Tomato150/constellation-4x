class Colony:
	def __init__(self, colony_id, name, planet_instance, empire_instance, galaxy, **kwargs):
		# Colony Location and General information
		self.galaxy = galaxy
		self.name = name

		# Parents
		self.parent_empire = empire_instance
		self.parent_planet = planet_instance
		self.ids = {
			'self': colony_id,

			'star': planet_instance.ids['star'],
			'planet': planet_instance.ids['self'],

			'empire': empire_instance.ids['self']
		}

		# Colony Type information
		self.colony_type = 'mixed'  # Military, Mixed, Civilian

		# Colony buildings information
		self.buildings = {
			# Quantity buildings (Can keep expanding more facilities)
			'mines': 100,
			'factories': 100,
		}
		self.installations = {
			# The are buildings that have instances attached with special and unique stats for each building.
			# 'name': id
		}

		self.construction_projects = {}  # A dict of {id's: instance} of all construction projects assigned to the colony.

		# Colony Storage
		self.resource_storage = {
			'water': 999999999,
			'building_materials': 999999999999
		}

		self.__dict__.update(kwargs)

		empire_instance.colonies[self.ids['self']] = self
		planet_instance.colonies[self.ids['self']] = self

	def update_construction(self, galaxy, empire):
		for construction_project in self.construction_projects:
			galaxy.construction_projects[construction_project].tick_construction(empire, self)

	# SETTERS
	def add_buildings(self, building):
		if type(building) == str:
			self.buildings[building] += 1
		else:
			self.galaxy.add_objects({'installations': building})
			self.installations[building.name] = building.id

	def serialize(self):
		dictionary = dict(self.__dict__)
		dictionary['construction_projects'] = dict()
		dictionary['installations'] = dict()
		del dictionary['galaxy']
		return dictionary


class Installation:
	def __init__(self, name, installation_id, galaxy):
		# General information and identification of the installation.
		self.galaxy = galaxy
		self.name = name
		self.id = installation_id

		self.stats = {}

	def serialize(self):
		dictionary = dict(self.__dict__)
		del dictionary['galaxy']
		del dictionary['parent_empire']
		del dictionary['parent_planet']
		return dictionary
