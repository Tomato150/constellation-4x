from game_data.constants import construction_constants


class ConstructionProject:
	def __init__(self, project_id, project_building, project_runs, num_of_factories, colony_instance, galaxy_instance, **kwargs):
		# Parents
		self.galaxy = galaxy_instance
		self.parent_colony = colony_instance


		self.ids = {
			'self': project_id,
			'star': colony_instance.parent_ids['star'],
			'planet': colony_instance.parent_ids['planet'],

			'empire': colony_instance.parent_ids['empire'],
			'colony': colony_instance.id
		}

		# Project Info
		self.project_building = project_building  # What you are building
		self.project_cost = construction_constants.building_costs[project_building]  # Individual resource cost per resource
		self.project_runs = project_runs  # How many copies are to be made.
		self.num_of_factories = num_of_factories

		currently_completed = {}
		for key in self.project_cost:
			currently_completed[key] = 0

		self.currently_completed = currently_completed  # What and how much of a material has been completed.

		self.construction_per_tick = {}
		self.set_construction_per_tick()

		self.__dict__.update(kwargs)

		colony_instance.construction_projects[self.ids['self']] = self

	def _assign_build_points(self, material, cp_allocated):
		cp_to_finish = self.project_cost[material] - self.currently_completed[material]
		colony_resource = self.parent_colony.resource_storage[material]

		remainder_CP = 0
		available_for_extra = False

		# CP_allocated = Limiting
		if colony_resource > cp_allocated and cp_to_finish > cp_allocated:
			self.currently_completed[material] += cp_allocated
			self.parent_colony.resource_storage[material] -= cp_allocated
			available_for_extra = True

		# Resource = Limiting
		elif cp_allocated > colony_resource and cp_to_finish > colony_resource:
			self.currently_completed[material] += colony_resource
			self.parent_colony.resource_storage[material] = 0
			remainder_CP += cp_allocated - colony_resource

		# CP_to_finish = Limiting
		elif cp_allocated >= cp_to_finish and colony_resource >= cp_to_finish:
			self.currently_completed[material] += cp_to_finish
			self.parent_colony.resource_storage[material] -= cp_to_finish
			remainder_CP += cp_allocated - cp_to_finish

		return remainder_CP, available_for_extra

	def _check_for_built(self):
		self.currently_completed['total'] = 0
		for key, value in self.currently_completed.items():
			if key != 'total':
				self.currently_completed['total'] += value

		if self.project_cost == self.currently_completed:
			for key in self.currently_completed:
				self.currently_completed[key] = 0
			self.project_runs -= 1
			self.parent_colony.add_buildings(self.project_building)
			return True
		else:
			return False

	def set_construction_per_tick(self):
		construction_per_tick = {}

		total_CP = self.num_of_factories * self.parent_colony.parent_empire.modifiers['building_modifiers']['build_points'] / 365
		for material, cost in self.project_cost.items():
			if material != 'total':
				self.currently_completed[material] = (cost * total_CP) / self.project_cost['total']

		self.construction_per_tick = construction_per_tick

	def construction_tick(self):
		self.set_construction_per_tick()

		colony_has_resources = False
		for material in self.project_cost:
			if self.parent_colony.resource_storage[material] != 0:
				colony_has_resources = True
		if not colony_has_resources:
			return None

		available_for_extra_CP = []
		remainder = 0

		while True:
			for material in self.project_cost:
				if material != 'total':
					remaining, extra = self._assign_build_points(material, self.construction_per_tick[material])
					remainder += remaining
					if extra:
						available_for_extra_CP.append(material)
			if not self._check_for_built():
				break

		while remainder >= 0.0001:  # Due to rounding errors.
			remainder_CP = remainder
			new_available_for_extra_CP = []
			for material in available_for_extra_CP:
				extra_cp = remainder_CP / len(available_for_extra_CP)
				remaining, extra = self._assign_build_points(material, extra_cp)
				remainder = remainder - extra_cp + remaining
				if extra:
					new_available_for_extra_CP.append(material)
			available_for_extra_CP = new_available_for_extra_CP

		return {
			'update': {
				'colonies': {self.ids['colony']: self.parent_colony}
			}
		}

	def serialize(self):
		dictionary = dict(self.__dict__)
		del dictionary['galaxy']
		del dictionary['parent_colony']
		return dictionary
