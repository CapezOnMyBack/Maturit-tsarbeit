from typing import List
import numpy as np
from scipy.special import softmax
from config import wr


class Network:

    @classmethod
    def new(cls, weights, biases, architecture):
        network = cls(architecture, False)
        network.weights = weights
        network.biases = biases
        return network

    @staticmethod
    def sigmoid_matrix(x):
        return 1 / (1 + np.exp(-x))

    def __init__(self, architecture: List[int], new_init: bool = True):

        self.architecture = architecture
        self.weights = []
        self.biases = []

        if new_init:
            self.random_init()

    def random_init(self):

        for n1, n2 in zip(self.architecture[:-1], self.architecture[1:]):
            self.weights.append(np.random.uniform(
                low=-wr, high=wr, size=(n1, n2)))
        for n in self.architecture[1:]:
            self.biases.append(np.random.uniform(
                low=-wr, high=wr, size=n))

    def forward(self, activations):

        for weights, biases in zip(self.weights[:-1], self.biases[:-1]):
            net = np.dot(activations, weights) + biases
            activations = self.sigmoid_matrix(net)

        net = np.dot(activations, self.weights[-1]) + self.biases[-1]
        return softmax(net)

    # Todo: Softmax really usefull?

# --------------------------------------------------------------------------------------
