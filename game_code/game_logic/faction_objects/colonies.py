"""
The colonies File

A file containing any relevant information about the colony object.
"""

from utils import observers
import collections


colony_flags = {  # Any relevant flags for a colony instance.
    'capital': False
}


class Colony:
    def __init__(self, colony_id, name, flags, planet_instance, empire_instance, galaxy, **kwargs):
        """
        Initialize the colony instance
        
        :param colony_id: The ID of the colony
        :param name: Name of the colony
        :param flags: Any additional flags for any specific use.
        :param planet_instance: Parent Planet
        :param empire_instance: Parent Empire
        :param galaxy: Galaxy
        :param kwargs: Any Kwargs used to assign specific values
        """
        self.galaxy = galaxy  # Reference to the galaxy object
        self.name = name  # Name of the object (For game purposes)

        self.parent_empire = empire_instance  # Parent Empire
        self.parent_planet = planet_instance  # Parent Planet
        self.ids = {
            'self': colony_id,  # ID of self

            'star': planet_instance.ids['star'],  # ID of parent star
            'planet': planet_instance.ids['self'],  # ID of parent planet

            'empire': empire_instance.ids['self']  # ID of parent empire
        }

        self.construction_project_created = observers.Subject('construction_project_created')  # Deleted Con. subject
        self.flags = colony_flags.copy()  # Relevant flags for colonies
        if flags is not None:
            self.flags.update(flags)

        self.buildings = {  # A dict of which buildings are present on the colony
            'mines': 100,
            'factories': {
                'total': 100,  # For factories, there's total on the colony, and the amount not being used by a project
                'free': 100
            }
        }

        self.resource_storage = {  # A dict of the storage of minerals on the planet
            'total': 1999999998,
            'water': 999999999,
            'building_materials': 999999999
        }

        self.construction_projects = collections.OrderedDict()  # Construction dict. Ordered to maintain priority
        self.construction_projects_updates = dict()
        self.remove_construction_project_list = list()

        self.__dict__.update(kwargs)  # Update any kwargs

        if self.flags['capital']:  # Assign to value on empire. Strong ref
            empire_instance.colonies['capital'] = self
            empire_instance.colonies_updates['capital'] = False
        else:
            empire_instance.colonies[self.ids['self']] = self
            empire_instance.colonies_updates[self.ids['self']] = False

        planet_instance.colonies[self.ids['self']] = self  # Assign to planet. Strong ref

    def __getstate__(self):
        """
        Invoked whenever serializing self. Used to shed any issue with circularisation.
        
        :return dictionary: A dict of self, without pointers to parent object
        """
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        del dictionary['parent_empire']
        del dictionary['parent_planet']
        return dictionary

    def get_update_status(self):
        # If there is stuff to mine
        if self.buildings['mines'] and self.parent_planet.resources['total']:
            return True
        # If there is construction projects that can have work done on them
        elif self.construction_projects and self.resource_storage['total']:
            return True
        return False

    def update(self):
        """
        The update method for the colony.
        """
        if self.buildings['mines'] and self.parent_planet.resources['total'] != 0:
            self.mine_resources()

        for con_project_id, con_project_update in self.construction_projects_updates.items():
            if con_project_update:
                self.construction_projects[con_project_id].update()

    def mine_resources(self):
        """
        Get and apply resource additions from planet.
        """
        resources = self.parent_planet.apply_mining(self.buildings['mines'])
        for resource, amount in resources:
            self.resource_storage['total'] += amount
            self.resource_storage[resources] += amount

    def unhook_all(self):
        """
        Unhooks any observer from self, and from all children.
        """
        self.construction_project_created.remove_all()
        for construction_project in self.construction_projects.values():
            construction_project.unhook_all()

    def delete_construction_projects(self):
        """
        delete any finished construction projects
        """
        for construction_project in self.remove_construction_project_list:
            construction_project = self.construction_projects[construction_project]
            self.buildings['factories']['free'] += construction_project.num_of_factories['current']
            del self.construction_projects[construction_project]
        self.remove_construction_project_list = list()

        while self.buildings['factories']['free'] > 0 and self.construction_projects:
            for construction_project in self.construction_projects.values():
                construction_project.construction_component.assign_free_factories(self.buildings['factories']['free'])
                #  construction_project.get_free_factoires()

    # SETTERS
    def add_buildings(self, building):
        self.buildings[building] += 1
