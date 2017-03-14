# TODO Create game loop structure and code
def update_return_values(return_values, new_values):
	if new_values is not None:
		for major_key in new_values:
			for minor_key in new_values[major_key]:
				return_values.update(new_values[major_key][minor_key])


def game_loop(galaxy):
	return_values = {
		'create': {
			'stars': {},
			'planets': {},
			'empires': {},
			'colonies': {},
			'construction_projects': {}
		},
		'update': {
			'stars': {},
			'planets': {},
			'empires': {},
			'colonies': {},
			'construction_projects': {}
		},
		'delete': {
			'stars': {},
			'planets': {},
			'empires': {},
			'colonies': {},
			'construction_projects': {}
		}
	}

	# Whole Game Events
	for empire in galaxy.world_objects['empires']:
		# Empire Wide Events
		for colony_id, colony in empire.colonies.items():
			# Colony Wide Events
			for construction_project_id, construction_project in colony.construction_projects.items():
				# Construction Project Events
				update_return_values(return_values, construction_project.construction_tick())

	return return_values
