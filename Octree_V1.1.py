""" 
OCTREE version 1.0

DESCRIPTION:

    This python code is used to build an Octree - 3D hierachical spatial tree data structure.
    The background of this code is based on recursive divide & conquer algorithm to insert 
    and find nodes in the octree. It can store any type of object you create, so long as that 
    object has a 'position' property in the form of a 3-vector tuple.

    It also include a test function which create a random number of 3D points to put into the 
    tree. Besides, another function is utilized to detect the collision (this function create 
    a number of random point and find which points of the tree located in the same node with 
    each random point input)

NOTES:

    The OctNode positions do not correspond to any object position rather they are seperate 
    containers which may contain objects or other nodes.
     
    An OctNode which which holds less objects than MAX_OBJECTS_PER_CUBE is a LeafNode; 
    it has no branches, but holds a list of objects contained within its boundaries. 
    The list of objects is held in the leafNode's 'data' property.
     
    If more objects are added to an OctNode, taking the object count over MAX_OBJECTS_PER_CUBE
    Then the cube has to subdivide itself, and arrange its objects in the new child nodes.
    The new octNode itself contains no objects, but its children should.
    
    The worldSize of Octree must larger at least 2 times of the maximum size of points in dataset  
 
CLASSES:

    - OctNode(position, size, objects): create the OctNode with centroid position, size of 
                                        node and input data.
    - Octree(worldSize): create an Octree with the bounding size (worldSize).

AUTHOR:

    Copyright(c) and written by Van Hung Cao
    Affiliation: School of Computer Sciences and Informatics - University College Dublin
    Created day: May 22, 2015

LICENSE:

    Released under GNU General Public License (GPL)

UPDATE:
    Version v1.0
   
"""
#### Global Variables ####
 
# This defines the maximum objects an LeafNode can hold, before it gets subdivided again.
MAX_OBJECTS_PER_CUBE = 5

# This dictionary is used by the findBranch function, to return the correct branch index
DIRLOOKUP = {-4:"right up forward", -3:"right up back", -2:"right down forwards", -1:"right down back", 0:"left up forward", 1:"left up back", 2:"left down forwards", 3:"left down back"}

#### End Globals ####

class OctNode:
    # New Octnode Class, can be appended to as well 
    def __init__(self, position, size, data):
        # OctNode Cubes have a centroid position and size
        # position is related to, but not the same as the objects the node contains.
        self.position = position
        self.size = size

        # All OctNodes will be leaf nodes at first
        # Then subdivided later as more objects get added
        self.isLeafNode = True

        # store our object, typically this will be one, but maybe more
        self.data = data
        
        # It also have 8 empty branches while we are here.
        self.branches = [None, None, None, None, None, None, None, None]

        # The cube's bounding coordinates -- Not currently used
        self.ldb = (position[0] - (size / 2), position[1] - (size / 2), position[2] - (size / 2))
        self.ruf = (position[0] + (size / 2), position[1] + (size / 2), position[2] + (size / 2))
        

class Octree:
    def __init__(self, worldSize):
        # Init the world bounding root cube
        # all world geometry is inside this
        # it will first be created as a leaf node (ie, without branches)
        # this is because it has no objects, which is less than MAX_OBJECTS_PER_CUBE
        # if we insert more objects into it than MAX_OBJECTS_PER_CUBE, 
        # then it will subdivide itself.
        self.root = self.addNode((0,0,0), worldSize, [])
        self.worldSize = worldSize

    def addNode(self, position, size, objects):
        # This creates the actual OctNode itself.
        return OctNode(position, size, objects)

    def insertNode(self, root, size, parent, objData):
        # This function is used to insert new Node to the tree
        if root == None:
            # we're inserting a single object, so if we reach an empty node, insert it here
            # Our new node will be a leaf with one object, our object
            # More may be added later, or the node maybe subdivided if too many are added
            # Find the Real Geometric centre point of our new node:
            # Found from the position of the parent node supplied in the arguments
            pos = parent.position
            # offset is halfway across the size allocated for this node
            offset = size / 2
            # find out which direction we're heading in
            branch = self.findBranch(parent, objData.position)
            
            newCenter = (0,0,0)
            if branch == -4:
                # right up forward
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] + offset )

            elif branch == -3:
                # right up back
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
            
            elif branch == -2:
                # right down forwards
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
            
            elif branch == -1:
                # right down back
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )
    
            elif branch == 0:
                # left up forward
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
            
            elif branch == 1:
                # left up back
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )
            
            elif branch == 2:
                # left down forwards
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
         
            elif branch == 3:
                # left down back
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
                          
            # Now we know the centre point of the new node
            # we already know the size as supplied by the parent node
            # So create a new node at this position in the tree
            
            #print "Adding Node of size: " + str(size / 2) + " at " + str(newCenter)
            sub_cube =DIRLOOKUP[branch]
            #print the centroid position of parent node, the branch of sub node, (the 
            #position of sub cube) and the point position in sub cube.
            print 'Cube: ',newCenter,' branch: ',branch+4, sub_cube,"=>", 'point position:', objData.position 
            
            
            return self.addNode(newCenter, size, [objData])
        
        #else: are we not at our position, but not at a leaf node either
        elif root.position != objData.position and root.isLeafNode == False:
            
            # we're in an octNode still, we need to traverse further
            branch = self.findBranch(root, objData.position)
            # Find the new scale we working with
            newSize = root.size / 2
            # Perform the same operation on the appropriate branch recursively
            root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, objData)
        # else, is this node a leaf node with objects already in it?
        elif root.isLeafNode:
            # We've reached a leaf node. This has no branches yet, but does hold
            # some objects, at the moment, this has to be less objects than MAX_OBJECTS_PER_CUBE
            # otherwise this would not be a leafNode.
            # if we add the node to this branch will we be over the limit?
            if len(root.data) < MAX_OBJECTS_PER_CUBE:
                # No? then Add to the Node's list of objects and we're done
                root.data.append(objData)
                #print root.position, objData.position
                #return root
            elif len(root.data) == MAX_OBJECTS_PER_CUBE:
                # Adding this object to this leaf takes us over the limit
                # So we have to subdivide the leaf and redistribute the objects
                # on the new children. 
                # Add the new object to pre-existing list
                root.data.append(objData)
                # copy the list
                objList = root.data
                # Clear this node's data
                root.data = None
                # Its not a leaf node anymore
                root.isLeafNode = False
                # Calculate the size of the new children
                newSize = root.size / 2
                # distribute the objects on the new tree
                print "\nSubdividing Node sized at: " + str(root.size) + " Centroid of node at coords: " + str(root.position)
                for ob in objList:
                    branch = self.findBranch(root, ob.position)
                    root.branches[branch] = self.insertNode(root.branches[branch], newSize, root, ob)
        return root

    def findPosition(self, root, position):
        # Basic collision lookup that finds the leaf node containing the specified position
        # Returns the child objects of the leaf, or None if the leaf is empty or none
        if root == None:
            return None
        elif root.isLeafNode:
            return root.data
        else:
            branch = self.findBranch(root, position)
            return self.findPosition(root.branches[branch], position)
    
    def findParent(self, root, position):
        # This function will tell us the location of parent of a point which we checking out
        # Returns the position of the parent of the node, or None if the leaf is empty or none
        if root == None:
            return None
        elif root.isLeafNode:
            return root.position
        else:
            branch = self.findBranch(root, position)
            return self.findParent(root.branches[branch], position)
        
    def printLeafNode(self, root):
        # Basic collision lookup that finds the leaf node containing the specified position
        # Returns the child objects of the leaf, or None if the leaf is empty or none
        global LEAFNODE_POINTS_ARRAY, LEAFNODE_PARENT_LOCATION_ARRAY
        
        if root == None:
            return None
        elif root.isLeafNode:
#             print 'Leafnode position:',root.position
#             for i in root.data:
#                 print i.name, i.position,
#             print "\n"
            
            LEAFNODE_POINTS_ARRAY.append(root.data)
            LEAFNODE_PARENT_LOCATION_ARRAY.append(root.position)
            #return root.data
        else:
            branch = -4
            while branch<=3:
                self.printLeafNode(root.branches[branch])
                branch=branch+1

    def findBranch(self, root, position):
        # This function help us to find the branch for new node,
        # returns an index corresponding to a branch
        # pointing in the direction we want to go
        vec1 = root.position
        vec2 = position
        result = 0
        # Equation created by adding nodes with known branch directions
        # into the tree, and comparing results.
        # See DIRLOOKUP above for the corresponding return values and branch indices
        for i in range(3):
            if vec1[i] <= vec2[i]:
                result += (-4 / (i + 1) / 2)
            else:
                result += (4 / (i + 1) / 2)
        return result
    
## We done with Octree class.
## ---------------------------------------------------------------------------------------------------##

## Now we can test our tree data structure. 
if __name__ == "__main__":

    ### Object Insertion Test ###
    
    # So lets test the adding:
    import random
    import time

    #Dummy object class to test with
    class TestObject:
        def __init__(self, name, position):
            self.name = name
            self.position = position

    # Create a new octree, size of world
    myTree = Octree(90.0000)

    # Number of objects we intend to add.
    NUM_TEST_OBJECTS = 100

    # Number of collisions we're going to test
    NUM_COLLISION_LOOKUPS = 10
    
    # Array of list of points each leaf node
    LEAFNODE_POINTS_ARRAY = []
    
    # Array location of parent of each leaf node
    LEAFNODE_PARENT_LOCATION_ARRAY = []

    # Insert some random objects and time it
    Start = time.time()
    myTree.insertNode(myTree.root, 50.000, myTree.root, TestObject("Point_ID", (1,2,3)))
    myTree.insertNode(myTree.root, 50.000, myTree.root, TestObject("Point_ID", (-5,-5,-5)))
    myTree.insertNode(myTree.root, 50.000, myTree.root, TestObject("Point_ID", (11.25,-11.25,-11.25)))
    for x in range(NUM_TEST_OBJECTS):
        name = "Point_ID_" + str(x)
        pos = (random.randrange(-45.000, 45.000), random.randrange(-45.00, 45.00), random.randrange(-45.00, 45.00))
        testOb = TestObject(name, pos)
        myTree.insertNode(myTree.root, 50.000, myTree.root, testOb)
    End = time.time() - Start

    # print some results.
    print str(NUM_TEST_OBJECTS) + "-Node Tree Generated in " + str(End) + " Seconds"
    print "Tree Leaves contain a maximum of " + str(MAX_OBJECTS_PER_CUBE) + " objects each."
    
    print myTree.findParent(myTree.root,(1,2,3))
    print myTree.findParent(myTree.root,(-5,-5,-5))
    print myTree.findParent(myTree.root,(11.25,-11.25,-11.25))
    result = myTree.findPosition(myTree.root,(11.25,11.25,11.25))
    if result != None:
            for i in result:
                print i.name, i.position,
            print
    result = myTree.findPosition(myTree.root,(1,2,3))
    if result != None:
            for i in result:
                print i.name, i.position,
            print
    
    
    result1 = myTree.printLeafNode(myTree.root)
   
    for i in range(len(LEAFNODE_POINTS_ARRAY)):
        print "\n", LEAFNODE_PARENT_LOCATION_ARRAY[i], "=>"
        for j in LEAFNODE_POINTS_ARRAY[i]:
            print j.name, j.position,
        print

    
    
    """
    ### Lookup Tests ###
    
    # Look up some random positions and time it
    Start = time.time()
    for x in range(NUM_COLLISION_LOOKUPS):
        pos = (random.randrange(-45.000, 45.000), random.randrange(-45.00, 45.00), random.randrange(-45.00, 45.00))
        result = myTree.findPosition(myTree.root, pos)
        print "Results for test at: " + str(pos)
        if result != None:
            for i in result:
                print i.name, i.position,
            print
        
        ##################################################################################
        # This proves that results are being returned - but may result in a large printout
        #print "Results for test at: " + str(pos)
        #if result != None:
        #    for i in result:
        #        print i.name, i.position,
        #print
        ##################################################################################
        
    End = time.time() - Start

    # print some results.
    print str(NUM_COLLISION_LOOKUPS) + " Collision Lookups performed in " + str(End) + " Seconds"
    print "Tree Leaves contain a maximum of " + str(MAX_OBJECTS_PER_CUBE) + " objects each."
    """
    x = raw_input("Press any key to exit:")
