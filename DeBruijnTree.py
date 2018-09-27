#Vocany Pitia
#CSCE 4430
#Assignment 2

import graphviz

#Graphviz graph object do display the tree
dot = graphviz.Digraph(comment="DeBruijn Tree")

#Class defining what a node is within the tree
class TreeNode:
    def __init__(self, value, parent, left, middle, right):
        self.value = value              #The value of the node (l,a, or 0-9)
        self.parent = parent            #The parent node of the node, for traversal
        self.left = left                #The left child
        self.middle = middle            #The middle child
        self.right = right              #the right child
        self.root = False               #Boolean flag to determine if this is the root node
        self.pnum = 0                   #Identifier for its parent node, for graph output
        self.cnum = 0                   #Identifier for its child node, for graph output

#Prints the tree using graphviz and in dot format
def printTree(root):
    dot.node(str(root.value)+str(root.cnum),str(root.value))
    if(root.left != None):
        #Creates the edge between the parent node and its left child
        dot.edge(str(root.value)+str(root.cnum),str(root.left.value)+str(root.left.cnum))
        printTree(root.left)
    if(root.middle != None):
        # Creates the edge between the parent node and its middle child
        dot.edge(str(root.value) + str(root.cnum), str(root.middle.value) + str(root.middle.cnum))
        printTree(root.middle)
    if(root.right != None):
        # Creates the edge between the parent node and its right child
        dot.edge(str(root.value) + str(root.cnum), str(root.right.value) + str(root.right.cnum))
        printTree(root.right)

#Defines the lambda functions
def l(x):
    return ('l',x)

def a(x,y):
    return ('a',x,y)

if __name__ == '__main__':
    #lamb is the variable that holds the DeBruijn lambda function to be parsed
    lamb = l(a(a(1,a(l(l(0)),1)),1))
    stri = (["".join(str(x) for x in lamb)][0])             #converts lamb into a string to make parsing easier

    #finList will hold each individual element of the stri string
    finList = []
    finList.append('(')
    for item in stri:
        if item not in [',', '\'', ' ']:
            finList.append(item)

    stack = []                                          #This stack will keep track of the parent nodes
    LTree = TreeNode(None,None,None,None,None)          #The root node
    LTree.root = True
    currentNode = LTree
    counter = 1                                         #Unique identifier for nodes when creating the tree
    for token in finList:
        counter += 1
        if token == '(' and currentNode.value == 'a':
            currentNode.right = TreeNode(None,None,None,None,None)
            currentNode.right.pnum = currentNode.cnum
            currentNode.right.cnum = counter
            stack.append(currentNode)
            currentNode = currentNode.right
        elif token == '(' and (currentNode.root == False or currentNode.root == True):
            continue
        elif token == '(' and currentNode.root == None:
            continue
        elif token in ['l','a']:
            if token == 'l':
                currentNode.value = 'l'
                currentNode.middle = TreeNode(None,None,None,None,None)
                currentNode.middle.pnum = currentNode.cnum
                currentNode.middle.cnum = counter
                #if(stack == [] or currentNode.root != True):
                stack.append(currentNode)
                currentNode = currentNode.middle
            else:
                currentNode.value = 'a'
                currentNode.left = TreeNode(None,None,None,None,None)
                currentNode.left.pnum = currentNode.cnum
                currentNode.left.cnum = counter
                stack.append(currentNode)
                currentNode = currentNode.left
        elif token.isdigit() == True:
            if currentNode.value != 'a':
                currentNode.value = token
                parent = stack.pop()
                currentNode = parent
            else:
                currentNode.right = TreeNode(None,None,None,None,None)
                currentNode.right.pnum = currentNode.cnum
                currentNode.right.cnum = counter
                stack.append(currentNode)
                currentNode = currentNode.right
                currentNode.value = token
                parent = stack.pop()
                currentNode = parent
        elif token == ')':
            currentNode = stack.pop()
        else:
            print("Error")

    printTree(LTree)            #Calling the printTree() function to create the tree
    print(dot.source)           #Creates the dot format of the tree for graphical representation
    dot.render('output.gv', view=True)