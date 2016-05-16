import math
from node import Node
import sys




def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''

    data_set=clean_data(data_set , len(attribute_metadata), attribute_metadata)
    return helper(data_set, attribute_metadata, numerical_splits_count, depth)



def helper(data_set, attribute_metadata, numerical_splits_count, depth):
    root = Node()
    root.name = 'default'
    if len(data_set) == 0 :
        return root
    else :
        if check_homogenous(data_set) != None :
            root.label = check_homogenous(data_set)
            return root
        else :
            if  len(attribute_metadata) == 1 or depth == 0 :
                root.label = mode(data_set)
                return root
            else :
                best_attribute = pick_best_attribute(data_set, attribute_metadata , numerical_splits_count)
                if best_attribute[0] == False :
                    root.label = mode(data_set)
                    return root


                else :
                    root.name = attribute_metadata[best_attribute[0]]['name']

                    root.decision_attribute = best_attribute[0]

                    if best_attribute[1] == False : # dictionary

                        root.is_nominal = None
                        temp_dict = split_on_nominal(data_set,best_attribute[0])
                        depth -= 1
                        for key in temp_dict.keys():
                            root.children[key] = helper(temp_dict[key],attribute_metadata,numerical_splits_count,depth)
                    else :
                        numerical_splits_count[best_attribute[0]] -= 1

                        root.is_nominal = best_attribute[1]
                        root.splitting_value = best_attribute[1]
                        temp_tuple = split_on_numerical(data_set,best_attribute[0] , best_attribute[1])
                        depth -= 1
                        root.children[0] = (helper(temp_tuple[0] ,attribute_metadata,numerical_splits_count,depth))
                        root.children[1] = (helper(temp_tuple[1] ,attribute_metadata,numerical_splits_count,depth))
                    return root



def clean_data(data_set , length, attribute_metadata) :
    

    mode = []  # mode of each attribute
    avg = []  # median of each attribute 
    for i in range(0 , length) :
        temp = 0.0
        count = 0.0
        for j in range(0 , len(data_set) ) :
            if data_set[j][i] != None :
                temp += data_set[j][i]
                count += 1
        avg.append(temp/count)


    for i in range(0,length):
        mode.append(mode_clean(data_set , i))

    my_res = []

    for k in range(0, length) :
        if attribute_metadata[k]['is_nominal'] == True:
            my_res.append(mode[k])
        else:
            my_res.append(avg[k])

    cursor = open('./output/clean.txt','w+')
    for x in range(0,length):
        cursor.write(str(my_res[x]) + ",")
    cursor.close()  

    for i in range(0,len(data_set)):
        for j in range(0 , length) :
            if data_set[i][j] == None :
                    data_set[i][j] = my_res[j]

    
    return data_set



def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    # Your code here

    for i in range(0,len(data_set)):
        if i == 0 :
            continue 
        if data_set[i][0] != data_set[i-1][0] :
            return None
    return data_set[0][0]

# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # Your code here

    res1 = False
    res2 = False
    temp = 0
        
    for x in range(1, len(attribute_metadata)):
        

        my_attr = attribute_metadata[x]
        
        if numerical_splits_count[x] > 0 :
            if my_attr['is_nominal'] == True :
                temp1 = gain_ratio_nominal(data_set, x)
                if  temp1 > temp:
                    temp = temp1
                    res1 = x
                    res2 = False
            else : 
                temp2 = gain_ratio_numeric(data_set, x, 500)
                if temp2[0] > temp :
                    temp = temp2[0]
                    res1 = x 
                    res2 = temp2[1]

    if temp == 0 :
        return (False, False)

    return (res1, res2)



def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here
    d = {} 
    max_num = 0 ;
    result = data_set[0][0]
    for i in range(0,len(data_set)):
        if (data_set[i][0] != None) :
            if d.has_key(data_set[i][0]) :
                d[data_set[i][0]]+= 1 
                if d[data_set[i][0]] >= max_num :
                    max_num = d[data_set[i][0]]
                    result = data_set[i][0]
            else :
                d[data_set[i][0]] = 0 
    return result

def mode_clean(data_set , index):

    d = {} 
    max_num = 0 ;
    result = data_set[2][index]
    for i in range(0,len(data_set)):
        if (data_set[i][index] != None) :
            if d.has_key(data_set[i][index]) :
                d[data_set[i][index]]+= 1 
                if d[data_set[i][index]] >= max_num :
                    max_num = d[data_set[i][index]]
                    result = data_set[i][index]
            else :
                d[data_set[i][index]] = 0 
    return result
        


def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''

    total = len(data_set)
    ones = 0.0
    zeros = 0.0
    for i in range(0, len(data_set)):
        if data_set[i][0] == 1:
           ones += 1
    if ones == 0:
        return 0
    if ones == total:
        return 0
    else:
        zeros = total - ones
        pplus = ones / total
        pminus = zeros / total
        result = -(pplus) * math.log10(pplus) / math.log10(2) - (pminus) * math.log10(pminus) / math.log10(2)
        return result
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    # Your code here

    dict = split_on_nominal(data_set , attribute)
    total_entropy = entropy(data_set) 
    total_dataset = len(data_set) + 0.0
    rest = 0.0 
    rest2 = 0.0
    for k in dict.keys() :
        rest += (len(dict.get(k))+0.0)/total_dataset * entropy(dict.get(k))
        rest2 += (len(dict.get(k))+0.0)/total_dataset * math.log((len(dict.get(k))+0.0)/total_dataset,2)
    if rest2 == 0.0 :
        return 0.0
    return (total_entropy - rest ) / -rest2     # !!!!!!!!!!!!!!!!


# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    temp = 0
    mydic = {}
    temp1 = []
    for i in range(0, len(data_set)):
        temp1.append(data_set[i][attribute])

    while temp < len(temp1): 
        temp2 = split_on_numerical(data_set, attribute, temp1[temp])
        k1 = (len(temp2[0])+0.0)/(len(data_set)+0.0)
        k2 = (len(temp2[1])+0.0)/(len(data_set)+0.0)

        if (k1 == 0 or k2 == 0):
            h = 0
        else :
            h1 = entropy(data_set) - (k1*entropy(temp2[0])) - (k2*entropy(temp2[1]))
            h2 = -((k1*(0.0+math.log(k1,2)))+(k2*(0.0+math.log(k2,2))))
            h = h1/h2
            
        mydic[temp1[temp]] = h
        temp += steps

    res1 = 0
    res2 = 0
    for k in mydic.keys() :
        if mydic.get(k) > res1 :
            res1 = mydic.get(k)
            res2 = k

    return (res1, res2)
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [1,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here

    mydic = {}
    for x in range(0,len(data_set)):
        if  mydic.has_key(data_set[x][attribute]) :
            mydic.get(data_set[x][attribute]).append(data_set[x])
        else : 
            myarr2 = []
            myarr2.append(data_set[x])
            mydic[data_set[x][attribute]] = myarr2

    return mydic

# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    list_less = [] 
    list_more = []

    for i in range(0,len(data_set)):
        if data_set[i][attribute] < splitting_value :
            list_less.append(data_set[i])
        else :
            list_more.append(data_set[i])    
    return (list_less, list_more)

# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])



