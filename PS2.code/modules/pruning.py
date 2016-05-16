from node import Node
from ID3 import *
from operator import xor


# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(root,training_set,validation_set):
    '''
    take the a node, training set, and validation set and returns the improved node.
    You can implement this as you choose, but the goal is to remove some nodes such that doing so improves validation accuracy.
    '''

    node = root
    prune_helper(root, node, training_set, validation_set)


def prune_helper (root, node, training_set, validation_set):

    if node.label != None :
        return 
    else :
        if node.is_nominal == None :
            for k in node.children.keys() :
                prune_helper(root,node.children.get(k), training_set, validation_set)
        else :
                prune_helper(root,node.children[0],training_set,validation_set)
                prune_helper(root,node.children[1],training_set,validation_set)

        temp = node.label

        acuraccy_ori = validation_accuracy(root , validation_set)
        node.label = 0 
        acuraccy_0 = validation_accuracy(root , validation_set) 
        node.label = 1 
        acuraccy_1 = validation_accuracy(root , validation_set)
       
        

        if acuraccy_ori >= acuraccy_1 and acuraccy_ori >= acuraccy_0 :
            node.label = temp
        else :
            if acuraccy_1 >= acuraccy_0 :
                node.label = 1
            else :
                node.label = 0




def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    # Your code here

    

    correct = 0 

    for i in range(0, len(validation_set)):
        if tree.classify(validation_set[i]) == validation_set[i][0]:
            correct +=1 

    return (correct+0.0)/(len(validation_set)+0.0)
