"""
The Construction Project File. 
This file is used for containing all relevant code to the Construction Project,
but not any data, which is found at 'construction_constants.py'
"""
from utils import observers
from game_code.game_logic.components import construction_component


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

        self.construction_changed = observers.Subject('construction_project_change')

        self.construction_component = construction_component.ConstructionComponent(  # Construction Component loading.
            parent=self,
            parent_colony=self.parent_colony,
            construction_changed_subject=self.construction_changed,
            project_building=project_building,
            project_runs=project_runs,
            num_of_factories=num_of_factories
        )

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
        return self.construction_component.get_data_for_table()

    def update(self):
        self.construction_component.construction_tick()
