import numpy
import random
import math

inputs = 3
inputs_list = []
hidden_layers = 4
hidden_layers_list = []
weights1 = inputs * hidden_layers
weights1_list = []
output_layers = 2
output_layers_list = []
weights2 = hidden_layers * output_layers
weights2_list = []
bias = -0.7


def sigmoid(s):

    return 1 / (1 + math.exp(-s))


def create_input_list():

    for x in range(1, inputs + 1):
        inputs_list.append((random.random() - 0.4))


def create_weights1():

    for x in range(1, weights1 + 1):
        weights1_list.append(random.random())


def create_weights2():

    for x in range(1, weights2 + 1):
        weights2_list.append(random.random())


def create_hidden_layer_list():

    for x in range(0, hidden_layers):

        zw = 0

        for y in range(0, inputs - 1):
            zw += inputs_list[y] * (weights1_list[y * hidden_layers + 1])

        zw += bias

        print(f'Before Sigmoid:{zw}')

        hidden_layers_list.append(sigmoid(zw))

def create_output_layer_list():

    for x in range(0, output_layers):

        zw2 = 0

        for y in range(0, hidden_layers):
            zw2 += hidden_layers_list[y] * (weights2_list[y * output_layers + 1])

        zw2 += bias

        print(f'Before Sigmoid2:{zw2}')

        output_layers_list.append(sigmoid(zw2))


create_input_list()
create_weights1()
create_hidden_layer_list()
create_weights2()
create_output_layer_list()

print(f'Inputs:{inputs_list}')
print(weights1_list)
print("Hidden Neurons:", hidden_layers_list)
print(output_layers_list)

