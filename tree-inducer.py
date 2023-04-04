import math, numpy as np
import copy
import csv

'''
This Node class takes itself and a parent node. This node is used to build the decision
tree
'''
class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []
        self.splitFeature = None
        self.label = None
        self.leaf = False
        self.vote = None
        self.majority = None

'''
This Representative class takes itself, and id, part, and its votes. This class is used to
store all of the representative information
'''
class Representative:
    def __init__(self, id, party, votes):
        self.id = id
        self.party = party
        self.votes = votes

'''
This function takes in a file and creates a matrix of voting records for each 
representative
'''
def makeMatrix(file):
    matrix1 = []
    matrix2 = []
    
    with open(file) as file:
        count = 0
        tsvFile = csv.reader(file, delimiter='\t')
        for line in tsvFile:
            num = count % 4
            row = []
            for elem in line:
                row.append(elem)
            if num == 0:
                matrix2.append(row)
            else:
                matrix1.append(row)
            count += 1

    return matrix1, matrix2

'''
This function takes the numerators and the denominators for the entropy function
and returns the entropy
'''
def entropy(data):
    
    denom = len(data)
    firstNum = len(list(filter(lambda rep: rep.party == 'D', data)))
    secondNum = len(list(filter(lambda rep: rep.party == 'R', data)))
    
    # entropy formula
    if firstNum == 0 and secondNum == 0:
        entropy = 0
    elif firstNum == 0: 
        entropy = - (secondNum / denom) * math.log2(secondNum/ denom)
    elif secondNum == 0:
        entropy = - (firstNum / denom) * math.log2(firstNum / denom)
    else:
        entropy = - (firstNum / denom) * math.log2(firstNum/ denom) \
            - (secondNum / denom) * math.log2(secondNum / denom)
    
    return entropy

'''
This function takes a list of representatives and returns the maximum information gain
value and index of the feature with the highest information gain. It then returns that
maximum information gain and index of the feature with the highest information gain
'''    
def findSplits(reps):
    # entropy for each feature
    entropyList = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # calculate entropies for each feature
    options = ['+', '-', '.']
    counter = 0
    for i, elem in enumerate(entropyList):
        totalEnt = 0
        for j, item in enumerate(options):
            # print(item, elem)
            votesTotal = list(filter(lambda reps: reps.votes[i] == item, reps))
            # print("total votes: ",len(votesTotal))
            totalEnt += (len(votesTotal) / len(reps)) * entropy(votesTotal)
            counter += 1
        entropyList[i] = totalEnt
    
    # find the max gain of all the features
    oldEnt = entropy(reps)
    index = 0
    maxGain = 0
    for i, elem in enumerate(entropyList):
        theGain = oldEnt - entropyList[i]
        if theGain > maxGain:
            maxGain = theGain
            index = i
    
    return maxGain, index

'''
This function takes an array of Democrats and Republicans and returns the majority
party
'''
def majority(arr):
    
    dems = len([x for x in arr if x == 'D'])
    reps = len([x for x in arr if x == 'R'])
    size = len(arr)
    
    if size == 0 or dems == 0 or reps == 0:
        return None
    
    if dems/size > .5:
        return 'D'

    if reps/size > .5:
        return 'R'
    
    return None
 
'''
This function takes a tree and level and prints the tree structure
'''
def printTree(root, level=0):
    if root.leaf:
        print(" " * level, root.vote, root.label)
    else:
        if root.parent == None:
            print(" " * level, "Issue",root.splitFeature + ":")
        else:
            print(" " * level, root.vote, "Issue",root.splitFeature + ":")
    for child in root.children:
        printTree(child, level + 1)
    
'''
This function takes data, a node, and the vote. It then recurses through the data and finds
the maximum information gain for each data split. This function builds the tree structure
'''
def decisionTreeMaker(data, node, theVote):
    
    issues = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    dict = {letter:num for (letter, num) in enumerate(issues)}
    
    # get all representative information
    representatives = []
    for i, elem in enumerate(data):
        record = data[i]
        newRep = Representative(record[0], record[1], record[2])
        representatives.append(newRep)
    
    listReps = []
    for i, elem in enumerate(representatives):
        # get voting record
        rep = representatives[i]
        # append all representatives into the list of Reps
        listReps.append(rep.party)
    
    # find majority amount of members in data
    classification = majority(listReps)
    node.majority = classification
    
    # CHECK IF NUMBER OF REPS IS 0 OR REPS ARE TIED
    numOfReps = len(representatives)
    if numOfReps == 0 or classification == None:
        while node.parent is not None:
            maj = node.parent.majority # get parent's majority
            if maj is not None:
                node.label = maj
                node.leaf = True
                node.vote = theVote
                return node.label
            node = node.parent
            
    # CHECK IF MAX GAIN IS 0
    maxGain, index = findSplits(representatives)       
    if maxGain == 0:
        while node.parent is not None:
            maj = node.parent.majority # get parent's majority
            if maj is not None:
                node.label = maj
                node.leaf = True
                node.vote = theVote
                return node.label
            node = node.parent
    
    # CHECK IF ALL OF THE REPRESENTATIVES ARE THE SAME PARTY
    allSame = True
    element = listReps[0]
    for item in listReps:
        if element != item:
            allSame = False
            break
    if allSame == True:
        node.label = listReps[0]
        node.leaf = True
        return node.label
    
    # CHECK IF ALL REPS HAVE THE SAME VOTING RECORD IF NOT HOMOGENOUS
    listVotes = []
    for i, elem in enumerate(representatives):
        # get voting record
        record = representatives[i].votes
        listVotes.append(record)
    votesAllSame = True
    voteLength = len(listVotes[0])
    for i in range(voteLength):
        column = []
        for j in listVotes:
            column.append(j[i])
        check = column[0]
        # print(column)
        for item in column:
            if check != item:
                votesAllSame = False
                break  
    if votesAllSame:
        node.label = classification
        node.leaf = True
        node.vote = theVote
        return node.label
    
    # split the data on the feature with highest gain
    leftBranchData = [] # +
    middleBranchData = [] # -
    rightBranchData = [] # .
    for i, elem in enumerate(data):
        record = data[i]
        votes = record[2]
        votesList = [v for v in votes]
        if votesList[index] == '+':
            leftBranchData.append(record)
        elif votesList[index] == '-':
            middleBranchData.append(record)
        elif votesList[index] == '.':
            rightBranchData.append(record)
            
    
    # Make children nodes and add to parent node
    leftNode = Node(node) # +
    middleNode = Node(node) # -
    rightNode = Node(node) # .
    node.children.append(leftNode)
    node.children.append(middleNode)
    node.children.append(rightNode)
    node.splitFeature = dict[index]
    node.vote = theVote
    
    
    decisionTreeMaker(leftBranchData, leftNode, '+')
    decisionTreeMaker(middleBranchData, middleNode, '-')
    decisionTreeMaker(rightBranchData, rightNode, '.')

'''
This function takes a tree and creates a list of internal nodes. It then returns that list
of internal nodes.
'''
def makeListOfInternalDescendants(root):
    internalNodes = []
    queue = []
    queue.append(root)
    while(len(queue)):
        current = queue[0]
        queue.pop(0)
        
        isInternal = 0
        
        if current.leaf is False:
            isInternal = 1
            for child in current.children:
                queue.append(child)
        
        if (isInternal):
            internalNodes.append(current)
    
    return internalNodes
        
'''
This function takes a tree and dataset and finds a cut in the tree that has the highest
accuracy. Returns the root of the tree
'''
def pruneTree(root, tuneData):
    
    listOfInternalNodes = makeListOfInternalDescendants(root)
    representatives = []
    for i, elem in enumerate(tuneData):
        newRep = Representative(elem[0], elem[1], elem[2])
        representatives.append(newRep)
       
    maxAccuracy = 0
    bestNode = copy.deepcopy(root)
    
    # iterate over the list of internal nodes and finds the max accuracy
    for i in listOfInternalNodes:

        i.leaf = True
        i.label = i.majority
        
        newAccuracy = accuracy(root, representatives)
        if newAccuracy > maxAccuracy:
            maxAccuracy = newAccuracy
            bestNode = i
        
        i.leaf = False
        i.label = None
        
    # make the change permanent with best node to prune
    bestNode.leaf = True
    bestNode.label = bestNode.majority
    bestNode.children = []
    bestNode.splitFeature == None
    
    return root

'''
This function takes a tree and dataset, keeps pruning until the accuracy begins to drop
and returns the root of the completely pruned tree
'''
def completelyPruned(root, data):
    
    representatives = []
    for i, elem in enumerate(data):
        newRep = Representative(elem[0], elem[1], elem[2])
        representatives.append(newRep)
    
    theRoot = root
    currAccuracy = accuracy(theRoot, representatives)
    maxAccuracy = 0
    while True:
        theRoot = pruneTree(theRoot, data)
        currAccuracy = accuracy(theRoot, representatives)
        if currAccuracy <= maxAccuracy:
            break
        maxAccuracy = currAccuracy
    
    return theRoot

'''
This function takes a tree, dataset, list of representatives, and index. It then deletes
a representative record at the specified index and then builds a new tree and calculates
the accuracy of that tree and prints it out.
'''   
def leave_one_out_cross_validation(root, data, reps, i):
    
    deleted = reps.pop(i)
    
    decisionTreeMaker(data, root, None)
    
    acc = accuracy(root, reps)
    print("Left out Representative",deleted.id, "Accuracy:",acc)
    
    reps.insert(i, deleted)
  
'''
This function takes a tree and list of representatives and returns the accuracy of that
tree on the list of representatives given.
'''
def accuracy(node, representatives):
    
    root = node # get root and save in root
    totalData = len(representatives)
    count = 0
    
    # iterate through each representative
    for i, rep in enumerate(representatives):

        votes = rep.votes   # get votes
        index = 0           # maintain index of votes
        node = root
        
        # loop through each node until it's a leaf
        while node.leaf is False:
            theVote = votes[index]
            
            # loop through each node's children & if 
            for child in node.children:
                if child.vote == theVote:
                    node = child
                    break
            index += 1
        if node.label == rep.party:
            count += 1
    
    return count/totalData

###########################################################
##################     MAIN FUNCTION   ####################
###########################################################
def main():
    data, tuneData = makeMatrix('voting-data.tsv')
    representative = []
    for i, elem in enumerate(data):
        newRep = Representative(elem[0], elem[1], elem[2])
        representative.append(newRep)

    # BUILD AND PRINT TREE ON TRAINING SET
    treeRoot = Node()
    decisionTreeMaker(data, treeRoot, None)
    print("THE TREE BEFORE PRUNING: ")
    printTree(treeRoot)
    print()
    
    # BUILD AND PRINT TREE AFTER PRUNING
    newRoot = completelyPruned(treeRoot, tuneData)
    print("THE PRUNED TREE: ")
    printTree(newRoot)
    
    # ESTIMATE TREE'S ACCURACY ON TESTING SET
    for i, elem in enumerate(tuneData):
        leave_one_out_cross_validation(newRoot, data, representative, i)
    
if __name__ == "__main__":
    main()