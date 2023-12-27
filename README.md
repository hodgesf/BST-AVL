# BST-AVL
Binary search tree and AVL tree implementations

Binary Search Tree (BST) Implementation
This repository provides an implementation of a Binary Search Tree (BST) data structure in Python.

Overview
A Binary Search Tree is a hierarchical data structure with a root node and subtrees, where the left subtree contains nodes with values less than the root and the right subtree contains nodes with values greater than the root. This repository offers a Python implementation of a BST with key features:

Efficient Search: Provides efficient search operations with an average time complexity of O(log n).

Insertion and Deletion: Supports insertion and deletion of elements while maintaining the BST property.

Features
BST class: Includes functionalities for creating and manipulating a Binary Search Tree.

Search: Efficiently find elements in the tree.

Insertion and Deletion: Add or remove elements while keeping the tree balanced and ordered.

Usage
Example usage of the BST class:

python
Copy code
# Create a BST instance
bst = BST()

# Insert elements
bst.insert(10)
bst.insert(5)
bst.insert(15)

# Search for an element
found = bst.search(5)
print(f"Element found: {found}")
Getting Started
To use this BST implementation in your project, clone the repository and import the BST class:

python
Copy code
from binary_search_tree import BST
Contributions
Contributions and feedback are appreciated! Feel free to open issues or pull requests for improvements, bug fixes, or additional features.

AVL Tree Implementation
This repository contains an implementation of an AVL (Adelson-Velsky and Landis) Tree in Python.

Overview
An AVL Tree is a self-balancing binary search tree where the heights of the two child subtrees of any node differ by at most one. This repository offers a Python implementation of an AVL Tree with key features:

Self-Balancing: Automatically maintains balance after insertion or deletion, ensuring logarithmic time complexity for basic operations.

Efficient Operations: Provides efficient search, insertion, and deletion operations.

Features
AVLTree class: Includes functionalities for creating and manipulating an AVL Tree.

Insertion and Deletion: Supports balanced insertion and deletion of elements.

Usage
Example usage of the AVLTree class:

python
Copy code
# Create an AVLTree instance
avl_tree = AVLTree()

# Insert elements
avl_tree.insert(10)
avl_tree.insert(5)
avl_tree.insert(15)

# Delete an element
avl_tree.delete(5)
Getting Started
To use this AVL Tree implementation, clone the repository and import the AVLTree class:

python
Copy code
from avl_tree import AVLTree
Contributions
Contributions are welcome! If you have suggestions, bug reports, or want to add new features, feel free to open an issue or create a pull request.
