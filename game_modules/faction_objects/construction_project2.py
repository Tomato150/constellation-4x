from game_data.constants import construction_constants


class ConstructionProject:
	def __init__(self, project_id, project_building, project_runs, num_of_factories, colony_instance, galaxy, **kwargs):
		# Parents
		self.galaxy = galaxy
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

	def _assign_build_points(self, material, CP_allocated):
		CP_to_finish = self.project_cost[material] - self.currently_completed[material]
		colony_resource = self.parent_colony.resource_storage[material]

		remainder_CP = 0
		available_for_extra = False

		# CP_allocated = Limiting
		if colony_resource > CP_allocated and CP_to_finish > CP_allocated:
			self.currently_completed[material] += CP_allocated
			self.parent_colony.resource_storage[material] -= CP_allocated
			available_for_extra = True

		# Resource = Limiting
		elif CP_allocated > colony_resource and CP_to_finish > colony_resource:
			self.currently_completed[material] += colony_resource
			self.parent_colony.resource_storage[material] = 0
			remainder_CP += CP_allocated - colony_resource

		# CP_to_finish = Limiting
		elif CP_allocated >= CP_to_finish and colony_resource >= CP_to_finish:
			self.currently_completed[material] += CP_to_finish
			self.parent_colony.resource_storage[material] -= CP_to_finish
			remainder_CP += CP_allocated - CP_to_finish

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

		available_for_extra_CP = []
		remainder = 0

		while True:
			for material in self.project_cost:
				if material != 'total':
					remainding, extra = self._assign_build_points(material, self.construction_per_tick[material])
					remainder += remainding
					if extra:
						available_for_extra_CP.append(material)
			if not self._check_for_built():
				break

		while True:
			if remainder <= 0.0001:
				break
			remainder_CP = remainder
			for material in available_for_extra_CP:
				remainding, extra = self._assign_build_points(material, remainder_CP/len(available_for_extra_CP))


