import numpy as np
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