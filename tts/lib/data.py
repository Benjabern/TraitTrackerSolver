import json
import numpy as np
import os
import tts
def load_data(set):
  libpath = os.path.abspath(tts.lib.__file__).rstrip('__init__.py')
  set_data = json.load(open(libpath+set+'.json'))
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
