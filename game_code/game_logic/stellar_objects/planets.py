"""
The Planet File. Contains any relevant code to the planets.
"""


planet_flags = {
    'anomoly': False
}


class TerrestrialBody:
    """
    The Terrestrial Body class. Classifies as the base for all large bodies in space.
    """
    def __init__(self, planet_id, name, flags, orbit_index, star_instance, galaxy, **kwargs):
        """
        Initialize the instance
        
        :param planet_id: The ID of the planet
        :param name: Name of the planet.
        :param flags: Any additional flags for any specific use.
        :param orbit_index: The order it will appear in lists.
        :param star_instance: Parent Star
        :param galaxy: Galaxy
        :param kwargs: Any kwargs used to set a specific value
        """
        self.galaxy = galaxy  # Reference to the galaxy object.
        self.name = name  # Name of the object (For game purposes)

        self.parent_star = star_instance  # Parent star
        self.ids = {
            'self': planet_id,  # ID of self

            'star': star_instance.ids['self']  # ID of parent star
        }
        self.flags = planet_flags.copy()  # Relevant flags for planet
        if flags is not None:
            self.flags.update(flags)

        self.orbit_index = orbit_index  # Distance (in planets starting from 0) from the star.
        self.orbital_distance = 1.4  # Radius from the center.
        self.eccentricity = 0

        self.planet_type = 'terrestrial'  # Type of planet
        self.file_path = '/path/to/file.png'  # Path to file (used in rendering)

        self.resources = {
            'total': 1999999999998,
            'water': {
                'amount': 999999999999,  # How many units are stored on the planet
                'availability': 1  # How easily mineable it is
            },
            'build_materials': {
                'amount': 999999999999,  # 999,999,999,999
                'availability': 1
            },
        }

        self.colonies = dict()  # A dict of {id's: instances} of planet objects.

        self.__dict__.update(kwargs)  # Update any kwargs

        star_instance.planets[self.ids['self']] = self  # Assign to parent planet

    def __repr__(self):
        """
        Easy debugger printing of the planet
        
        :return: A formatted string of the details necessary for debugging.
        """
        return "'Planet Name: {self_name}, ID: {self_id}, Type: {self_type}'\n".format(
            self_name=self.name,
            self_id=self.ids['self'],
            self_type=self.planet_type + "|" + self.file_path
        )

    def __getstate__(self):
        """
        Invoked whenever serializing self. Used to shed any issue with circularisation.
        
        :return dictionary: A dict of self, without pointers to parent object
        """
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        del dictionary['parent_star']
        return dictionary

    def apply_mining(self, mines):
        """
        Called by child colony, mines resources based on accessibility and returns an amount to the colony
        
        :param mines: How many mines are being used on the planet.
        :return mined_resources: The units mined from the planet.
        """
        mined_resources = dict()
        for resource, value in self.resources.items():
            pass  # TODO Impliment mining.
        return mined_resources
