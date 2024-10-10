import numpy as np
from tts.lib.parse_data import champ_names, champ_to_cost, trait_levels, champion_traits_matrix, champ_to_index, num_traits, num_champions, trait_to_index

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

