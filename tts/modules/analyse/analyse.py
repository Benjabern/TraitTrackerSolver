import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool, cpu_count
import os
from tts.lib.data import load_data
from tts.modules.compute.parse_binary import load_combinations_from_file
import tts.data
path = os.path.abspath(tts.data.__file__).rstrip('__init__.py')


def convert_indices_to_names(combos, champion_list):
    name_combos = []
    for combo in combos:
        name_combos.append([champion_list[i]["name"] for i in combo])
    return name_combos


# Function to count active traits for each champion combination
def count_traits(combo, trait_levels):
    trait_sums = np.sum(combo, axis=0)
    active_traits = trait_sums >= trait_levels
    return active_traits

# Parallel processing wrapper
def trait_count(champion_combos, trait_levels):
    with Pool(cpu_count()) as pool:
        results = pool.starmap(count_traits, [(combo, trait_levels) for combo in champion_combos])
    return results

# Function to plot the distribution of individual trait activations and active traits
def plot_trait_distribution(total_trait_sums, active_trait_counts, traits):
    # Plotting the individual trait activations
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.bar([trait['name'] for trait in traits], total_trait_sums, color='blue', alpha=0.7)
    plt.xticks(rotation=30, ha='right')
    plt.xlabel('Trait')
    plt.ylabel('Activation Count')
    plt.title('Total Trait Activations Across All Comps')

    # Plotting the distribution of activated traits per combination
    plt.subplot(1, 2, 2)
    plt.hist(active_trait_counts, bins=range(np.max(active_trait_counts)+2), align='left', color='green', alpha=0.7)
    plt.xlabel('Number of Activated Traits')
    plt.ylabel('Count')
    plt.title('Distribution of Activated Traits per Comp')

    plt.tight_layout()
    plt.show()


def run_analysis(file, set):
    champions, traits, champ_names, champ_to_index, champ_to_cost, champion_traits_matrix, trait_levels, trait_to_index = load_data(set)
    file = path+file
    comps = load_combinations_from_file(file)
    champion_combos = [champion_traits_matrix[np.array(combination, dtype=np.uint8)] for combination in comps]
    results = trait_count(champion_combos, trait_levels)

    # Summing the trait activations and active traits
    total_trait_sums = np.sum([r for r in results], axis=0)
    active_trait_counts = [np.sum(r) for r in results]

    # Plot the distribution
    plot_trait_distribution(total_trait_sums, active_trait_counts, traits)