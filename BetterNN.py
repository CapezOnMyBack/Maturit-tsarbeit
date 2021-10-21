import numpy as np
from scipy.special import softmax

input_n = 5

hidden_n = 4

output_n = 2

wr = 1.0


def sigmoid_matrix(x):
    return 1 / (1 + np.exp(-x))


def create_inputs(car):
    input_1 = abs((car.distance_f - car.position).length()) / 100
    input_2 = abs((car.distance_f_R - car.position).length()) / 100
    input_3 = abs((car.distance_f_L - car.position).length()) / 100
    input_4 = abs((car.distance_R - car.position - 4 * car.vel).length()) / 100
    input_5 = abs((car.distance_L - car.position - 4 * car.vel).length()) / 100
    return np.array([input_1, input_2, input_3, input_4, input_5])


# -------------------------------------------------------------------------------------
# Weights 1&2:

def create_weights_1():
    return np.random.uniform(low=-wr, high=wr, size=(input_n, hidden_n))


def create_weights_2():
    return np.random.uniform(low=-wr, high=wr, size=(hidden_n, output_n))


# ----------------------------------------------------------------------------------
# Biases 1&2:

def create_bias_1():
    return np.random.uniform(low=-wr, high=wr, size=hidden_n)


def create_bias_2():
    return np.random.uniform(low=-wr, high=wr, size=output_n)


# ------------------------------------------------------------------------------------

def forward(x, w1, w2, b1, b2):
    net1 = np.dot(x, w1) + b1
    # print(net1)
    act_hidden = sigmoid_matrix(net1)
    # print(act_hidden)
    net2 = np.dot(act_hidden, w2) + b2
    # print(net2)
    act_output = softmax(net2)
    # print(act_output)
    # print(np.sum(act_output))
    return act_output


# --------------------------------------------------------------------------------------

def create_network(car):
    w1 = create_weights_1()
    w2 = create_weights_2()
    b1 = create_bias_1()
    b2 = create_bias_2()

    def direction_decision():

        output = forward(create_inputs(car), w1, w2, b1, b2)

        if output[0] > 0.6:
            car.goleft = 1
            car.goright = 0
        elif output[1] > 0.6:
            car.goright = 1
            car.goleft = 0
        else:
            car.goright = 0
            car.goleft = 0

    return direction_decision
