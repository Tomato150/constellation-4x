class TerrestrialBody:
    def __init__(self, planet_id, name, flags, orbit_index, star_instance, galaxy, **kwargs):
        # Planet Location and General Information
        self.galaxy = galaxy
        self.name = name

        # Parents
        self.parent_star = star_instance
        self.ids = {
            'self': planet_id,

            'star': star_instance.ids['self']
        }
        self.flags = dict() if flags is None else flags

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

    def __str__(self):
        return "Planet name: " + self.name + ", ID: " + self.ids['self']

    def __repr__(self):
        return "'Planet Name: {self_name}, ID: {self_id}, Type: {self_type}'".format(
            self_name=self.name,
            self_id=self.ids['self'],
            self_type=self.planet_type + " " + self.file_path
        )

    def __getstate__(self):
        dictionary = self.__dict__.copy()
        del dictionary['galaxy']
        del dictionary['parent_star']
        return dictionary
