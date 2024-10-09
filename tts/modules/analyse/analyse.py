import numpy as np
from tts.lib.data import champions, traits


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


def convert_indices_to_names(valid_combos, champion_list):
    name_combos = []
    for combo in valid_combos:
        name_combos.append([champion_list[i]["name"] for i in combo])
    return name_combos


def count_active_traits(combination, trait_matrix, min_levels):
  """
  This function takes a combination (list of champion indices), and computes the number
  of active traits for that combination based on the trait matrix and minimum levels.
  """
  # Select the sub-matrix of the trait matrix corresponding to the selected champions
  selected_trait_matrix = trait_matrix[combination]

  # Sum across the selected champions to count trait occurrences
  trait_counts = selected_trait_matrix.sum(axis=0)

  # Check how many traits meet the minimum level requirements
  active_traits = np.sum(trait_counts >= min_levels)

  return active_traits

input_file = '../../data/7_champs.npy'
file = np.load(input_file, allow_pickle=True)