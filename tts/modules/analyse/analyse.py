import matplotlib.pyplot as plt
import numpy as np
import tts.data
import os
from tts.lib.data import traits
from tts.modules.compute.parse_binary import load_combinations_from_file
from tts.lib.parse_data import champ_names, champ_to_cost, trait_levels, champion_traits_matrix, champ_to_index, num_traits, num_champions, trait_to_index
path = os.path.abspath(tts.data.__file__).rstrip('__init__.py')

def convert_indices_to_names(valid_combos, champion_list):
    name_combos = []
    for combo in valid_combos:
        name_combos.append([champion_list[i]["name"] for i in combo])
    return name_combos

# def count_active_traits(combination, trait_matrix, min_levels):
#
#     active_traits = np.negative(min_levels)
#     np.expand_dims(active_traits, 0)
#     # Select the sub-matrix of the trait matrix corresponding to the selected champions
#     selected_trait_matrix = trait_matrix[combination]
#     print(selected_trait_matrix)
#     # Sum across the selected champions to count trait occurrences
#     trait_counts = selected_trait_matrix.sum(axis=0)
#     active_traits = np.vstack((active_traits, trait_counts))
#     # Check how many traits meet the minimum level requirements
#     active_traits = np.sum(active_traits,  axis=0)
#     active_traits[active_traits == 0] = 1
#     active_traits[active_traits < 0] = 0
#     return active_traits
#
#
# # distribution of costs
# # max trait number
# # max trait number comp
# # cost of max trait number comp
# def trait_distribution(combinations, trait_matrix, min_levels):
#     trait_sum = np.zeros(min_levels)
#     np.expand_dims(trait_sum, 0)
#     active_traits = []
#     print(combinations[0])
#     a=count_active_traits(combinations[0], trait_matrix, min_levels)
#     # for combo in combinations:
#     #     a_traits = count_active_traits(combo, trait_matrix, min_levels)
#     #     print(trait_sum, a_traits)
#     #     trait_sum = np.vstack((trait_sum, a_traits))
#     #     nr_traits = sum(a_traits)
#     #     active_traits.append(nr_traits)
#     # trait_sum = np.sum(trait_sum, axis=0)
#     #return trait_sum, active_traits

from multiprocessing import Pool, cpu_count

# Function to count active traits for each champion combination
def count_traits(combo, trait_levels):
    # Sum across champions for each trait to get the count per trait
    trait_sums = np.sum(combo, axis=0)
    # Determine which traits are active (i.e., meet or exceed minimum level)
    active_traits = trait_sums >= trait_levels
    return trait_sums, np.sum(active_traits)

# Parallel processing wrapper
def parallel_trait_count(champion_combos, trait_levels):
    with Pool(cpu_count()) as pool:
        results = pool.starmap(count_traits, [(combo, trait_levels) for combo in champion_combos])
    return results

# Function to plot the distribution of individual trait activations and active traits
def plot_trait_distribution(total_trait_sums, active_trait_counts):
    # Plotting the individual trait activations
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar([trait['name'] for trait in traits], total_trait_sums, color='blue', alpha=0.7)
    plt.xticks(rotation=30, ha='right')
    #plt.bar(range(len(total_trait_sums)), total_trait_sums, color='blue', alpha=0.7)
    #plt.xlabel([trait['name'] for trait in traits])
    plt.xlabel('Trait Index')
    plt.ylabel('Activation Count')
    plt.title('Total Trait Activations Across All Comps')

    # Plotting the distribution of activated traits per combination
    plt.subplot(1, 2, 2)
    plt.hist(active_trait_counts, bins=range(np.max(active_trait_counts)+2), align='left', color='green', alpha=0.7)
    plt.xlabel('Number of Activated Traits')
    plt.ylabel('Frequency')
    plt.title('Distribution of Activated Traits per Comp')

    plt.tight_layout()
    plt.show()


def run_analysis(file):
    suffix = file[len(file) - 4:]
    file = path+file
    if suffix == '.npy':
        comps = np.load(file, allow_pickle=True)
    if suffix == '.bin':
        comps = load_combinations_from_file(file)

    champion_combos = [champion_traits_matrix[combination] for combination in comps]
    results = parallel_trait_count(champion_combos, trait_levels)

    # Summing the trait activations across all combinations
    total_trait_sums = np.sum([r[0] for r in results], axis=0)
    active_trait_counts = np.array([r[1] for r in results])

    # Plotting the distribution
    plot_trait_distribution(total_trait_sums, active_trait_counts)