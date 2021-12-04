"""Red and black tree algorithm
    Written by Jakob Adamsson
Explenations of the different cases may be seen in the course book"""

# IMPORTS
import random

# GLOBAL VARS
BLACK = 'BLACK'
RED = 'RED'


class Node():
    """Make Nodes"""

    def __init__(self, value=None):
        self._parent = None
        self._left_node = None
        self._right_node = None
        self._value = value
        self._color = RED

    @property
    def parent(self):
        """Getter method for parent"""
        return self._parent

    @parent.setter
    def parent(self, parent):
        """setter method for parent"""
        self._parent = parent

    @property
    def left(self):
        """Getter method for left node"""
        return self._left_node

    @left.setter
    def left(self, node):
        """setter method for left node"""
        self._left_node = node

    @property
    def right(self):
        """Getter method for left node"""
        return self._right_node

    @right.setter
    def right(self, node):
        """setter method for right node"""
        self._right_node = node

    @property
    def value(self):
        """Getter method for value"""
        return self._value

    @property
    def color(self):
        """Getter method for color"""
        return self._color

    @color.setter
    def color(self, color: str):
        """Setter method for color"""
        self._color = color


class RedBlackTree():
    """Make the tree"""

    def __init__(self):
        self._none_node = Node(None)
        self._none_node._color = BLACK
        self._root = self._none_node

    @property
    def none_node(self):
        """Getter method for none_node"""
        return self._none_node

    @property
    def root(self):
        """Getter method for root"""
        return self._root

    @root.setter
    def root(self, root: Node):
        """Setter method for root"""
        self._root = root

    def inorder_tree_walk(self, node):
        """Walks the tree, visiting each node one time"""
        if node != self.none_node:
            self.inorder_tree_walk(node.left)
            print(node.value, node.color, node.left.value, node.right.value)
            self.inorder_tree_walk(node.right)

    def path(self, key, start_node=None):
        """Returns the path to given value in the tree, in a list"""
        path = []
        # if startnode is None, set it to the root, else go into while loop
        if start_node is None:
            start_node = self.root
            path.append(start_node.value)

        # loop untill we reach the end node, that being a nil node(none_node)
        while start_node != self.none_node:
            if key == start_node.value:
                return path
            if key > start_node.value:
                path.append(start_node.right.value)
                start_node = start_node.right
            if key < start_node.value:
                path.append(start_node.left.value)
                start_node = start_node.left
        return path

    def bfs(self):
        """Searches the tree, breadth first"""
        # start in the root
        root_node = self.root

        # append each visited node into this list
        node_lst = []

        # nodes gets appended to this list, then popped to check next child node
        node_queue = [root_node]
        while len(node_queue) > 0:
            if node_queue != []:
                # grab first node in the queue, check its children
                check_current_node = node_queue.pop(0)
            if check_current_node != self.none_node:
                if check_current_node.value not in node_lst:
                    if check_current_node.left != self.none_node:
                        node_queue.append(check_current_node.left)

                    if check_current_node.right != self.none_node:
                        node_queue.append(check_current_node.right)

                    node_lst.append([check_current_node.value, check_current_node.color,
                                     check_current_node.left.value, check_current_node.right.value])
        return node_lst

    def search(self, key, node=None):
        """Searches for given value"""
        if node is None:
            node = self.root

        if key == node.value:
            return True

        if node is self.none_node:
            return False

        # search for given value by using recurssion
        if node is not None:
            if key < node.value:
                return self.search(key, node.left)
            return self.search(key, node.right)

    def min(self, root=None):
        """Returns the minimum value in the tree"""
        if root is None:
            root = self.root
        min_val = root
        # loop until the the last node in the left subtree has been reached
        # updating var min_val untill we reach it
        while min_val.left != self.none_node:
            min_val = min_val.left
        return min_val.value

    def node_min(self, root=None):
        """Returns the node holding the lowest value in the tree"""
        if root is None:
            root = self.root
        min_node = root
        # loop until the the last node in the left subtree has been reached
        # updating var min_node untill we reach it
        while min_node.left != self.none_node:
            min_node = min_node.left
        return min_node

    def max(self, root=None):
        """Returns the maximum value in the tree"""
        if root is None:
            root = self.root
        max_val = root
        # loop until the the last node in the right subtree has been reached
        # updating var max_val untill we reach it
        while max_val.right != self.none_node:
            max_val = max_val.right
        return max_val.value

    def left_rotate(self, node):
        """Rotates the tree so it keeps the red black tree constraints """
        node2 = node.right
        # rotate node(parameter)'s left subtree into node2's right subtree
        node.right = node2.left
        if node2.left != self.none_node:
            node2.left.parent = node
        # connect node(parameter)'s parent to node2'
        node2.parent = node.parent
        if node.parent == self.none_node:
            self.root = node2
        elif node == node.parent.left:
            node.parent.left = node2
        else:
            node.parent.right = node2
        # move node(parameter) to the left of node2, to maintain correct structure
        node2.left = node
        # since rotated, node(parameter)'s parent needs new value
        node.parent = node2

    def right_rotate(self, node):
        """Rotates the tree so it keeps the red black tree constraints """
        node2 = node.left
        node.left = node2.right
        if node2.right != self.none_node:
            node2.right.parent = node
        node2.parent = node.parent
        if node.parent == self.none_node:
            self.root = node2
        elif node == node.parent.right:
            node.parent.right = node2
        else:
            node.parent.left = node2
        node2.right = node
        node.parent = node2

    def insert(self, new_val):
        """Inserts given value into the tree"""
        # if value already in tree, return
        if self.search(new_val):
            return
        # create new node, containing the wanted value to insert
        node = Node(new_val)
        # y_node and x_node is helper nodes
        y_node = self.none_node
        x_node = self.root
        while x_node != self.none_node:
            y_node = x_node
            if node.value < x_node.value:
                x_node = x_node.left
            else:
                x_node = x_node.right
        node.parent = y_node
        if y_node == self.none_node:
            self.root = node
        elif node.value < y_node.value:
            y_node.left = node
        else:
            y_node.right = node
        # to maintan corrent structure of the tree
        node.left = self.none_node
        node.right = self.none_node
        node.color = RED
        # restore corrent properties of red black tree
        self.insert_fixup(node)

    def insert_fixup(self, node):
        """After insert, it recolors the nodes if needed to keep the structure
        and corrent properties of e red black tree"""
        while node.parent.color == RED:
            if node.parent == node.parent.parent.left:
                y_node = node.parent.parent.right
                if y_node.color == RED:
                    node.parent.color = BLACK  # case 1
                    y_node.color = BLACK  # case 1
                    node.parent.parent.color = RED  # case 1
                    node = node.parent.parent  # case 1
                else:
                    if node == node.parent.right:
                        node = node.parent  # case 2
                        self.left_rotate(node)  # case 2
                    node.parent.color = BLACK  # case 3
                    node.parent.parent.color = RED  # case 3
                    self.right_rotate(node.parent.parent)  # case 3
            else:
                y_node = node.parent.parent.left
                if y_node.color == RED:
                    node.parent.color = BLACK  # case 1
                    y_node.color = BLACK  # case 1
                    node.parent.parent.color = RED  # case 1
                    node = node.parent.parent  # case 1
                else:
                    if node == node.parent.left:
                        node = node.parent  # case 2
                        self.right_rotate(node)  # case 2
                    node.parent.color = BLACK  # case 3
                    node.parent.parent.color = RED  # case 3
                    self.left_rotate(node.parent.parent)  # case 3
        # root shall always be black, corrent if we colored the root red
        self.root.color = BLACK

    def rb_delete_fixup(self, node):
        """After deletion, recolor the nodes and re-assigning nodes"""
        while node != self.root and node.color == BLACK:
            if node == node.parent.left:
                w_node = node.parent.right
                if w_node.color == RED:
                    w_node.color = BLACK  # case 1
                    node.parent.color = RED  # case 1
                    self.left_rotate(node.parent)  # case 1
                    w_node = node.parent.right  # case 1
                if w_node.left.color == BLACK and w_node.right.color == BLACK:
                    w_node.color = RED  # case 2
                    node = node.parent  # case 2
                else:
                    if w_node.right.color == BLACK:
                        w_node.left.color = BLACK  # case 3
                        w_node.color = RED  # case 3
                        self.right_rotate(w_node)  # case 3
                        w_node = node.parent.right  # case 3
                    w_node.color = node.parent.color  # case 4
                    node.parent.color = BLACK  # case 4
                    w_node.right.color = BLACK  # case 4
                    self.left_rotate(node.parent)  # case 4
                    node = self.root  # case 4
            else:
                w_node = node.parent.left
                if w_node.color == RED:
                    w_node.color = BLACK  # case 1
                    node.parent.color = RED  # case 1
                    self.right_rotate(node.parent)  # case 1
                    w_node = node.parent.left  # case 1
                if w_node.right.color == BLACK and w_node.left.color == BLACK:
                    w_node.color = RED  # case 2
                    node = node.parent  # case 2
                else:
                    if w_node.left.color == BLACK:
                        w_node.right.color = BLACK  # case 3
                        w_node.color = RED  # case 3
                        self.left_rotate(w_node)  # case 3
                        w_node = node.parent.left  # case 3
                    w_node.color = node.parent.color  # case 4
                    node.parent.color = BLACK  # case 4
                    w_node.left.color = BLACK  # case 4
                    self.right_rotate(node.parent)  # case 4
                    node = self.root  # case 4
        node.color = BLACK

    def rb_transplant(self, node1, node2):
        """Helper method to check each case during re-coloring phase"""
        if node1.parent == self.none_node:
            self.root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        node2.parent = node1.parent

    def get_node(self, value):
        """Returns a node of given value"""
        # start in the root
        start_node = self.root
        # loop untill node is found, then return it
        while start_node != self.none_node:
            if value == start_node.value:
                return start_node
            if value > start_node.value:
                start_node = start_node.right
            if value < start_node.value:
                start_node = start_node.left

    def remove(self, value):
        """Removes a node from the tree"""
        # check if value is even in the tree, if not do nothing
        if self.search(value):
            node = self.get_node(value)
            # rep_node is a replacer node, it helps when removing certain nodes
            rep_node = node
            rep_node_original_color = rep_node.color
            # check if node got a left subtree
            if node.left == self.none_node:
                x_node = node.right
                self.rb_transplant(node, node.right)
            # check if node got a right subtree
            elif node.right == self.none_node:
                x_node = node.left
                self.rb_transplant(node, node.left)
            else:
                rep_node = self.node_min(node.right)
                rep_node_original_color = rep_node.color
                x_node = rep_node.right
                if rep_node.parent == node:
                    x_node.parent = rep_node
                else:
                    self.rb_transplant(rep_node, rep_node.right)
                    rep_node.right = node.right
                    rep_node.right.parent = rep_node
                self.rb_transplant(node, rep_node)
                rep_node.left = node.left
                rep_node.left.parent = rep_node
                rep_node.color = node.color
            if rep_node_original_color == BLACK:
                self.rb_delete_fixup(x_node)


if __name__ == '__main__':
    tree = RedBlackTree()
    for i in [random.randint(1, 100) for nbr in range(1, 20)]:
        tree.insert(i)
    # test code:
