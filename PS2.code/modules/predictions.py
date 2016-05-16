import os.path
from operator import xor
from parse import *

# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    predict_set, attribute_metadata = parse(predict, True)
    file = open('./output/PS2.csv', 'w+')
    temp = ''
    for attribute in attribute_metadata:
        temp += (attribute['name'] + ',')
    temp = temp[7:] + temp[:7]
    file.write(temp[:-1] + '\n')
    for data in predict_set:
        output = tree.classify(data)
        temp = str(output) + ','
        for value in data[1:]:
            if value == None:
                temp += '?,'
            else:
                temp += str(value) + ','
        temp = temp[2:] + temp[:2]

        file.write(temp[:-1] + '\n')


    file.close()