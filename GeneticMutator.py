import random

import numpy as np
import random

from BetterNN import Network

margin = 2

def mutator_w(w, margin) -> Network:
    
    mutated_weights = []
    delta_w = []
    
    for weights in w:

        for l in weights:

            for i in l:

                low = i * (1.0 - margin / 100)
                high = i * (1.0 + margin / 100)
                delta_w.append(random.uniform(low, high))

        mutated_weights.append(weights + np.array(delta_w).reshape(weights.shape))
        delta_w.clear()
        
        w = mutated_weights
        return w
        
def mutator_b(b, margin) -> Network:
    mutated_biases = []
    delta_b = []
     
    for biases in b:
        
        for l in biases:
            
            for i in l:
                
                low = i * (1.0 - margin / 100)
                high = i * (1.0 + margin / 100)
                delta_b.append(random.uniform(low, high))
                
        mutated_biases.append(biases + np.array(delta_b).reshape(biases.shape))
        delta_b.clear()
        
    b = mutated_biases
    
    return b

    # TODO: Ändern zu np.random.unify(), weil es arrays ebenfalls annimmt... ;-;
