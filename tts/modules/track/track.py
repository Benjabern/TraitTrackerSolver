import numpy as np
import tts.data
import os
from tts.lib.data import load_data
from tts.modules.compute.parse_binary import load_combinations_from_file

path = os.path.abspath(tts.data.__file__).rstrip('__init__.py')



def convert_indices_to_names(valid_combos, champion_list):
    name_combos = []
    for combo in valid_combos:
        name_combos.append([champion_list[i]["name"] for i in combo])
    return name_combos


def find_top_combinations(champion_names, all_combinations, max_champ_cost, max_comb_size, champ_to_index, champ_to_cost, champ_names, top_n=5
                                                    ):
    matched_combinations = []
    # Convert the input list of champion names to indices
    input_indices = set([champ_to_index[champ] for champ in champion_names if champ in champ_to_index])

    # Iterate over all combinations
    for comb in all_combinations:
        # Filter based on maximum comp size
        if len(comb) > max_comb_size:
            continue

        # Check if any champion in the combination exceeds the max cost
        if any(champ_to_cost[champ_names[i]] > max_champ_cost for i in comb):
            continue
        # Convert the combination to a set of indices
        comb_set = set(comb)
        # Find the intersection of input_indices and the combination
        matches = comb_set & input_indices
        match_count = len(matches)

        if match_count > 0:
            # Calculate the percentage of the combination that matches the input champs
            match_percentage = match_count / len(comb_set)

            # Find the missing champions
            missing_champs = comb_set - input_indices

            # Calculate the total cost of the missing champions
            missing_cost = sum([champ_to_cost[champ_names[i]] for i in missing_champs])

            # Store the combination, match percentage, and missing cost
            matched_combinations.append((comb, match_percentage, missing_cost, missing_champs))

    # Sort the combinations by match percentage (descending) and by missing cost (ascending)
    matched_combinations.sort(key=lambda x: (-x[1], x[2]))

    # Return the top N combinations
    return matched_combinations[:top_n]


def solve_comp(input_champs, file, mc, cs, set):
    champions, traits, champ_names, champ_to_index, champ_to_cost, champion_traits_matrix, trait_levels, trait_to_index = load_data(set)
    input_champs = [champ.capitalize() for champ in input_champs]
    file = path+file
    comps = load_combinations_from_file(file)
    top_combinations = find_top_combinations(input_champs, comps, mc, cs, champ_to_index, champ_to_cost, champ_names, top_n=5)
    out=[]
    for comb, match_percentage, missing_cost, missing_champs in top_combinations:
        champ_names_comb = [champ_names[i] for i in comb]
        missing_champs_name = [champ_names[i] for i in missing_champs]
        row = [f"Comp: {', '.join(champ_names_comb)}", f"Match: {match_percentage:.1%}", f"Gold needed: {missing_cost}", f"buy: {', '.join(missing_champs_name)}"]
        out.append(row)
    for row in out:
      print("{: <60} {: <14} {: <16} {: <7}".format(*row))
