"""Progream testing correctness in RED-BLACK Tree class from module red_black_tree"""

import math
import random
import sys
import pylint.lint
import red_black_tree as rbt

SPEED_FACTOR = 1

MAX_SIZE = 500
LIST_SIZE = MAX_SIZE // SPEED_FACTOR

LINT_THRESHOLD = 8.0


def check_functions(the_rbt):
    """Checks if required methods are implemented in class RedBlackTree"""
    FUNC_LIST = ["insert", "remove", "search", "path", "min", "max", "bfs"]
    print(f"\nTesting if the class has the required methods. ({FUNC_LIST})")

    for func in FUNC_LIST:
        if not hasattr(the_rbt, func):
            print(f"The class does not have {func}() method.")
            sys.exit(1)
    print("The class has the required methods.\n")
    return True


def create_test_list():
    """Creates random list of unique values to pyt in the tree"""
    return random.sample(range(-5*LIST_SIZE, 5*LIST_SIZE), LIST_SIZE)


def test_red_black_constraints(t_bfs):
    THE_VALUE = 0
    THE_COLOR = 1
    LEFT_VALUE = 2
    RIGHT_VALUE = 3
    THE_INDEX = 4

    def find_child(value, start=0):
        if start > len(t_bfs)-2:
            return None
        for i, item in enumerate(t_bfs[start:len(t_bfs)]):
            if item[THE_VALUE] == value:
                return [t_bfs[i+start][THE_VALUE], t_bfs[i+start][THE_COLOR],
                        t_bfs[i+start][LEFT_VALUE], t_bfs[i+start][RIGHT_VALUE], i+start]
        return None

    def test_black_count(index):
        if index >= len(t_bfs):
            return 0

        left_node = find_child(t_bfs[index][LEFT_VALUE], index+1)
        right_node = find_child(t_bfs[index][RIGHT_VALUE], index+1)

        left_black_count = 0
        if not left_node is None:
            if str(left_node[THE_COLOR]).upper() == "BLACK":
                left_black_count += 1
            left_black_count += test_black_count(left_node[THE_INDEX])

        right_black_count = 0
        if not right_node is None:
            if str(right_node[THE_COLOR]).upper() == "BLACK":
                right_black_count += 1
            right_black_count += test_black_count(right_node[THE_INDEX])

        if right_black_count != left_black_count:
            print(
                f"Error: For the node {t_bfs[index][THE_VALUE]}, the number of black nodes in "
                + f"each path in in the right branch ({right_black_count}) is not the same as its "
                + f"left branch ({left_black_count}).")
            sys.exit(1)
        else:
            pass
        return left_black_count

    def test_black_count_constraint():
        test_black_count(0)

    def test_red_parent_constraint():
        for i, item in enumerate(t_bfs):
            if str(item[THE_COLOR]).upper() == "RED":

                left_node = find_child(item[LEFT_VALUE], i+1)
                right_node = find_child(item[RIGHT_VALUE], i+1)

                if not left_node is None and str(left_node[THE_COLOR]).upper() == "RED":
                    print(
                        f"ERROR: A red left child ({left_node[THE_VALUE]}  for a "
                        + f"red parent ({item[THE_VALUE]}) violates Red-Black Trees constraints.")
                    sys.exit(1)

                if not (right_node is None) and str(right_node[THE_COLOR]).upper() == "RED":
                    print(
                        f"ERROR: A red right child ({right_node[THE_VALUE]}  for a"
                        + f" red parent ({item[THE_VALUE]}) violates Red-Black Trees constraints.")
                    sys.exit(1)

    test_red_parent_constraint()
    test_black_count_constraint()


def test_insert(tree, insert_list):
    # print(f"Inserts {LIST_SIZE} items")
    # print(insert_list)
    print("Tests red-black constraints after each step")
    for i, item in enumerate(insert_list):
        tree.insert(item)
        if not tree.search(item):
            print(f"Failed to insert {item}, element number {i+1}")
            sys.exit(1)
        bfs_list = tree.bfs()
        test_red_black_constraints(bfs_list)
    nr_of_nodes = len(bfs_list)
    if nr_of_nodes != LIST_SIZE:
        print(
            f"The bfs from tree has {len(bfs_list)} nodes, it should be {LIST_SIZE}")
        print("Wrong nr of nodes in list from bfs")
        sys.exit(1)

    print("All inserts correct")


def test_bfs(tree):
    print(f"\nTesting BFS")
    bfs_list = tree.bfs()
    bfs_list_length = len(bfs_list)
    if bfs_list_length != LIST_SIZE:
        print("Wrong number of nodes in BFS list")
        sys.exit(1)
    for i in range(bfs_list_length-1):
        if bfs_list[i] > bfs_list[i+1]:
            if i+2 < bfs_list_length and bfs_list[i+1] > bfs_list[i+2]:
                print(
                    f"Wrong BFS, check items {bfs_list[i]},{bfs_list[i+1]},{bfs_list[i+2]}")
                sys.exit(1)
    print("Passed the first BFS validity test.")


def test_duplicate(tree, base_list):
    """Test so duplicates are not inserted in RB Tree"""
    print("\nTest if duplicates are ignored")
    test_values = random.sample(base_list, 4)
    # print("Try to insert duplicates", test_values)
    tree_size = len(tree.bfs())
    for item in test_values:
        # print("Insert:", item)
        tree.insert(item)
        if len(tree.bfs()) > tree_size:
            print("Error: You put a duplicate value in your tree.")
            print("Insertion of duplicates is not allowed")
            sys.exit(1)

    print("Your tree handles duplicates correctly.")


def test_min_max(tree, base_list):
    print("\nTesting min,max")
    try:

        the_min = tree.min()
        if the_min == min(base_list):
            print(f"Correct min ({the_min})")
        else:
            print(
                f"Error: Calculated Min is {the_min}, while it should be {min(base_list)}")
            sys.exit(1)
    except:
        print("Error: in calculating min value")
        sys.exit(1)

    try:
        the_max = tree.max()
        if the_max == max(base_list):
            print(f"Correct max ({the_max})")
        else:
            print(
                f"Error: Calculated Max is {the_max}, while it should be {max(base_list)}")
            sys.exit(1)
    except:
        print("Error: in calculating max value")
        sys.exit(1)
    return [the_min, the_max]


def test_search(tree, item_list):
    print("\nTesting search() method")
    in_list = random.sample(item_list, len(item_list)//4)
    not_in_list = []
    while len(not_in_list) < 5:
        candidate = random.randint(-3*LIST_SIZE, 3*LIST_SIZE)
        if candidate not in item_list:
            not_in_list.append(candidate)
    for item in in_list:
        hit = tree.search(item)
        if not isinstance(hit, bool):
            print(
                f"Method returned wrong type. Type is {type(hit)}, should be bool.")
            sys.exit(1)
        if not hit:
            print("Search method returns False for an item that should be in the tree")
            sys.exit(1)

    for item in not_in_list:
        hit = tree.search(item)
        if not isinstance(hit, bool):
            print(
                f"Method returned wrong type. Type is {type(hit)}, should be bool.")
            sys.exit(1)
        if hit:
            print("Search method returns True for an item that should not be in the tree")
            sys.exit(1)
    print("Successfully passed search() tests")


def test_remove(tree, remove_list):
    print("\nRemoves all items")
    # print(remove_list)
    print("Tests red-black constraints after each step")
    for i, item in enumerate(remove_list):
        # print(item)
        tree.remove(item)
        if tree.search(item):
            print(f"Failed to remove {item}, element number {i+1}")
            # print(tree.bfs())
            sys.exit(1)
        bfs_list = tree.bfs()

    test_red_black_constraints(bfs_list)

    empty = len(bfs_list)
    if empty != 0:
        print(
            f"List from bfs is not empty {bfs_list} \n"
            + "when the tree should be empty after all removes")
        sys.exit(1)

    print("All nodes removed correctly!")


def test_path(the_rbt, base_list):
    print("\nTest paths implementation and length")

    path_lengths = []
    try:
        for i in range(LIST_SIZE):
            path = the_rbt.path(base_list[i])
            if path[-1] != base_list[i]:
                print(
                    f"Could not find the item in the path function ({path[-1]}!={base_list[i]}).")
                sys.exit(1)
            path_lengths.append(len(path)-1)
    except:
        print(f"Problem finding path for item {base_list[i]}")
        sys.exit(1)
    print("Found all paths successfully")

    path_length_min = min(path_lengths)
    path_length_max = max(path_lengths)
    print(
        f"Min path length = {path_length_min}, Max path length = {path_length_max}")
    if 2*math.log2(LIST_SIZE) <= path_length_max:
        print(
            f"Error: Max = {path_length_max} > {2*math.log2(LIST_SIZE)}")
        sys.exit(1)

    theoretical_max = math.ceil(2*math.log2(LIST_SIZE))
    full_balance = math.floor(math.log2(LIST_SIZE))
    print(f"Max = {path_length_max}  <= Max by theory = {theoretical_max}")
    print(f"          <= Mininimum by theory = {full_balance}")

    if len(base_list) > 1:
        if path_length_max < full_balance:
            print(f"Error: Maximum path length can not be {path_length_max}.")
            print(f"It needs to be at least{full_balance}")
            sys.exit(1)
    return path_lengths


def test_code_quality():
    """Tests if pylint score of file is minimum LINT_THRESHOLD"""
    print("\nTesting code quality by lint score .....\n")
    run = pylint.lint.Run([file], do_exit=False)
    score = run.linter.stats["global_note"]
    if score < LINT_THRESHOLD:
        print(f"The pylint score is only {score}, at least 8.0 required")
        sys.exit(1)

    print("Lint score OK")


if __name__ == "__main__":
    file = "red_black_tree.py"
    my_tree = rbt.RedBlackTree()
    check_functions(my_tree)
    my_list = create_test_list()
    test_insert(my_tree, my_list)
    test_bfs(my_tree)
    test_duplicate(my_tree, my_list)
    test_min_max(my_tree, my_list)
    test_search(my_tree, my_list)
    my_list = random.sample(my_list, len(my_list))
    test_path(my_tree, my_list)

    test_remove(my_tree, my_list)
    test_code_quality()
    print("\nCongratulations, all tests passed successfully!")
