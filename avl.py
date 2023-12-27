# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Add a value to the AVL tree

        :param value: Object to be added to the AVL tree
        :return: None
        """
        if not self._root:
            self._root = AVLNode(value)
        else:
            self._add_recursive(value, self._root)

    def _add_recursive(self, value: object, node: AVLNode) -> None:
        """
        Helper function to recursively add a value to the AVL tree

        :param value: Object to be added to the AVL tree
        :param node: Current AVLNode being considered during recursion
        :return: None
        """
        if value < node.value:
            if node.left is None:
                node.left = AVLNode(value)
                node.left.parent = node
                self._update_height(node.left)  # Update height after insertion
                self._rebalance(node.left)  # Rebalance if necessary
            else:
                self._add_recursive(value, node.left)
        elif value > node.value:
            if node.right is None:
                node.right = AVLNode(value)
                node.right.parent = node
                self._update_height(node.right)  # Update height after insertion
                self._rebalance(node.right)  # Rebalance if necessary
            else:
                self._add_recursive(value, node.right)

    def remove(self, value: object) -> bool:
        """
        Remove a value from the AVL tree

        :param value: Object to be removed from the AVL tree
        :return: True if the value is successfully removed, False otherwise
        """
        if not self._root:
            return False
        else:
            removed = self._remove_recursive(value, self._root)
            if removed:
                self._rebalance(self._root)  # Rebalance from the root only if a node was removed
            return removed

    def _remove_recursive(self, value: object, node: AVLNode) -> bool:
        """
        Helper function to recursively remove a value from the AVL tree

        :param value: Object to be removed from the AVL tree
        :param node: Current AVLNode being considered during recursion
        :return: True if the value is successfully removed, False otherwise
        """
        if not node:
            return False

        if value < node.value:
            removed = self._remove_recursive(value, node.left)
            if removed:
                self._update_height(node)
                self._rebalance(node)
            return removed
        elif value > node.value:
            removed = self._remove_recursive(value, node.right)
            if removed:
                self._update_height(node)
                self._rebalance(node)
            return removed
        else:  # Found the node to remove
            if not node.left and not node.right:
                self._remove_leaf(node)
            elif not node.left or not node.right:
                self._remove_with_single_child(node)
            else:
                successor = self._find_min_node(node.right)
                node.value = successor.value
                self._remove_recursive(successor.value, node.right)
                self._update_height(node)
                self._rebalance(node)
            return True

    def _find_min_node(self, node: AVLNode) -> AVLNode:
        """
        Helper function to find the node with the minimum value in a subtree

        :param node: Current AVLNode being considered to find the minimum value
        :return: AVLNode with the minimum value in the subtree
        """
        current = node
        while current.left:
            current = current.left
        return current

    def _remove_leaf(self, node: AVLNode) -> None:
        """
        Helper function to remove a leaf node

        :param node: Leaf AVLNode to be removed from the AVL tree
        :return: None
        """
        if node.parent:
            if node.parent.left == node:
                node.parent.left = None
            else:
                node.parent.right = None
            self._update_height(node.parent)  # Update height after removal
            self._rebalance(node.parent)  # Rebalance the tree after removal
        else:
            self._root = None

    def _remove_with_single_child(self, node: AVLNode) -> None:
        """
        Helper function to remove a node with a single child

        :param node: AVLNode with a single child to be removed from the AVL tree
        :return: None
        """
        if node.left:
            child = node.left
        else:
            child = node.right

        if node.parent:
            if node.parent.left == node:
                node.parent.left = child
            else:
                node.parent.right = child
            if child:
                child.parent = node.parent
            self._update_height(node.parent)  # Update height after removal
            self._rebalance(node.parent)  # Rebalance the tree after removal
        else:
            self._root = child
            if child:
                child.parent = None
            self._update_height(child)  # Update height after removal
            self._rebalance(child)  # Rebalance the tree after removal

    def _update_height(self, node: AVLNode) -> None:
        """
        Update the height of a node in the AVL tree

        :param node: AVLNode whose height needs to be updated
        :return: None
        """
        if not node:
            return

        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        node.height = 1 + max(left_height, right_height)

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalance the AVL tree from a given node

        :param node: AVLNode from which the tree needs to be rebalanced
        :return: None
        """
        if not node:
            return
        self._update_height(node)
        balance = self._balance_factor(node)

        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self._rotate_left(node.left)
            node = self._rotate_right(node)
        elif balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self._rotate_right(node.right)
            node = self._rotate_left(node)

        if node.parent:
            self._rebalance(node.parent)
        else:
            self._root = node

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Perform a left rotation on a node in the AVL tree

        :param node: AVLNode object on which the left rotation is performed
        :return: AVLNode representing the new root after the left rotation
        """
        # Check if the node or its right child is None, indicating inability to rotate left
        if not node or not node.right:
            return node

        # Assign the right child of the node as the new root for the left rotation
        new_root = node.right
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node

        new_root.parent = node.parent
        # Update the root of the AVL tree if the node was the root
        if node.parent is None:
            self._root = new_root
        else:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root

        # Perform the rotation
        new_root.left = node
        node.parent = new_root

        # Update heights after the rotation
        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Perform a right rotation on a node in the AVL tree

        :param node: AVLNode object on which the right rotation is performed
        :return: AVLNode representing the new root after the right rotation
        """
        # Check if the node or its left child is None, indicating inability to rotate right
        if not node or not node.left:
            return node

        # Assign the left child of the node as the new root for the right rotation
        new_root = node.left
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node

        new_root.parent = node.parent
        # Update the root of the AVL tree if the node was the root
        if node.parent is None:
            self._root = new_root
        else:
            if node.parent.left == node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root

        # Perform the rotation
        new_root.right = node
        node.parent = new_root

        # Update heights after the rotation
        self._update_height(node)
        self._update_height(new_root)

        return new_root

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculate the balance factor of a node in the AVL tree

        :param node: AVLNode object for which the balance factor needs to be calculated
        :return: Integer representing the balance factor of the node
        """
        # The balance factor is calculated as the height of the left subtree
        # minus the height of the right subtree
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_height(self, node: AVLNode) -> int:
        """
        Get the height of a node in the AVL tree

        :param node: AVLNode object whose height needs to be determined
        :return: The height of the node; -1 if the node is None
        """
        # If the node is None, its height is -1
        if not node:
            return -1
        # Return the height of the node
        return node.height


# ------------------- BASIC TESTING -----------------------------------------
li = [55, 3, 33, 22, 42, 76, 20]
for i in li:
    print(i % 7)





