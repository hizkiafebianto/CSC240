# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 11:59:07 2016

@author: Hizkia
Description: Python Implementation of the FP-growth Algorithm
This code implements an fp-growth algorithm to find interesting 
patterns in a census data set retrieved from the following link:
http://archive.ics.uci.edu/ml/datasets/Adult

"""
# LIBRARIES
from collections import defaultdict, namedtuple
import urllib2
import datetime

##################################################################
# TREE STRUCTURE
##################################################################

# The implementation of FPTree and FPNode class is taken from the 
# following link https://github.com/enaeseth/python-fp-growth

class FPNode(object):
    """A node in an FP tree."""

    def __init__(self, tree, item, count=1):
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    def add(self, child):
        """Add the given FPNode `child` as a child of this node."""

        if not isinstance(child, FPNode):
            raise TypeError("Can only add other FPNodes as children")

        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self

    def search(self, item):
        """
        Check whether this node contains a child node for the given item.
        If so, that node is returned; otherwise, `None` is returned.
        """
        try:
            return self._children[item]
        except KeyError:
            return None

    def __contains__(self, item):
        return item in self._children
        
    @property
    def root(self):
        """True if this node is the root of a tree; false if otherwise."""
        return self._item is None and self._count is None
        
    @property
    def item(self):
        """The item contained in this node."""
        return self._item
        
    @property
    def tree(self):
        """The tree in which this node appears."""
        return self._tree

    @property
    def item(self):
        """The item contained in this node."""
        return self._item

    @property
    def count(self):
        """The count associated with this node's item."""
        return self._count
    
    def increment(self):
        """Increment the count associated with this node's item."""
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1
    
    @property
    def parent(self):
        """The node's parent"""
        return self._parent

    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a parent.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a parent from another tree.")
        self._parent = value

    @property
    def neighbor(self):
        """
        The node's neighbor; the one with the same value that is "to the right"
        of it in the tree.
        """
        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a neighbor.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a neighbor from another tree.")
        self._neighbor = value

    @property
    def children(self):
        """The nodes that are children of this node."""
        return tuple(self._children.itervalues())


class FPTree(object):
    """
    An FP tree.

    This object may only store transaction items that are hashable
    (i.e., all items must be valid as dictionary keys or set members).
    """

    Links = namedtuple('Links', 'head tail')

    def __init__(self):
        # The root node of the tree.
        self._root = FPNode(self, None, None)

        # A dictionary mapping items to the head and tail of a path of
        # "neighbors" that will hit every node containing that item.
        self._links = {}

    @property
    def root(self):
        """The root node of the tree."""
        return self._root

    def add(self, transaction):
        """Add a transaction to the tree."""
        point = self._root

        for item in transaction:
            next_point = point.search(item)
            if next_point:
                # There is already a node in this tree for the current
                # transaction item; reuse it.
                next_point.increment()
            else:
                # Create a new point and add it as a child of the point we're
                # currently looking at.
                next_point = FPNode(self, item)
                point.add(next_point)

                # Update the route of nodes that contain this item to include
                # our new node.
                self._update_links(next_point)

            point = next_point

    def _update_links(self, point):
        """Add the given node to the route through all nodes for its item."""
        assert self is point.tree

        try:
            link = self._links[point.item]
            link[1].neighbor = point 
            self._links[point.item] = self.Links(link[0], point)
        except KeyError:
            # First node for this item; start a new route.
            self._links[point.item] = self.Links(point, point)

    def items(self):
        """
        Generate one 2-tuples for each item represented in the tree. The first
        element of the tuple is the item itself, and the second element is a
        generator that will yield the nodes in the tree that belong to the item.
        """
        for item in self._links.iterkeys():
            yield (item, self.nodes(item))

    def nodes(self, item):
        """
        Generate the sequence of nodes that contain the given item.
        """

        try:
            node = self._links[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
        """Generate the prefix paths that end with the given item."""

        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))


##################################################################
# SUPPORTING FUNCTIONS
##################################################################
def age_bins(age):
    '''Return the category of input age. 
       Return missing value as it is
    '''
    try:
        int(age)
    except ValueError:
        return age
    else:
        if int(age) < 45:
            return 'young-adult'
        elif 45 <= int(age) <= 65:
            return 'middle-age'
        elif int(age) > 65:
            return 'senior'
    
def caploss_bins(cap_loss):
    '''Return the category of capital loss. 
       Return missing value as it is
    '''
    try:
        int(cap_loss)
    except ValueError:
        return cap_loss
    else:
        if int(cap_loss) == 0:
            return '$0'
        elif 1 <= int(cap_loss) <= 1700:
            return '$1-$1700'
        elif 1701 <= int(cap_loss) > 2000:
            return '$1701-$2000'
        elif int(cap_loss) > 2000:
            return '>2000'

def capgain_bins(cap_gain):
    '''Return the category of capital gain. 
       Return missing value as it is
    '''
    try:
        int(cap_gain)
    except ValueError:
        return cap_gain
    else:
        if int(cap_gain) == 0:
            return '$0'
        elif 1 <= int(cap_gain) <= 4000:
            return '$1-$4000'
        elif 4001 <= int(cap_gain) > 7700:
            return '$4001-$7700'
        elif int(cap_gain) > 7700:
            return '>7700'

def workhour_bins(workhour):
    '''Return the category of workhour. 
       Return missing value as it is
    '''
    try:
        int(workhour)
    except ValueError:
        return workhour
    else:
        if int(workhour) == 40:
            return 'full-time'
        elif int(workhour) < 40:
            return 'part-time'
        elif int(workhour) > 40:
            return 'overtime'

def fp_growth(tree, suffix, min_sup, T):
    for item, nodes in tree.items():
        support = sum(n.count for n in nodes)
        if support >= (min_sup*len(T)) and item not in suffix:
            beta = [item] + suffix
            yield (beta, support)
            cond_tree = conditional_fptree(tree.prefix_paths(item))
            for s in fp_growth(cond_tree, beta, min_sup, T):
                yield s
            
def conditional_fptree(paths):
    """ Build a conditional FPTree"""    
    tree = FPTree()
    suffix_item = None
    
    for path in paths:
        if suffix_item is None:
            suffix_item = path[-1].item
        
        point = tree.root        
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                if node.item == suffix_item:
                    count = node.count
                else: 
                    count = 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_links(next_point)
            point = next_point
    assert suffix_item is not None
    for path in tree.prefix_paths(suffix_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count        
    return tree

##################################################################
# DATA PROCESSING
##################################################################
# Load data into the program and discretize quantitative         #
# attributes                                                     #
##################################################################

data_url = "https://raw.githubusercontent.com/hizkiafebianto/CSC240/master/Project%201/Apriori/adult.data"
raw_data = []
f = urllib2.urlopen(data_url) # create connection with the URL
for line in f.readlines():
    temp = []    
    for item in line.split(','): # split each line by comma
        temp.append(item.strip()) # strip whitespace from each item
    raw_data.append(temp)
del raw_data[len(raw_data)-1]

# Remove records with cap_gain = 99999 and calculate missing values. 
data = []
missing_val = 0
for item in raw_data:
    if int(item[10]) != 99999:
        data.append(item[:])
    if '?' in item:
        missing_val += 1;

# Discretize continuous attributes: age, capital-gain, capital-loss,
# and hours-per-week. Remove insignificant attributes: fnlwgt and 
# education-num. 
data1 = [] 
for row in data:
    temp = row[:]
    # Discretize age
    temp[0] = age_bins(row[0])
    # Discretize capital gain
    temp[10] = capgain_bins(row[10])
    # Discretize capital loss
    temp[11] = caploss_bins(row[11])
    # Discretize workhour
    temp[12] = workhour_bins(row[12])
    # Delete education_num
    del temp[4]
    # Delete fnlwgt
    del temp[2]
    data1.append(temp)

keys = ['age','workclass','education','marital','occupation',\
'relationsip','race','sex','gain','loss','hours','country','salary']

##################################################################
# APRIORI IMPLEMENTATION
##################################################################
# Prompts user for minimum support and minimum confidence
min_sup = input("Input minimum support [0..1]= ")
min_conf = input("Input minimum confidence [0..1]= ")
print "Processing... \n"

# Record start time 
start = datetime.datetime.now()

# Build the transaction database
# Each row in the data set will be treated as a transaction
transactions = []
for row in data1:
    temp = []
    for i, item in enumerate(row):   
        temp.append('%s=%s'%(keys[i],item))
    transactions.append(temp)

# Scan the transaction database D once and collect the set of 
# frequent items and their support counts.
freq_items = defaultdict(int)
for transaction in transactions:
    for item in transaction:
        freq_items[item] += 1
        
# Remove infrequent items
for item, f in freq_items.items():
    if float(f)/len(transactions) < min_sup:
        del freq_items[item]   

# Sorted each transaction in T according to the order of freq_items and 
#insert the transaction into an FPTree
Tree = FPTree()
for transaction in transactions:
    temp = []
    for item in transaction:
        if item in freq_items.keys():
            temp.append(item)
    temp.sort(key=lambda x: freq_items[x],reverse = True)
    Tree.add(temp)

# Mining the tree
freq_patterns = defaultdict(int)
for itemset, sup in fp_growth(Tree,[],min_sup,transactions):
    freq_patterns[frozenset(itemset)] = sup

# Record finish time
finish = datetime.datetime.now()

# Show results
print "List of frequent patterns:"
for item, f in freq_patterns.items():
    print "{}, support: {}\n".format(list(item),f)

# Showing time spent
print "The operation took {}.".format(finish-start)
print
print

##################################################################
# A TEST USING TRANSACTION DATA FROM THE TEXTBOOK
##################################################################

print "#######################################################\n"
print "### A TEST USING TRANSACTION DATA FROM THE TEXTBOOK ###\n"
print "#######################################################\n"

T = [['I1','I2','I5'],['I2','I4'],['I2','I3'],['I1','I2','I4'],\
['I1','I3'],['I2','I3'], ['I1','I3'],['I1','I2','I3','I5'],['I1','I2','I3']]

print "T = {0}\n".format(T)

# minimum support
ms = float(2)/9
# minimum confidence
mc = 0.7

f_items = defaultdict(int)

# Generate list of items
for t in T:
    for item in t:
        f_items[item] += 1

# Remove infrequent items
for item, f in f_items.items():
    if float(f)/len(T) < ms:
        del f_items[item]

# Sorted each transaction in T according to the order of f_items and insert
# the transaction into an FPTree
Tree = FPTree()
for t in T:
    temp = []
    for item in t:
        if item in f_items.keys():
            temp.append(item)
    temp.sort(key=lambda x: f_items[x], reverse=True)
    Tree.add(temp)

# Mining the tree
freq_patterns = defaultdict(int) # freq patterns and their supports
for itemset, sup in fp_growth(Tree, [], ms, T):
    freq_patterns[frozenset(itemset)] = sup
    


#x = Tree._links['I4'][0]
#while x.neighbor <> None:
#    print "{}:{}".format(x.parent.item, x.parent.count)
#    x = x.neighbor
#print "{}:{}".format(x.parent.item, x.parent.count)