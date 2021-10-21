import random
from MainGame import Car

import numpy as np
import random as rd

from scipy.special import softmax

input_n = 3
# input_dict = {}
hidden_n = 4
# hidden_dict = {}
weights1 = input_n * hidden_n
# weights1_dict = {}
output_n = 2
# output_dict = {}
weights2 = hidden_n * output_n
# weights2_dict = {}


def sigmoid_matrix(x):
    return 1 / (1 + np.exp(-x))


input_1 = abs((Car.distance_f - Car.position).length()) / 100
input_2 = abs((Car.distance_f_R - Car.position).length()) / 100
input_3 = abs((Car.distance_f_L - Car.position).length()) / 100

i1 = input_1
i2 = input_2
i3 = input_3

i = np.array([i1, i2, i3])


# ----------------------------------
# Weights 1:

w1_1 = rd.random()
w1_2 = rd.random()
w1_3 = rd.random()
w1_4 = rd.random()

w2_1 = rd.random()
w2_2 = rd.random()
w2_3 = rd.random()
w2_4 = rd.random()

w3_1 = rd.random()
w3_2 = rd.random()
w3_3 = rd.random()
w3_4 = rd.random()


w1 = np.array([[w1_1, w1_2, w1_3, w1_4], [w2_1, w2_2, w2_3, w2_4], [w3_1, w3_2, w3_3, w3_4]])

# -------------------------------------

w1_r = np.random.rand(input_n, hidden_n)

net1 = np.dot(i, w1_r)
# print(net1)
act_hidden = sigmoid_matrix(net1)
# print(act_hidden)


# -----------------------------------
# Weights 2:

w21_1 = rd.random()
w21_2 = rd.random()

w22_1 = rd.random()
w22_2 = rd.random()

w23_1 = rd.random()
w23_2 = rd.random()

w24_1 = rd.random()
w24_2 = rd.random()

w2 = np.array([[w21_1, w21_2], [w22_1, w22_2], [w23_1, w23_2], [w24_1, w24_2]])

# -------------------------------------------

w2_r = np.random.rand(hidden_n, output_n)

net2 = np.dot(act_hidden, w2_r)
# print(net2)
act_output = softmax(net2)
# print(act_output)
# print(np.sum(act_output))


def direction_decision():
    if act_output[0] > 60:
        Car.goleft = 1
        Car.goright = 0
    elif act_output[1] > 60:
        Car.goright = 1
        Car.goleft = 0
    else:
        Car.goright = 0
        Car.goleft = 0