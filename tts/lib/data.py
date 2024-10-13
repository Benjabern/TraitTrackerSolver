import json
import numpy as np
import os
import tts
def load_data(set):
  libpath = os.path.abspath(tts.lib.__file__).rstrip('__init__.py')
  set_data = json.load(open(libpath+set))
  champions = set_data["champions"]
  traits = set_data["traits"]
  champ_names = [champ["name"] for champ in champions]
  trait_to_index = {trait["name"]: idx for idx, trait in enumerate(traits)}
  champ_to_index = {champ: idx for idx, champ in enumerate(champ_names)}  # Map champ names to indices
  champ_to_cost = {champ["name"]: champ["cost"] for champ in champions}  # Map champ names to costs
  trait_levels = np.array([trait["levels"][0] for trait in traits])
  num_champions = len(champions)
  num_traits = len(traits)
  champion_traits_matrix = np.zeros((num_champions, num_traits), dtype=np.int32)

  for i, champ in enumerate(champions):
    for trait in champ["traits"]:
      if trait in trait_to_index:
        champion_traits_matrix[i, trait_to_index[trait]] = 1
  return champions, traits, champ_names, champ_to_index, champ_to_cost, champion_traits_matrix, trait_levels, trait_to_index


# champions = [
#   {"name": "Briar", "cost": 5, "traits": ["Eldritch", "Ravenous", "Shapeshifter"]},
#   {"name": "Camille", "cost": 5, "traits": ["Chrono", "Multistriker"]},
#   {"name": "Diana", "cost": 5, "traits": ["Frost", "Bastion"]},
#   {"name": "Milio", "cost": 5, "traits": ["Faerie", "Scholar"]},
#   {"name": "Morgana", "cost": 5, "traits": ["Witchcraft", "Preserver", "Bat Queen"]},
#   {"name": "Norra", "cost": 5, "traits": ["Portal", "Mage", "Best Friends"]},
#   {"name": "Smolder", "cost": 5, "traits": ["Dragon", "Blaster"]},
#   {"name": "Xerath", "cost": 5, "traits": ["Arcana", "Ascendant"]},
#   {"name": "Fiora", "cost": 4, "traits": ["Witchcraft", "Warrior"]},
#   {"name": "Gwen", "cost": 4, "traits": ["Sugarcraft", "Warrior"]},
#   {"name": "Kalista", "cost": 4, "traits": ["Faerie", "Multistriker"]},
#   {"name": "Karma", "cost": 4, "traits": ["Chrono", "Incantor"]},
#   {"name": "Nami", "cost": 4, "traits": ["Eldritch", "Mage"]},
#   {"name": "Nasus", "cost": 4, "traits": ["Pyro", "Shapeshifter"]},
#   {"name": "Olaf", "cost": 4, "traits": ["Frost", "Hunter"]},
#   {"name": "Rakan", "cost": 4, "traits": ["Faerie", "Preserver"]},
#   {"name": "Ryze", "cost": 4, "traits": ["Portal", "Incantor"]},
#   {"name": "Tahm", "cost": 4, "traits": ["Arcana", "Vanguard"]},
#   {"name": "Taric", "cost": 4, "traits": ["Portal", "Bastion"]},
#   {"name": "Varus", "cost": 4, "traits": ["Pyro", "Blaster"]},
#   {"name": "Bard", "cost": 3, "traits": ["Sugarcraft", "Preserver", "Scholar"]},
#   {"name": "Ezreal", "cost": 3, "traits": ["Portal", "Blaster"]},
#   {"name": "Hecarim", "cost": 3, "traits": ["Arcana", "Bastion", "Multistriker"]},
#   {"name": "Hwei", "cost": 3, "traits": ["Frost", "Blaster"]},
#   {"name": "Jinx", "cost": 3, "traits": ["Sugarcraft", "Hunter"]},
#   {"name": "Katarina", "cost": 3, "traits": ["Faerie", "Warrior"]},
#   {"name": "Mordekaiser", "cost": 3, "traits": ["Eldritch", "Vanguard"]},
#   {"name": "Neeko", "cost": 3, "traits": ["Witchcraft", "Shapeshifter"]},
#   {"name": "Shen", "cost": 3, "traits": ["Pyro", "Bastion"]},
#   {"name": "Swain", "cost": 3, "traits": ["Frost", "Shapeshifter"]},
#   {"name": "Veigar", "cost": 3, "traits": ["Honeymancy", "Mage"]},
#   {"name": "Vex", "cost": 3, "traits": ["Chrono", "Mage"]},
#   {"name": "Wukong", "cost": 3, "traits": ["Druid"]},
#   {"name": "Ahri", "cost": 2, "traits": ["Arcana", "Scholar"]},
#   {"name": "Akali", "cost": 2, "traits": ["Pyro", "Warrior", "Multistriker"]},
#   {"name": "Cassiopeia", "cost": 2, "traits": ["Witchcraft", "Incantor"]},
#   {"name": "Galio", "cost": 2, "traits": ["Portal", "Vanguard", "Mage"]},
#   {"name": "Kassadin", "cost": 2, "traits": ["Portal", "Multistriker"]},
#   {"name": "Kog'Maw", "cost": 2, "traits": ["Honeymancy", "Hunter"]},
#   {"name": "Nilah", "cost": 2, "traits": ["Eldritch", "Warrior"]},
#   {"name": "Nunu", "cost": 2, "traits": ["Honeymancy", "Bastion"]},
#   {"name": "Rumble", "cost": 2, "traits": ["Sugarcraft", "Vanguard", "Blaster"]},
#   {"name": "Shyvana", "cost": 2, "traits": ["Dragon", "Shapeshifter"]},
#   {"name": "Syndra", "cost": 2, "traits": ["Eldritch", "Incantor"]},
#   {"name": "Tristana", "cost": 2, "traits": ["Faerie", "Blaster"]},
#   {"name": "Zilean", "cost": 2, "traits": ["Frost", "Chrono", "Preserver"]},
#   {"name": "Ashe", "cost": 1, "traits": ["Eldritch", "Multistriker"]},
#   {"name": "Blitzcrank", "cost": 1, "traits": ["Honeymancy", "Vanguard"]},
#   {"name": "Elise", "cost": 1, "traits": ["Eldritch", "Shapeshifter"]},
#   {"name": "Jax", "cost": 1, "traits": ["Chrono", "Multistriker"]},
#   {"name": "Jayce", "cost": 1, "traits": ["Portal", "Shapeshifter"]},
#   {"name": "Lillia", "cost": 1, "traits": ["Faerie", "Bastion"]},
#   {"name": "Nomsy", "cost": 1, "traits": ["Dragon", "Hunter"]},
#   {"name": "Poppy", "cost": 1, "traits": ["Witchcraft", "Bastion"]},
#   {"name": "Seraphine", "cost": 1, "traits": ["Faerie", "Mage"]},
#   {"name": "Soraka", "cost": 1, "traits": ["Sugarcraft", "Mage"]},
#   {"name": "Twitch", "cost": 1, "traits": ["Frost", "Hunter"]},
#   {"name": "Warwick", "cost": 1, "traits": ["Frost", "Vanguard"]},
#   {"name": "Ziggs", "cost": 1, "traits": ["Honeymancy", "Incantor"]},
#   {"name": "Zoe", "cost": 1, "traits": ["Portal", "Witchcraft", "Scholar"]}
# ]
# traits = [
#   {"name": "Arcana", "levels": [2, 3, 4, 5]},
#   {"name": "Chrono", "levels": [2, 4, 6]},
#   {"name": "Dragon", "levels": [2, 3]},
#   {"name": "Druid", "levels": [1]},
#   {"name": "Eldritch", "levels": [3, 5, 7, 10]},
#   {"name": "Faerie", "levels": [3, 5, 7, 9]},
#   {"name": "Frost", "levels": [3, 5, 7, 9]},
#   {"name": "Honeymancy", "levels": [3, 5, 7]},
#   {"name": "Portal", "levels": [3, 6, 8, 10]},
#   {"name": "Pyro", "levels": [2, 3, 4, 5]},
#   {"name": "Ravenous", "levels": [1]},
#   {"name": "Sugarcraft", "levels": [2, 4, 6]},
#   {"name": "Witchcraft", "levels": [2, 4, 6, 8]},
#   {"name": "Ascendant", "levels": [1]},
#   {"name": "Bastion", "levels": [2, 4, 6, 8]},
#   {"name": "Bat Queen", "levels": [1]},
#   {"name": "Best Friends", "levels": [1]},
#   {"name": "Blaster", "levels": [2, 4, 6]},
#   {"name": "Hunter", "levels": [2, 4, 6]},
#   {"name": "Incantor", "levels": [2, 4]},
#   {"name": "Mage", "levels": [3, 5, 7, 9]},
#   {"name": "Multistriker", "levels": [3, 5, 7]},
#   {"name": "Preserver", "levels": [2, 3, 4, 5]},
#   {"name": "Scholar", "levels": [2, 4, 6]},
#   {"name": "Shapeshifter", "levels": [2, 4, 6, 8]},
#   {"name": "Vanguard", "levels": [2, 4, 6]},
#   {"name": "Warrior", "levels": [2, 4, 6]}
# ]