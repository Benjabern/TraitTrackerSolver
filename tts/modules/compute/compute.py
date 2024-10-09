import numpy as np
from numba import njit
from tts.lib.data import champions, traits
from tqdm import tqdm

#Create mappings
trait_to_index = {trait["name"]: idx for idx, trait in enumerate(traits)}

# Create a matrix of champions vs traits
num_champions = len(champions)
num_traits = len(traits)
champion_traits_matrix = np.zeros((num_champions, num_traits), dtype=np.int64)

for i, champ in enumerate(champions):
    for trait in champ["traits"]:
        if trait in trait_to_index:
            champion_traits_matrix[i, trait_to_index[trait]] = 1

# Create a trait level array (activation thresholds)
trait_levels = np.array([trait["levels"][0] for trait in traits])


@njit
def comb_n_r(n, r):
    if r > n:
        return 0
    r = min(r, n - r)  # symmetry
    numerator = 1
    denominator = 1
    for i in range(1, r + 1):
        numerator *= (n - i + 1)
        denominator *= i
    return numerator // denominator

# # Step 3: Custom combinations generator
@njit
def generate_combinations(n, r):
    total_combos = comb_n_r(n, r)  # Total number of combinations
    result = np.empty((total_combos, r), dtype=np.uint8)  # Pre-allocate array for combinations
    indices = np.arange(r)

    result_idx = 0
    while True:
        result[result_idx] = indices.copy()
        result_idx += 1

        # Find the rightmost element that can be incremented
        i = r - 1
        while i >= 0 and indices[i] == i + n - r:
            i -= 1
        if i < 0:
            break
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[i] + j - i
    return result


# JIT function to check active traits
@njit
def check_active_traits(combo_indices, champ_traits, trait_levels):
    trait_sums = np.sum(champ_traits[combo_indices], axis=0)
    active_traits = 0
    for i in range(len(trait_levels)):
        if trait_sums[i] >= trait_levels[i]:
            active_traits += 1
    return active_traits

def generate_valid_comps(champion_traits, trait_levels, n, x, file_path):
    num_champions = champion_traits.shape[0]

    # Open the file in binary write mode
    with open(file_path, 'wb') as file_buffer:
        for r in range(1, n + 1):
            total_combos = int(comb_n_r(num_champions, r))
            indices = np.arange(r, dtype=np.uint8)

            result_idx = 0

            # Initialize the progress bar for this combination length
            with tqdm(total=total_combos, desc=f"Processing combinations of length {r}") as pbar:
                while result_idx < total_combos:
                    # Check the combination directly
                    active_traits = check_active_traits(indices, champion_traits, trait_levels)

                    if active_traits >= x:
                        # Write the length of the combination
                        length = np.array([len(indices)], dtype=np.uint8)
                        file_buffer.write(length.tobytes())

                        # Write the valid combination directly to the buffer
                        file_buffer.write(indices.tobytes())

                    # Generate the next combination
                    i = r - 1
                    while i >= 0 and indices[i] == i + num_champions - r:
                        i -= 1
                    if i < 0:
                        break
                    indices[i] += 1
                    for j in range(i + 1, r):
                        indices[j] = indices[i] + j - i
                    result_idx += 1
                    pbar.update(1)  # Update the progress bar for each combination

# calculate valid combinations
def run_computation(n, x):
    generate_valid_comps(champion_traits_matrix, trait_levels, n, x, f'out/{n}_champs_{x}+_traits.bin')

## TODO emblems & on the fly