from libs import get_similarity


def process_directory(directory):
    sim_sets = get_similarity(directory, scores=True)
    return sim_sets
