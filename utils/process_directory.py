from libs import get_similarity


def process_directory(directory):
    clusters = get_similarity(directory, scores=False)
    return clusters
