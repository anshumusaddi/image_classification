from typing import Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from libs.clustering.utils.general_utils import parallelize


def cosine_similarity_chunk(t: Tuple) -> np.ndarray:
    return cosine_similarity(t[0][t[1][0]: t[1][1]], t[0]).astype('float16')


def get_cosine_similarity(
        x: np.ndarray, verbose: bool = True, chunk_size: int = 1000, threshold: int = 10000
) -> np.ndarray:
    n_rows = x.shape[0]

    if n_rows <= threshold:
        return cosine_similarity(x)

    else:
        start_idxs = list(range(0, n_rows, chunk_size))
        end_idxs = start_idxs[1:] + [n_rows]
        cos_sim = parallelize(
            cosine_similarity_chunk,
            [(x, idxs) for i, idxs in enumerate(zip(start_idxs, end_idxs))],
            verbose,
        )

        return np.vstack(cos_sim)
