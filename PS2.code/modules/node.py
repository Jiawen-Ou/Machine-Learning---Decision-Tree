# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 if numeric and a dictionary if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes
#       to split on or the data is homogenous
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        '''
        given a single observation, will return the output of the tree
        '''
	# Your code here
        temp = self

        while temp.label == None :
            if instance[temp.decision_attribute] == None:
                text_file = open("./output/clean.txt", "r")
                default = text_file.read().split(',')
                if len(default) == 0:
                    print 'no decision tree exist.'
                else:
                    instance[temp.decision_attribute] = default[temp.decision_attribute]
                text_file.close()

            if temp.is_nominal == None :
                if not temp.children.has_key(instance[temp.decision_attribute]) :
                    return 1

                else :
                    temp = temp.children.get(instance[temp.decision_attribute])
                    

            else :
                if instance[temp.decision_attribute] < temp.splitting_value :
                    temp = temp.children[0]
                else :
                    temp = temp.children[1]
        return temp.label




    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        '''
        # Your code here


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        
        node = self
        res = []
        res_str = ""
        res2 = []
        res2.append(res_str)
        dnf_helper(node, res, res2)
        return res2[0]
        
    def split_count(self):

        root = self
        q = [root]
        count = 0
        while q :
            node = q.pop(0)
            if node.label == None:
                count += 1
                if node.is_nominal == None:
                    for k in node.children.keys():
                        q.append(node.children.get(k))
                else :
                    q.append(node.children[0])
                    q.append(node.children[1])
        return count


def dnf_helper (node, res, res2):


    if node.label != None:
        if node.label == 1:
            res2[0] += "("
            for x in range(0, len(res)):
                res2[0] += str(res[x])
                if x != (len(res)-1):
                    res2[0] += " ^ "
            res2[0] += ")"
            res2[0] += " v "
            # print("Result " + res2[0])
        res.pop()
        return
    else : 
        if node.is_nominal == None:
            for k in node.children.keys():
                temp_str = str(node.name) + " = " + str(k)
                res.append(temp_str)
                dnf_helper(node.children.get(k), res, res2)
        else :
            temp_str = str(node.name) + " < " + str(node.splitting_value)
            res.append(temp_str)
            dnf_helper(node.children[0], res, res2)
            temp_str = str(node.name) + " >= " + str(node.splitting_value)
            res.append(temp_str)
            dnf_helper(node.children[1], res, res2)

























