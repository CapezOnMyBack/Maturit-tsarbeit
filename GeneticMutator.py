import random

import numpy as np
import random

from BetterNN import Network

margin = 2

def mutator(w, b, margin) -> Network:
    mutated_weights = []
    mutated_biases = []
    delta_w = []

    for weights in w:

        for l in weights:

            for i in l:

                low = i * (1.0 - margin / 100)
                high = i * (1.0 + margin / 100)
                delta_w.append(random.uniform(low, high))

        mutated_weights.append(weights + np.array(delta_w).reshape(weights.shape))
        delta_w.clear()

    # TODO: MUTATOR FERTIG MACHEN GENAU GLEICH FÜR BIASES WIE BEI WEIGHTS
    # TODO: Ändern zu np.random.unify(), weil es arrays ebenfalls annimmt... ;-;
