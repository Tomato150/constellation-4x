from game_code.game_data.constants import construction_constants
from utils import observers


construction_project_flags = {

}


class ConstructionProject:
    def __init__(self, project_id, flags, project_building, project_runs, num_of_factories, colony_instance, galaxy,
                 **kwargs):
        self.galaxy = galaxy

        # Parents
        self.parent_colony = colony_instance
        self.ids = {
            'self': project_id,
            'star': colony_instance.ids['star'],
            'planet': colony_instance.ids['planet'],

            'empire': colony_instance.ids['empire'],
            'colony': colony_instance.ids['self']
        }

        # Flags and Subjects
        self.construction_changed = observers.Subject('construction_project_change')

        self.flags = construction_project_flags.copy()
        if flags is not None:
            self.flags.update(flags)

        # Project Info
        self.project_building = project_building  # What you are building
        self.project_cost = construction_constants.building_costs[
            project_building]  # Individual resource cost per resource
        self.project_runs = project_runs  # How many copies are to be made.
        self._num_of_factories = num_of_factories

        currently_completed = {}
        for key in self.project_cost:
            currently_completed[key] = 0

        self.currently_completed = currently_completed  # What and how much of a material has been completed.

        self.construction_per_tick = {}
        self._set_construction_per_tick()

        self.__dict__.update(kwargs)

        colony_instance.construction_projects[self.ids['self']] = self

        colony_instance.construction_project_created.notify(data={'construction_project': self})

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        del dictionary['parent_colony']
        return dictionary

    def __del__(self):
        print("Destructor Called")

    @property
    def num_of_factories(self):
        return self._num_of_factories

    @num_of_factories.setter
    def num_of_factories(self, value):
        if value != self._num_of_factories:
            self._num_of_factories = value
            self._set_construction_per_tick()

    def unhook_all(self):
        self.construction_changed.remove_all()

    @staticmethod
    def get_metadata_for_table():
        return [
            'project_building',
            'project_runs',
            'num_of_factories',
            'construction_per_tick',
            'project_cost',
            'project_current'
        ]

    def get_data_for_table(self):
        return {
            'project_building': self.project_building,
            'project_runs': self.project_runs,
            'num_of_factories': self.num_of_factories,
            'construction_per_tick': self.construction_per_tick['total'],
            'project_cost': self.project_cost['total'],
            'project_current': self.currently_completed['total']
        }

    def _set_construction_per_tick(self):
        parent_empire = self.parent_colony.parent_empire

        total_cp_per_day = self.num_of_factories * parent_empire.modifiers['building_modifiers']['build_points'] / 365

        for material, cost in self.project_cost.items():
            if material == 'total':
                self.construction_per_tick['total'] = total_cp_per_day
            else:
                self.construction_per_tick[material] = (cost * total_cp_per_day) / self.project_cost['total']

    def _assign_build_points(self, material, cp_allocated):
        cp_to_finish = self.project_cost[material] - self.currently_completed[material]
        colony_resource = self.parent_colony.resource_storage[material]

        min_value = min(cp_allocated, colony_resource, cp_to_finish)

        remainder_CP = 0
        available_for_extra = False

        # CP_allocated = Limiting
        if min_value == cp_allocated:
            self.currently_completed[material] += cp_allocated
            self.parent_colony.resource_storage[material] -= cp_allocated
            return 0, True

        # Resource = Limiting
        elif min_value == colony_resource:
            self.currently_completed[material] += colony_resource
            self.parent_colony.resource_storage[material] = 0
            return cp_allocated - colony_resource, False

        # CP_to_finish = Limiting
        elif min_value == cp_to_finish:
            self.currently_completed[material] += cp_to_finish
            self.parent_colony.resource_storage[material] -= cp_to_finish
            return cp_allocated - cp_to_finish, False

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
            if self.project_runs == 0:
                self.parent_colony.remove_construction_project_list.append(self.ids['self'])
            return True
        else:
            return False

    def _assign_proportional_points(self):
        # Establishes some default variables
        available_for_extra_CP = []
        total_remainder = 0.0

        # While it's possible to create a building with the initial values
        while True:
            # Cycle through materials, and assign them their build points
            for material in self.project_cost:
                if material != 'total':
                    # Grab the remainder, and if it's available for extra once build points are assigned
                    remaining_from_material, available_for_extra = self._assign_build_points(
                        material=material,
                        cp_allocated=self.construction_per_tick[material]
                    )

                    total_remainder += remaining_from_material

                    if available_for_extra:
                        available_for_extra_CP.append(material)

            # Apply available build, otherwise move to allocation of remainders
            if not self._check_for_built():
                break

        return total_remainder, available_for_extra_CP

    def _assign_even_points(self, total_remainder, available_for_extra_CP):
        # While there's a remainder.
        while total_remainder >= 0.0001:  # Due to rounding errors.
            new_available_for_extra_CP = []
            extra_cp = total_remainder / len(available_for_extra_CP)
            # Split evenly between all that need it, and allocate it.
            for material in available_for_extra_CP:
                remaining_from_material, available_for_extra = self._assign_build_points(
                    material=material,
                    cp_allocated=extra_cp
                )

                total_remainder += remaining_from_material - extra_cp
                if available_for_extra:
                    new_available_for_extra_CP.append(material)

            # Check to see if something's been built
            if self._check_for_built():
                # And if it has, make all available for rebuild
                available_for_extra_CP = list()
                for material in self.project_cost:
                    if material != 'total':
                        available_for_extra_CP.append(material)
            else:
                available_for_extra_CP = new_available_for_extra_CP

    def construction_tick(self):
        """
        Runs a construction tick for the specified game time delta
        
        :param game_time_dela: What percentage of one day has passed since the last tick.
        :return: Breaks out of the function call. Never a value returned
        """

        # Checks to see if the construction tick can take place, otherwise returns,
        if self.num_of_factories == 0:
            return
        for material in self.project_cost:
            if material != 'total':  # TODO Make this merged with the one below
                if self.parent_colony.resource_storage[material] != 0:
                    break
        else:
            return

        total_remainder, available_for_extra_CP = self._assign_proportional_points()

        self._assign_even_points(total_remainder, available_for_extra_CP)

        self.construction_changed.notify(data={'construction_project': self})
