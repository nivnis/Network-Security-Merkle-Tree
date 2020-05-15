# Niv Haim Nisani, 206904021, Yuval Levy, 205781966
from hashlib import sha256
import math
# This class is the a structure of the nodes we will have in our Merkel tree.
# The min and max represents the most left node and the most right node in the tree, that our node is the root in.


class Node:
    def __init__(self, data, l_son, r_son, minimum, maximum):
        self.data = data  # Assign data
        self.father = None  # Initialize next as null
        self.left_son = l_son
        self.right_son = r_son
        self.min = minimum
        self.max = maximum


# This func creates a new node for our tree.
def createNode(str, l_son, r_son, min_index, max_index):
    node = Node(str, l_son, r_son, min_index, max_index)
    return node


# This func get a list of strings, returns a list of nodes.
def createLeafNodes(input_list):
    leafArray = []
    for i in range(1, len(input_list)):
        leafArray.append(createNode(input_list[i], None, None, i - 1, i - 1))
    return leafArray


# This func get a list of nodes, and creates the Merkel tree out of it.
def buildMerkleTree(leaf_list):
    # if the list is 1 node then this node is the root.
    if len(leaf_list) is 1:
        return leaf_list[0]
    father_List = []
    # loop with jumps of 2 each time.
    for i in range(0, len(leaf_list), 2):
        # take the data of 2 nodes and create one of of them.
        mixedString = str(leaf_list[i].data + leaf_list[i+1].data)
        # Use hash on the new string.
        hashedString = sha256(mixedString.encode())
        # Create the father node out of the 2 nodes.
        father_node = createNode(hashedString.hexdigest(),
                                 leaf_list[i], leaf_list[i + 1], leaf_list[i].min, leaf_list[i + 1].max)
        # Add the father node to the list.
        leaf_list[i].father = father_node
        leaf_list[i + 1].father = father_node
        father_List.append(father_node)
    # Get back from the func the Merkel tree.
    root = buildMerkleTree(father_List)
    return root


# This func return the proof of inclusion of a specific index of our tree.
def proofOfInclusion(r, treeDepth, requiredIndex):
    retString = ""
    proofList = []
    currNode = r
    for i in range(0, treeDepth + 1):
        # Check if the node that we are checking, its min == max. If so then we found our node that we need, and
        # we can go back and start returning nodes to out proof of inclusion.
        if currNode.min == requiredIndex and currNode.max == requiredIndex:
            # loop over our proof of inclusion list from the end to the beginning.
            for j in range(len(proofList) - 1, -1, -1):
                # Print the data and if the node was "left" or "right" in the proof of inclusion.
                retString = retString + proofList[j][0] + " "
                retString = retString + proofList[j][1].data + " "
            retString = retString[:-1]
            print(retString)

            return
        # If we got to the leaf level of the tree and did not find our node index, then its an error and need to exit.
        if i == treeDepth:
            exit(1)
        # Check if the right son of node that we are checking, its min is bigger then our index. If so then add the
        # right son to our proof of inclusion list and continue with the left son.
        if requiredIndex < currNode.right_son.min:
            proofList.append(('r', currNode.right_son))
            currNode = currNode.left_son
        # Add the left son to our proof of inclusion list and continue with the right son.
        else:
            proofList.append(('l', currNode.left_son))
            currNode = currNode.right_son


root = None
depth = 0
leafList = []
while True:
    msg = input()
    inputList = msg.split(' ')
    command = inputList[0]
    # First command - create a Merkel tree out of the input.
    if command is '1':
        # If the amount of leafs that we got is not a power of 2, the the tree will not be complete. Just exit.
        depth = int(math.log2(len(inputList)))
        # Get a list of nodes out of the list of strings.
        leafList = createLeafNodes(inputList)
        # Check if we got power of 2 leafs.
        checkListLen = len(leafList)
        num = math.log(checkListLen, 2).is_integer()
        if num is False:
            exit(1)
        # Get a root of the Merkel tree out of nodes.
        root = buildMerkleTree(leafList)
        print(root.data)
    # Second command - get a proof of inclusion of an index in our tree.
    elif command is '2':
        # Check we got only 1 index and its a number.
        if len(inputList) != 2 or root is None or not(inputList[1].isdigit()):
            exit(1)
        requiredLeafIndex = int(inputList[1])
        # Check that we got a correct index.
        if requiredLeafIndex >= len(leafList) or requiredLeafIndex < 0:
            exit(1)
        # Get the proof of inclusion.
        proofOfInclusion(root, depth, requiredLeafIndex)
    # Third command - Check that the proof of inclusion that the user gave us is correct.
    elif command is '3':
        # Check that the amount of args that we got is enough for a correct proof of inclusion.
        if len(inputList) < 5 or len(inputList) % 2 == 0:
            exit(1)
        proof = []
        mixedString = ""
        parentHash = ""
        requiredLeaf = inputList[1]
        rootHash = inputList[2]
        # create a proof of inclusion pair list
        for i in range(3, len(inputList), 2):
            # Create pair and add it to the list.
            proof.append((inputList[i], inputList[i + 1]))
        # If the second index in the pair is "l" then we need add the other nodes data from the right to our first node.
        if proof[0][0] == 'l':
            mixedString = str(proof[0][1] + requiredLeaf)
        # If the second index in the pair is "r" then we need add the other nodes data from the left to our first node.
        elif proof[0][0] == 'r':
            mixedString = str(requiredLeaf + proof[0][1])
        # If the second index in the pair is not "l" or "r", then the input is in correct.
        else:
            exit(1)
        # Create the hash out of the string that we created.
        parentHash = sha256(mixedString.encode()).hexdigest()
        # Now loop until we get to the height of the Merkel tree.
        for j in range(1, len(proof)):
            # If the second index in the pair is "l" then we need add the other nodes data from the right to our
            # first node.
            if proof[j][0] == 'l':
                mixedString = str(proof[j][1] + parentHash)
            # If the second index in the pair is "r" then we need add the other nodes data from the left to our
            # first node.
            elif proof[j][0] == 'r':
                mixedString = str(parentHash + proof[j][1])
            # If the second index in the pair is not "l" or "r", then the input is in correct.
            else:
                exit(1)
            parentHash = sha256(mixedString.encode()).hexdigest()
        # Check if the hashed root that we got is the same as the one we got from the user.
        if parentHash == rootHash:
            print(True)
        else:
            print(False)
    # Forth command - get the difficulty of the amount of "0" that we need to find in the hashed node.
    elif command is '4':
        # Check if the input is valid.
        if len(inputList) != 2 or root is None or not(inputList[1].isdigit()) or inputList[1] == '0':
            exit(1)
        # if root is None:
        #     exit(1)
        numOfZeros = int(inputList[1])
        zeroString = ""
        # create a string that has the mount of zeros that we need.
        for j in range(0, numOfZeros):
            zeroString = zeroString + '0'
        i = 0
        hashedString = ""
        # Loop until we got a hashed string that has the amount of zeros that we need.
        while True:
            mixedString = str(str(i) + root.data)
            hashedString = sha256(mixedString.encode()).hexdigest()
            # Check if the new hashed string has the amount of zeros.
            if hashedString[:numOfZeros] == zeroString:
                print(i, end=' ')
                print(hashedString)
                break
            i = i + 1
    # Fifth command - exit.
    elif command is '5':
        break
    # Unsupported command.
    else:
        break
exit(1)
