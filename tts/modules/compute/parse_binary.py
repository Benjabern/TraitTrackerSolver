import numpy as np

def load_combinations_from_file(filename):
    with open(filename, 'rb') as file:
        data = file.read()

    # Convert the binary data into a numpy array
    data_array = np.frombuffer(data, dtype=np.uint8)

    combinations = []
    i = 0
    while i < len(data_array):
        length = int(data_array[i])
        i += 1
        combination = data_array[i:i + length]
        combinations.append(combination)
        i += length

    return np.array(combinations, dtype=object)
