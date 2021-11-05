import numpy as np


def mutator_w(w, margin):

    weights_list = []
    
    for weights in w:

        high = weights * (margin / 100)
        low = high * (-1)
        delta_w = np.random.uniform(low=low, high=high, size=weights.shape)
        weights_list.append(weights + delta_w)

    return weights_list


def mutator_b(b, margin):

    biases_list = []

    for biases in b:

        high = biases * (margin / 100)
        low = high * (-1)
        delta_b = np.random.uniform(low=low, high=high, size=biases.shape)
        biases_list.append(biases + delta_b)
    
    return biases_list
