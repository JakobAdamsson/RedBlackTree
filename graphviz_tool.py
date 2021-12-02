import time
from graphviz import render
from graphviz import Source
import red_black_tree as rbt


NEWLINE = '\n'
TAB = '\t'
BIG_NUMBER = 100000
NODE_VALUE = 0
THE_COLOR = 1
LEFT_CHILD = 2
RIGHT_CHILD = 3


def tree_to_graphviz(nodes, filename):
    """Create Graphviz .dot file from a node list
    Parameters
    ----------
    node_list: list - elements must be info from nodes where each node is
                      represented by a list on the following format:
                      [value, color, left_child_value, right_child_value]

                      color must be the string 'BLACK' or 'RED' for RBT
                      (if color is None or '' nodes are gray, can be used for BST)
                      value of a missing child must be None

    filename: str
    """

    def gname(inp):
        return f'n{inp + BIG_NUMBER if inp >= 0 else abs(inp) + 2*BIG_NUMBER}'

    graph = f'digraph RBTREE {{\ngraph [class="{int(time.time())}"];'
    for _, item in enumerate(nodes):

        graph = f'{graph}{NEWLINE}{gname(item[NODE_VALUE])} [label = "{item[NODE_VALUE]}", ' + \
            f'style=filled, fontcolor = white'
        if item[THE_COLOR]:
            graph += f', fillcolor = {item[THE_COLOR]}'
        graph += '];'

        if not item[LEFT_CHILD] is None:
            graph = f'{graph}{NEWLINE}{gname(item[NODE_VALUE])} -> {gname(item[LEFT_CHILD])};'

        if not item[RIGHT_CHILD] is None:
            graph = f'{graph}{NEWLINE}{gname(item[NODE_VALUE])} -> {gname(item[RIGHT_CHILD])};'

    graph = graph + '\n}'
    f = open(filename, 'w')
    f.write(graph)
    f.close()


# Testcode
if __name__ == '__main__':
    träd = rbt.RedBlackTree()
    for i in [10]:
        träd.insert(i)
    träd.remove(10)
    test_list = träd.bfs()

    tree_to_graphviz(test_list, 'testfile.dot')
