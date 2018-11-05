"""
@author: William E Basquez
@Course: CS 2302
@Assignment: Lab 3, Option A
@Instructor: Diego Aguirre
@T.A: Manoj Saha
@Last modification: Nov 5, 2018 
"""
import os
import numpy as np
import math
from AVL_words import AVLTree, Node
from RBTree import RedBlackTree, RBTNode
def reader():
#This function reads the file, as well as encodes it to make the data manageable
#It also chacks if the first letter on a word is a letter; if it is, it appends it to the list
#otherwise, it skips it
	filename = "glove.6B.50d.txt"
	#filename = "new_list.txt"
	#filename = "temp.txt"
	contents, a = [], []
	if os.path.exists(filename):
		lines = open(filename, encoding="utf8")

		for line in lines:
			word = line.strip('\n')
			new_word = word.split(' ')
			if new_word[0][0].isalpha():
				contents.append(new_word)

		if len(contents) == 0:
			print("Existing file, but empty")
	else:
		print("File not found")

	return contents

def reader_words():
#This function also reads a file, but with a simple pair of words to test the similarity function later on
	filename = "pairOfWords.txt"

	pair_words = []
	if os.path.exists(filename):
		lines = open(filename, encoding="utf8")

		for line in lines:
			new_line = line.strip('\n')
			pair_words.append(new_line.split('\t'))

		if len(pair_words) == 0:
			print("Existing file, but no content")
	else:
		print("File not found")

	return pair_words

def file_writter(a):
#This function writes a new file named 'myfile' with the words in the tree, one per line
	f = open("myfile.txt", "w")
	for i in range(len(a)):
		b = bytes(a[i], encoding='utf-8')
		f.write(str(b, encoding='ascii',errors='ignore'))
		f.write('\n')


def arrStr_toFloat(arr):
#This array turns the list of vectors into actual floating numbers to use them to find the dot product as well as the
#magnitude of such vectors
	numbers = []
	j = 0
	while j < len(arr):
		numbers.append(float(arr[j]))
		j+=1
	return numbers

def dot_product(a1, a2):
#This function uses the package numpy to calculate the dot product of 2 lists of vectors
	return np.dot(a1, a2)

def word_magnitude(a):
#This function uses the package numpy and returns the magnitude of a list of vectors
	return np.linalg.norm(a)

def similarity(a1, a2):
	#It combines the functions 'dot_producs' and 'word_magnitude' to calculate the cosine similarity between 2 list of vectors
	#|a| = square root of the dot product of the vector with itself
	#so |a| |b| == |a|*|b|, and |a| == sqrt(dot_product(itself)) or np.linalg.norm(a)
	#It works now, answers are almost the same as in PDF
	arr1 = arrStr_toFloat(a1)
	arr2 = arrStr_toFloat(a2)
	top_part = dot_product(arr1, arr2)
	bottom_part = word_magnitude(arr1) * word_magnitude(arr2)
	magnitude = top_part / bottom_part
	return magnitude

def main():
	input_array = reader()
	pair_words = reader_words()
	input_array.sort() #TimSort O(n log n)
	arr_words = []
	arr_vecs = []
	for i in range(len(input_array)):
		arr_words.append(input_array[i][0])
		arr_vecs.append(input_array[i][1:])
	type_of_tree = input("What kind of tree would you like to use? Enter number\n1)AVL Tree\n2)Red-Black Tree\nAnswer: ")
	if type_of_tree == "1":
		tree = AVLTree()
		for i in range(len(arr_words)):
			node = Node(arr_words[i], arr_vecs[i])
			tree.insert(node)
		for i in range(len(pair_words)):
			node1 = tree.search(pair_words[i][0])
			node2 = tree.search(pair_words[i][1])
			#print(node1.key, node2.key, similarity(node1.vectors, node2.vectors))
		print("The height of the tree is:", tree.get_height(), "and it has", len(arr_words),"nodes")
		file_writter(arr_words)
	elif type_of_tree == "2":
		tree = RedBlackTree()
		for i in range(len(arr_words)):
			tree.insert(arr_words[i], arr_vecs[i])
		for i in range(len(pair_words)):
			node1 = tree.search(pair_words[i][0])
			node2 = tree.search(pair_words[i][1])
			#print(node1.key, node2.key, similarity(node1.vectors, node2.vectors))
		print("The height of the tree is:", tree.get_height(), "and it has", len(arr_words),"nodes")
		file_writter(arr_words)
	else:
		print("Option not available")

main()
#SOURCES USED
#https://www.geeksforgeeks.org/abs-in-python/
#https://www.geeksforgeeks.org/type-conversion-python/
#https://www.w3schools.com/python/python_file_write.asp
#https://www.geeksforgeeks.org/python-math-function-sqrt/
#https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-93.php
#https://stackoverflow.com/questions/9171158/how-do-you-get-the-magnitude-of-a-vector-in-numpy
#https://stackoverflow.com/questions/5919530/what-is-the-pythonic-way-to-calculate-dot-product
#https://slideplayer.com/slide/4559721/15/images/16/The+cosine+similarity+measure+%281%29.jpg
