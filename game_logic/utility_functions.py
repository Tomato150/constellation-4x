from game_data.constants import general_constants

import random
import roman


def name_creator(mini, maxi, syl):
	name = ""
	for i in range(0, syl):
		name = name + random.choice(general_constants.CONSONANTS)
		for j in range(1, random.randint(mini, maxi)):
			if name[i-1] in general_constants.CONSONANTS:
				name = name + random.choice(general_constants.VOWELS)
			else:
				name = name + random.choice(general_constants.CONSONANTS)
	return name.capitalize()


def toRoman(number):
	return roman.toRoman(number)
