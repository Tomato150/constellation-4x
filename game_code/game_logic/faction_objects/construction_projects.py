"""
The Construction Project File. 
This file is used for containing all relevant code to the Construction Project,
but not any data, which is found at 'construction_constants.py'
"""

from game_code.game_data.constants import construction_constants
from utils import observers


construction_project_flags = {

}


class ConstructionProject:
    """
    The Construction Project Object. 
    This is the base class for a construction project, whether that be for a 
    colony or for a shipyard.    
    """
    def __init__(self, project_id, flags, project_building, project_runs,num_of_factories, colony_instance, galaxy,
                 **kwargs):
        """
        Initialize the construction project.
        
        :param project_id: The ID of the project.
        :param flags: Any additional flags
        :param project_building: What the building type is 
        :param project_runs: How many runs
        :param num_of_factories: How many factories are assigned
        :param colony_instance: Parent Colony
        :param galaxy: Galaxy
        :param kwargs: Any Kwargs for specific values
        """
        self.galaxy = galaxy  # A pointer to the galaxy object.
        self.parent_colony = colony_instance  # A pointer to parent object
        self.ids = {  # A dict containing all the ID's of objects in it's tree.
            'self': project_id,  # ID of self

            'star': colony_instance.ids['star'],  # ID of parent star
            'planet': colony_instance.ids['planet'],  # ID of parent planet

            'empire': colony_instance.ids['empire'],  # ID of parent empire
            'colony': colony_instance.ids['self']  # ID of parent colony
        }

        self.construction_changed = observers.Subject('construction_project_change')  # Construction Changed Subject
        self.flags = construction_project_flags.copy()  # Flags for construction project
        if flags is not None:
            self.flags.update(flags)

        self.project_building = project_building  # What you are building
        self.project_cost = construction_constants.building_costs[
            project_building]  # Individual resource cost per resource
        self.project_runs = project_runs  # How many copies are to be made.
        self.num_of_factories = {
            'total': num_of_factories,  # Total amount of factories to be used on the project
            'current': 0  # Currently working on the project.
        }

        self.currently_completed = {}  # A dictionary of resources currently used for the specific run
        for key in self.project_cost:
            self.currently_completed[key] = 0

        self.construction_per_tick = dict()  # How much of each resource is to be consumed per tick
        self.__set_construction_per_tick()
        self.assign_free_points()

        self.__dict__.update(kwargs)  # Update kwargs

        colony_instance.construction_projects[self.ids['self']] = self  # adding self to parent colony. Only strong
        #                                                                 reference to the object
        colony_instance.construction_project_created.notify(data={'construction_project': self})  # Notify of creation

    def __getstate__(self):
        """
        Invoked whenever serializing self. Used to shed any issue with circularisation.
        
        :return: dictionary: A dict of self, without pointers to parent object
        """
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        del dictionary['parent_colony']
        return dictionary

    def __del__(self):
        """
        Invoked whenever destroyed
        """
        print("Destructor Called")

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
            'num_of_factories': str(self.num_of_factories['current']) + '/' + str(self.num_of_factories['total']),
            'construction_per_tick': self.construction_per_tick['total'],
            'project_cost': self.project_cost['total'],
            'project_current': self.currently_completed['total']
        }

    def assign_free_points(self, amount=-1):
        wanted = self.num_of_factories['total'] - self.num_of_factories['current']
        if amount == -1:
            # Do if grabbing factories from within the construction project
            self.num_of_factories['current'] += self.parent_colony.get_free_factories(wanted)
        else:
            # Do if given factories from colony
            used = min(wanted, amount)
            self.num_of_factories['current'] = used
            return used

        self.__set_construction_per_tick()

    def __set_construction_per_tick(self):
        parent_empire = self.parent_colony.parent_empire

        total_cp_per_day = \
            self.num_of_factories['current'] * parent_empire.modifiers['building_modifiers']['build_points'] / 365

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

        # FIXME Error when resource is used up, but is still required, and when everything else is finished
        # construction wise. Points will not allocate, and eventually crash the game.

        # CP_allocated = Limiting
        if min_value == cp_allocated:
            self.currently_completed[material] += cp_allocated
            self.parent_colony.resource_storage[material] -= cp_allocated
            self.parent_colony.resource_storage['total'] -= cp_allocated
            return 0, True

        # Resource = Limiting
        elif min_value == colony_resource:
            self.currently_completed[material] += colony_resource
            self.parent_colony.resource_storage['total'] -= colony_resource
            self.parent_colony.resource_storage[material] = 0
            return cp_allocated - colony_resource, False

        # CP_to_finish = Limiting
        elif min_value == cp_to_finish:
            self.currently_completed[material] += cp_to_finish
            self.parent_colony.resource_storage[material] -= cp_to_finish
            self.parent_colony.resource_storage['total'] -= cp_to_finish
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
