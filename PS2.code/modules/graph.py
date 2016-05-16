from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import *

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    size = len(train_set) * pct 
    # print("size is " + str(size) + str(len(train_set)))
    new_train_set = []
    x = 0
    while x < size:
        new_train_set.append(train_set[x])
        x += 1
    if len(new_train_set) > 2:
        tree2 = ID3(new_train_set, attribute_metadata, numerical_splits_count, 20)
        acc_1 = validation_accuracy(tree2, validate_set)
        reduced_error_pruning(tree2,new_train_set,validate_set)
        acc_2 = validation_accuracy(tree2, validate_set)
    else:
        acc_1 = 0.0
        acc_2 = 0.0

    return (acc_1,acc_2)

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, pcts):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    temp1 = 0
    temp2 = 0
    for x in range(0, iterations):
        temp = get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, pcts)
        temp1 += temp[0]
        temp2 += temp[1]
    return (temp1/(iterations+0.0),temp2/(iterations+0.0))

# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''

    x = lower
    arr = []
    while x < upper:
        arr.append(get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, iterations, x))
        x += increment

    # print("percentage    unpruned    pruned")
    # for k in range(0,len(arr)):
    #     print(str(k) + "  " + str(arr[k][0]) + "  " + str(arr[k][1]))

