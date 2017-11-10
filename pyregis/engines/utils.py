import numpy as np


def k_argmin(array, k):
    sorted_idx = np.argsort(array, axis=None)
    k_sorted = sorted_idx[:k]
    return k_sorted


def k_argmax(array, k):
    sorted_idx = np.argsort(array, axis=None)
    k_sorted = np.flip(sorted_idx[-k:], axis=-1)
    return k_sorted
