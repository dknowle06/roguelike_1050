"""
Two Classes that are used to create a Tree, since Python apparently doesn't have built in support?
My implementation allows any node to have an unlimited number of parents and an unlimited number of children
This could create some funky looking tree maps, but it will be useful for my game
I think more accurately this would be described as a graph, but I'm not sure if that's accurate either
IDK I just made a data structure that works for what I need

When iterating through this data structure, you can only go forward

This only works because Python objects are stored by reference instead of by value,
otherwise Python's lack of pointers would make this impossible 
"""

class Node:
    """
    `data` stores whatever the value of this node is 
    `children` stores which nodes this node points to
    `node_id` stores the id of the node, should be identical to the key in dictionary in the tree
    """

    # if this is true, printing a node will display some more debug info. otherwise, it will just display the node's data
    TESTING = True

    def __init__(self, data = None, node_id:int = 0, children:list = []):
        self.data = data
        self.children = list(children) # copies the list instead of referencing it 
        self.node_id = node_id

    # `*args` should all be `Node`
    def add_child(self, child) -> None:
        self.children.append(child)

    # returns whatever type of `self.data` is
    def get_data(self):
        return self.data

    # returns the id of the node
    def get_id(self) -> int:
        return self.node_id

    def get_children(self) -> list:
        return self.children

    def get_children_ids(self) -> list:
        temp = []

        for child in self.children:
            temp.append(child.get_id())

        return temp
    
    def __str__(self) -> str:
        # i love the ternary operator :)

        # creates an array to be printed during testing
        temp = []

        # only sets up the array values if `self.TESTING` is true
        if self.TESTING:

            for child in self.children:
                temp.append(f"{child.get_id()}:{child.get_data()}")

        return f"{self.data}, {type(self.data)}, # of children = {len(self.children)}, {temp}, id = {self.node_id}" if self.TESTING else f"{self.data}"

class Tree:
    """
    `parent_dictionary` stores id/node pairs
    `num_nodes` stores the amount of nodes currently in the tree
    `head` stores the first node 
    """

    # `head_data` can be any type
    # the root's id will always be 1 !!!!
    def __init__(self, head_data = None):
        self.parent_dictionary = {}
        self.num_nodes = 0

        self.head = Node(head_data, 0)

        self.parent_dictionary[self.num_nodes] = self.head

    # parents should be a list of ints
    # allows 2 nodes to lead to a single node
    # i don't think this is usually in tree implementations, but it will be useful for me 
    def add_node(self, node_data, parents:list = [0]) -> None:
        self.num_nodes += 1

        # not really temporary but only referenced in this method
        temp_node = Node(node_data, self.num_nodes)

        self.parent_dictionary[self.num_nodes] = temp_node

        for parent in parents:
            self.parent_dictionary[parent].add_child(temp_node)

    # returns a `Node`
    def get_node_from_id(self, node_id:int = 0):
        return self.parent_dictionary[node_id]

    # returns the number of nodes when `len(foo)` is called
    # adds 1 since the nodes are 0-indexed 
    def __len__(self) -> int:
        return self.num_nodes + 1

    # printing used during tested
    # shouldn't actually be called in a playable build
    # will write a seperate function to render generated maps into ascii
    def __str__(self) -> str:
        temp = ""

        for i in range(len(self)):
            temp += str(self.get_node_from_id(i)) + "\n"

        # returns string without the last linebreak
        return temp[:-1]