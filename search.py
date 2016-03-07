#A0110649J
import re
import nltk
import sys
import os
import getopt
import math
from collections import Counter
from os.path import basename
from os import listdir
from os.path import isfile, join

#use message
def usage():
	print "usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results"

#default settings
dictionary_file = "dictionary.txt"
postings_file = "postings.txt"
query_file = "query.txt"
output_file = "out.txt"

#variables
DICTIONARY = {}
LEFT_ASSOC = 0
RIGHT_ASSOC = 1
#representation of boolean operators
OPERATORS = { 
	"OR" : (0, LEFT_ASSOC),
    "AND" : (5, LEFT_ASSOC),
    "NOT" : (10, RIGHT_ASSOC)
}
LIST_DOC = []

#specified settings
try:
	opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o')
except getopt.GetoptError, err:
	usage()
	sys.exit(2)
for o, a in opts:
	if o == '-d':
		dictionary_file = a
	elif o == '-p':
		postings_file = a
	elif o == '-q':
		query_file = a
	elif o == '-o':
		output_file = a
	else:
		assert False, "unhandled option"

#filepath handling for specified options			
if dictionary_file == None or postings_file == None or query_file == None or output_file == None:
    usage()
    sys.exit(2)
	
#load dictionary into memory
def load_dic():
	print("loading dictionary into memory..."),
	dic_file = open(dictionary_file, 'r')
	dic = dic_file.readline()
	entries = dic.split()
	for entry in entries:
		item = entry.split('^')
		word = item[0]
		index = item[1]
		DICTIONARY[word] = index
	all_files = dic_file.readline()
	a = all_files.split()
	for x in a:
		LIST_DOC.append(x)
	print("[DONE]")

#wrapper method reads all queries in the file
def read_queries():
	print("reading and searching queries..."),
	query_lines = open(query_file).readlines()
	out_write = open(output_file, 'w')
	for query in query_lines:	
		print("once")
		line = parse(query)
		result = evaluate(line)
		out_write.write(result + "\n")
	print("[DONE]")
	
#parses the query 	
def parse(input):
	tokenised = input.split()
	temp =[]
	for token in tokenised:
		if "(" in token:
			word = token.strip('(')
			temp.append('(')
			temp.append(word)
		elif ")" in token:
			word = token.strip(')')
			temp.append(word)
			temp.append(')')
		else:
			temp.append(token)
	copy = []
	for token in temp:
		if token != "AND" and token != "OR" and token != "NOT":
			current = str.lower(token)
		else:
			current = token
		copy.append(current)
	output = toRPN(copy)
	return output

#evaluates the parsed query
def evaluate(input):
	read_dic = open(dictionary_file, "r")
	seek_pos = open(postings_file, "r")
	end_set = []
	temp_set = []
	print(input)
	print(len(input))
	if len(input) == 0:
		print("invalid query: empty")
		sys.exit(2)
	word = input.pop(0)
	if word in DICTIONARY:
		pointer = DICTIONARY[word]
		print(word),
		print("pointer"),
		print(pointer)
		seek_pos.seek(int(pointer))
		line = seek_pos.readline()
		print(line)
		temp_set = line.split()
		end_set.append(temp_set)
		seek_pos.seek(0,0)
	while len(input) != 0:
		print(len(input))
		current = input.pop(0)
		if isOperator(current):
			if current == "AND":
				temp = intersect(end_set[-1], end_set[-2])
				temp_set = temp
			if current == "OR":
				temp = union(end_set[-1], end_set[-2])
				temp_set = temp
			if current == "NOT":
				temp = negation(end_set[-1])
				temp_set = temp
				end_set.append(temp_set)
		elif current in DICTIONARY:
			pointer = DICTIONARY[current]
			print(current),
			print("pointer"),
			print(pointer)
			seek_pos.seek(int(pointer))
			line = seek_pos.readline()
			print(line)
			temp_set = line.split()
			end_set.append(temp_set)
			seek_pos.seek(0,0)
		else:
			temp_set = []
			end_set.append(temp_set)
	unique(end_set[0])
	write_string = set_to_string(end_set[0])
	return write_string
	
#strips duplicates if present
def unique(a):
	return list(set(a))
	
#BOOLEAN AND	
def intersect(a, b):
	return list(set(a) & set(b))
	
#BOOLEAN OR
def union(a, b):
	return list(set(a) | set(b))

#BOOLEAN NOT (with complete LIST_DOC)
def negation(a):
	b = [e for e in LIST_DOC if e not in a]
	return b
	
#method converts a set into the format specified by submission requirements
def set_to_string(set):
	string = " ".join(str(item) for item in set)
	return string
	
#changes the format of query, infix to rpn
def toRPN(query):
	output = []
	stack = []
	for token in query:
		if isOperator(token):
			while len(stack) != 0 and isOperator(stack[-1]):
				if (isAssoc(token, LEFT_ASSOC) and precedence(token, stack[-1]) <= 0) or (isAssoc(token, RIGHT_ASSOC) and precedence(token, stack[-1]) < 0):
					output.append(stack.pop())
					continue
				break
			stack.append(token)
		elif token == '(':
			stack.append(token)
		elif token == ')':
			while len(stack) != 0 and stack[-1] != '(':
				output.append(stack.pop())
			stack.pop()
		else:
			output.append(token)
	while len(stack) != 0:
		output.append(stack.pop())
	print(output)
	return output
		
#shunting yard helpers
#check if token is operator
def isOperator(token):
	return token in OPERATORS.keys()

#check associativity of operator
def isAssoc(token, assoc):
    return OPERATORS[token][1] == assoc

#compare precedence of operators
def precedence(token1, token2):
    return OPERATORS[token1][0] - OPERATORS[token2][0]
	
#run the methods declared above
load_dic()
read_queries()