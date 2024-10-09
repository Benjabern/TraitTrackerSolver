import numpy as np
from tts.lib.data import champions, traits

champ_names = [champ["name"] for champ in champions]
trait_to_index = {trait["name"]: idx for idx, trait in enumerate(traits)}
champ_to_index = {champ: idx for idx, champ in enumerate(champ_names)}  # Map champ names to indices
champ_to_cost = {champ["name"]: champ["cost"] for champ in champions}  # Map champ names to costs


num_champions = len(champions)
num_traits = len(traits)
champion_traits_matrix = np.zeros((num_champions, num_traits), dtype=np.int32)

for i, champ in enumerate(champions):
    for trait in champ["traits"]:
        if trait in trait_to_index:
            champion_traits_matrix[i, trait_to_index[trait]] = 1

trait_levels = np.array([trait["levels"][0] for trait in traits])

def convert_indices_to_names(valid_combos, champion_list):
    name_combos = []
    for combo in valid_combos:
        name_combos.append([champion_list[i]["name"] for i in combo])
    return name_combos


def find_top_combinations(champion_names, all_combinations, trait_matrix, min_levels, max_champ_cost, max_comb_size, top_n=5
                                                    ):
    """
    This function takes a list of champion names, searches for combinations of champions
    that match the highest percentage of champions in each combination, and returns the top N arrays
    with the highest percentage of matches, sorted by the total cost of the champions in the combination that are not in the input.

    Parameters:
    - champion_names: List of champion names as input.
    - all_combinations: List of combinations (as arrays of champion indices).
    - trait_matrix: Matrix with trait information (not directly used here).
    - min_levels: Minimum levels for traits (not directly used here).
    - top_n: Number of top combinations to return.
    - max_champ_cost: Maximum allowed cost of any champion in the combination.
    - max_comb_size: Maximum allowed number of champions in the combination.
    """
    matched_combinations = []
    # Convert the input list of champion names to indices
    input_indices = set([champ_to_index[champ] for champ in champion_names if champ in champ_to_index])

    # Iterate over all combinations
    for comb in all_combinations:
        # Filter based on maximum combination size
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

            # Find the missing champions (those in the combination but not in the input)
            missing_champs = comb_set - input_indices

            # Calculate the total cost of the missing champions (those in the combination but not in input list)
            missing_cost = sum([champ_to_cost[champ_names[i]] for i in missing_champs])

            # Store the combination, match percentage, and missing cost
            matched_combinations.append((comb, match_percentage, missing_cost, missing_champs))

    # Sort the combinations by match percentage (descending) and by missing cost (ascending)
    matched_combinations.sort(key=lambda x: (-x[1], x[2]))

    # Return the top N combinations
    return matched_combinations[:top_n]

def load_combinations_from_file(filename):
    combinations = []

    with open(filename, 'rb') as file:
        while True:
            # First, read the length of the next combination (1 byte)
            length_bytes = file.read(1)
            if not length_bytes:
                break  # End of file
            length = int(np.frombuffer(length_bytes, dtype=np.uint8)[0])

            # Then, read the combination itself (length bytes)
            combination = np.fromfile(file, dtype=np.uint8, count=length)
            combinations.append(combination)

    return np.array(combinations, dtype=object)

def solve_comp(input_champs, file, mc, cs):
    input_champs = [champ.capitalize() for champ in input_champs]
    comps = load_combinations_from_file('C:/Users/Benjamin/Documents/TraitTrackerSolver/tts/data/7_champs_7+_traits.bin')
    top_combinations = find_top_combinations(input_champs, comps, champion_traits_matrix, trait_levels, mc, cs)
    out=[]
    print(len(comps))
    for comb, match_percentage, missing_cost, missing_champs in top_combinations:
        champ_names_comb = [champ_names[i] for i in comb]
        missing_champs_name = [champ_names[i] for i in missing_champs]
        row = [f"Comp: {', '.join(champ_names_comb)}", f"Match: {match_percentage:.1%}", f"Gold needed: {missing_cost}", f"buy: {', '.join(missing_champs_name)}"]
        out.append(row)
    for row in out:
      print("{: <80} {: <14} {: <16} {: <7}".format(*row))

## TODO add emblems