import numpy as np
import multiprocessing
import os

# Helper function to process a chunk of the file
def process_chunk(start, end, filename):
    combinations = []
    with open(filename, 'rb') as file:
        file.seek(start)
        while file.tell() < end:
            # First, read the length of the next combination (1 byte)
            length_bytes = file.read(1)
            if not length_bytes:
                break  # End of file or chunk

            length = int(np.frombuffer(length_bytes, dtype=np.uint8)[0])

            # Then, read the combination itself (length bytes)
            combination = np.fromfile(file, dtype=np.uint8, count=length)
            combinations.append(combination)

    return combinations


# Main function to parallelize the reading process
def load_combinations_from_file(filename, chunk_size=1024 * 1024):
    # Get the size of the file
    file_size = os.path.getsize(filename)

    # Determine the chunk boundaries
    chunks = [(i, min(i + chunk_size, file_size)) for i in range(0, file_size, chunk_size)]

    # Use multiprocessing to process the chunks in parallel
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.starmap(process_chunk, [(start, end, filename) for start, end in chunks])

    # Flatten the results and return as a numpy object array
    combinations = [item for sublist in results for item in sublist]
    return np.array(combinations, dtype=object)