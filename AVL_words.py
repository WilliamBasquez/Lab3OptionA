#I used the implementation for AVL trees from ZyBook, just modified the insertion method to take a word as key
#as well as a list offloating point numbers as vectors; I also took away the deletion functions as these were
#not required on the lab.
#I implemented the function 'get_height' from the Red-Black Tree file

class Node:
    def __init__(self, key, arr):
	#the 'arr' parameter will become the node's vectors
        self.key = key
        self.vectors = arr
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def get_balance(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        return left_height - right_height

    def update_height(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        self.height = max(left_height, right_height) + 1


    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child is not None:
            child.parent = self

        self.update_height()
        return True

    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)

        return False


class AVLTree:
	def __init__(self):
		self.root = None

	def rotate_left(self, node):
		right_left_child = node.right.left

		if node.parent is not None:
			node.parent.replace_child(node, node.right)
		else:  # node is root
			self.root = node.right
			self.root.parent = None

		node.right.set_child('left', node)

		node.set_child('right', right_left_child)

		return node.parent

	def rotate_right(self, node):
		left_right_child = node.left.right

		if node.parent is not None:
			node.parent.replace_child(node, node.left)
		else:  # node is root
			self.root = node.left
			self.root.parent = None

		node.left.set_child('right', node)

		node.set_child('left', left_right_child)

		return node.parent

	def rebalance(self, node):
		node.update_height()

		if node.get_balance() == -2:
			if node.right.get_balance() == 1:
				self.rotate_right(node.right)
			return self.rotate_left(node)

		elif node.get_balance() == 2:
			if node.left.get_balance() == -1:
				self.rotate_left(node.left)
			return self.rotate_right(node)

		return node


	def left_child(self, node):
		current = self.root
		if current.left is None:
			current.left = node
			node.parent = current
			current = None
		else:
			current = current.left


	def right_child(self, node):
		current = self.root
		if current.right is None:
			current.right = node
			node.parent = current
			current = None
		else:
			current = current.right
		return

	def get_height(self):
		return self._get_height_recursive(self.root)

	def _get_height_recursive(self, node):
		if node is None:
			return -1
		left_height = self._get_height_recursive(node.left)
		right_height = self._get_height_recursive(node.right)
		return 1 + max(left_height, right_height)

	def insert(self, node):
		#this function takes in a node and in order to insert in the right place
		#it compares the Unicode code point of the first letter on the new word to the one
		#on the current node (if one exists)
		if self.root is None:
			self.root = node
			node.parent = None
		else:
			current_node = self.root
			while current_node is not None:
				if ord(node.key[0]) < ord(current_node.key[0]):
					if current_node.left is None:
						current_node.left = node
						node.parent = current_node
						current_node = None
					else:
						current_node = current_node.left
				else:
					if current_node.right is None:
						current_node.right = node
						node.parent = current_node
						current_node = None
					else:
						current_node = current_node.right

			node = node.parent
			while node is not None:
				self.rebalance(node)
				node = node.parent

	def search(self, key):
		current_node = self.root
		while current_node is not None:
			if current_node.key == key:
				return current_node
			elif current_node.key < key:
				current_node = current_node.right
			else:
				current_node = current_node.left

	# Overloading the __str__() operator to create a nicely-formatted text representation of
    # the tree. Derived from Joohwan Oh at:
    #    https://github.com/joowani/binarytree/blob/master/binarytree/__init__.py
	def __str__(self):
		return pretty_tree(self)
