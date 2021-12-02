"""Red and black tree algorithm
    Written by Jakob Adamsson"""

#GLOBAL VARS
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
        if start_node is None:
            start_node = self.root
            path.append(start_node.value)

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
        root_node = self.root
        lst = []

        node_queue = [root_node]
        while len(node_queue) > 0:
            if node_queue != []:
                check_current_node = node_queue.pop(0)
            if check_current_node != self.none_node:
                if check_current_node.value not in lst:
                    if check_current_node.left != self.none_node:
                        node_queue.append(check_current_node.left)

                    if check_current_node.right != self.none_node:
                        node_queue.append(check_current_node.right)

                    lst.append([check_current_node.value, check_current_node.color,
                                check_current_node.left.value, check_current_node.right.value])
        return lst

    def search(self, key, node=None):
        """Searches for given value"""
        if node is None:
            node = self.root

        if key == node.value:
            return True

        if node is self.none_node:
            return False

        if node is not None:
            if key < node.value:
                return self.search(key, node.left)
            return self.search(key, node.right)

    def min(self, root=None):
        """Returns the minimum value in the tree"""
        if root is None:
            root = self.root
        min_val = root
        while min_val.left != self.none_node:
            min_val = min_val.left
        return min_val.value

    def node_min(self, root=None):
        """Returns the node holding the lowest value in the tree"""
        if root is None:
            root = self.root
        min_node = root
        while min_node.left != self.none_node:
            min_node = min_node.left
        return min_node

    def max(self, root=None):
        """Returns the maximum value in the tree"""
        if root is None:
            root = self.root
        max_val = root
        while max_val.right != self.none_node:
            max_val = max_val.right
        return max_val.value

    def left_rotate(self, node):
        """Rotates the tree so it keeps the red black tree constraints """
        node2 = node.right
        node.right = node2.left
        if node2.left != self.none_node:
            node2.left.parent = node
        node2.parent = node.parent
        if node.parent == self.none_node:
            self.root = node2
        elif node == node.parent.left:
            node.parent.left = node2
        else:
            node.parent.right = node2
        node2.left = node
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
        if self.search(new_val):  # to handle dups
            return
        node = Node(new_val)
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
        node.left = self.none_node
        node.right = self.none_node
        node.color = RED
        self.insert_fixup(node)

    def insert_fixup(self, node):
        """After insert, it recolors the nodes if needed to keep the structure"""
        while node.parent.color == RED:
            if node.parent == node.parent.parent.left:
                y_node = node.parent.parent.right
                if y_node.color == RED:
                    node.parent.color = BLACK
                    y_node.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self.right_rotate(node.parent.parent)
            else:
                y_node = node.parent.parent.left
                if y_node.color == RED:
                    node.parent.color = BLACK
                    y_node.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self.left_rotate(node.parent.parent)
        self.root.color = BLACK

    def rb_delete_fixup(self, node):
        """After deletion, recolor the nodes and re-assigning nodes"""
        while node != self.root and node.color == BLACK:
            if node == node.parent.left:
                w_node = node.parent.right
                if w_node.color == RED:
                    w_node.color = BLACK
                    node.parent.color = RED
                    self.left_rotate(node.parent)
                    w_node = node.parent.right
                if w_node.left.color == BLACK and w_node.right.color == BLACK:
                    w_node.color = RED
                    node = node.parent
                else:
                    if w_node.right.color == BLACK:
                        w_node.left.color = BLACK
                        w_node.color = RED
                        self.right_rotate(w_node)
                        w_node = node.parent.right
                    w_node.color = node.parent.color
                    node.parent.color = BLACK
                    w_node.right.color = BLACK
                    self.left_rotate(node.parent)
                    node = self.root
            else:
                w_node = node.parent.left
                if w_node.color == RED:
                    w_node.color = BLACK
                    node.parent.color = RED
                    self.right_rotate(node.parent)
                    w_node = node.parent.left
                if w_node.right.color == BLACK and w_node.left.color == BLACK:
                    w_node.color = RED
                    node = node.parent
                else:
                    if w_node.left.color == BLACK:
                        w_node.right.color = BLACK
                        w_node.color = RED
                        self.left_rotate(w_node)
                        w_node = node.parent.left
                    w_node.color = node.parent.color
                    node.parent.color = BLACK
                    w_node.left.color = BLACK
                    self.right_rotate(node.parent)
                    node = self.root
        node.color = BLACK

    def rb_transplant(self, node1, node2):
        """Checks for each case"""
        if node1.parent == self.none_node:
            self.root = node2
        elif node1 == node1.parent.left:
            node1.parent.left = node2
        else:
            node1.parent.right = node2
        node2.parent = node1.parent

    def get_node(self, value):
        """Returns a node of given value"""
        start_node = self.root

        while start_node != self.none_node:
            if value == start_node.value:
                return start_node
            if value > start_node.value:
                start_node = start_node.right
            if value < start_node.value:
                start_node = start_node.left

    def remove(self, value):
        """Removes a node from the tree"""
        if self.search(value):
            node = self.get_node(value)
            rep_node = node
            rep_node_original_color = rep_node.color
            if node.left == self.none_node:
                x_node = node.right
                self.rb_transplant(node, node.right)
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
    träd = RedBlackTree()
    for i in [7]:
        träd.insert(i)
    # print(träd.bfs())
    # print(träd.min(träd.root))
    # print(träd.path(25))
    träd.remove(7)
    print(träd.bfs())
