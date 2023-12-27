# Name: Frank Hodges
# OSU Email: hodgesf@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4, BST and AVL
# Due Date: 11/21/23
# Description: Implementation of BST for use in the avl.py file.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        This method adds a new value to the tree. Duplicate values are allowed. If a node with
        that value is already in the tree, the new value should be added to the right subtree of that
        node. It is implemented with O(N) runtime complexity.
        :param value: value to be added to the BST
        :return: none
        """
        new_node = BSTNode(value)
        parent = None
        current = self._root

        while current is not None:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if parent is None:
            self._root = new_node
        elif value < parent.value:
            parent.left = new_node
        else:
            parent.right = new_node

    def remove(self, value: object) -> bool:
        """
        Removes the node with the specified value from the tree, if it exists.
        :param value: value to be removed from the BST
        :return: True if value was removed successfully, False otherwise
        """
        parent = None
        current = self._root

        # Finding the node to be removed and its parent
        while current is not None and current.value != value:
            parent = current
            if value < current.value:
                current = current.left
            else:
                current = current.right

        if current is None:
            return False  # Value not found

        # Case 1: Node has no children
        if current.left is None and current.right is None:
            if parent is None:  # Removing root
                self._root = None
            elif parent.left == current:
                parent.left = None
            else:
                parent.right = None
        # Rest of the code remains the same

            return True  # Value removed successfully

        # Case 2: Node has one child
        elif current.left is None or current.right is None:
            if current.left is not None:
                replacement = current.left
            else:
                replacement = current.right

            if parent is None:  # Removing root
                self._root = replacement
            elif parent.left == current:
                parent.left = replacement
            else:
                parent.right = replacement
            return True

        # Case 3: Node has two children
        else:
            successor_parent = current
            successor = current.right
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left

            if successor != current.right:
                successor_parent.left = successor.right
                successor.right = current.right

            successor.left = current.left

            if parent is None:  # Removing root
                self._root = successor
            elif parent.left == current:
                parent.left = successor
            else:
                parent.right = successor
            return True

    def contains(self, value: object) -> bool:
        """
        Checks if the tree contains a given value.

        :param value: The value to check for in the tree.
        :type value: object
        :return: True if the value is found in the tree, False otherwise.
        :rtype: bool
        :complexity: O(N) - linear time complexity where N is the number of nodes in the tree.
        """
        current = self._root  # Start at the root of the tree
        while current is not None:
            if value == current.value:
                return True  # Return True if the value is found in the tree
            elif value < current.value:
                current = current.left  # Traverse left if the value is less than the current node's value
            else:
                current = current.right  # Traverse right if the value is greater than the current node's value
        return False  # Return False if the value is not found or the tree is empty

    def inorder_traversal(self) -> Queue:
        """
        Performs an inorder traversal of the tree and returns a Queue object containing
        the visited nodes' values.

        :return: Queue containing the values of the visited nodes in inorder traversal.
        :rtype: Queue
        :complexity: O(N) - linear time complexity where N is the number of nodes in the tree.
        """
        result_queue = Queue()  # Create a queue to store the traversal result
        current = self._root  # Start at the root
        stack = []  # Use a stack for iterative traversal

        while stack or current:
            while current:
                stack.append(current)
                current = current.left  # Traverse left until the leftmost node

            current = stack.pop()  # Process the current node
            result_queue.enqueue(current.value)  # Enqueue the value of the current node
            current = current.right  # Move to the right subtree

        return result_queue

    def find_min(self) -> object:
        """
        Finds the minimum value in the tree.

        :return: The minimum value in the tree. Returns None if the tree is empty.
        :rtype: object
        :complexity: O(N) - linear time complexity where N is the number of nodes in the tree.
        """
        current = self.get_root()  # Get the root of the tree
        if current is None:
            return None  # Return None if the tree is empty

        # Traverse to the leftmost node to find the minimum value
        while current.left is not None:
            current = current.left

        return current.value  # Return the minimum value

    def find_max(self) -> object:
        """
        Returns the highest value in the tree.

        :return: The maximum value in the tree. Returns None if the tree is empty.
        :rtype: object
        :complexity: O(N) - linear time complexity where N is the number of nodes in the tree.
        """
        current = self.get_root()  # Retrieve the root of the tree
        if current is None:
            return None  # Return None if the tree is empty

        # Traverse to the rightmost node, which holds the maximum value
        while current.right is not None:
            current = current.right

        return current.value  # Return the maximum value

    def is_empty(self) -> bool:
        """
        Checks if the tree is empty.

        :return: True if the tree is empty, False otherwise.
        :rtype: bool
        :complexity: O(1) - constant time complexity.
        """
        if self.get_root() is None:
            return True  # If the root is None, the tree is empty
        return False  # If the root exists, the tree is not empty

    def make_empty(self) -> None:
        """
        Removes all nodes from the tree.

        :complexity: O(1) - constant time complexity.
        """
        self._root = None  # Set the root to None, effectively removing all nodes from the tree


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
