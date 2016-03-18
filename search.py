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
LIST_DOC = {}

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
	list_docs = dic_file.readline()
	for entry in list_docs:
		item = entry.split('_')
		filename = item[0]
		numwords = item[1]
		LIST_DOC[filename] = numwords
	print("[DONE]")

#read and evaluate all queries from file
def read_queries(file):
	out_writer = open("outtxt", 'w')
	with open(file) as fp:
		for line in fp:
			evaluate(line)
	close(file)

#evaluate one query
def evaluate(query):
	doc_score = {}
	seek_pos = open("postings.txt", 'r')
	seek_pos.seek(0,0)
	words = query.split()
	result = []
	for word in words:
		seek_pointer = DICTIONARY[word]
		seek_pos.seek(int(pointer))
		line = seek_pos.readline()
		seek_pos,seek(0,0)
		print("todo score word")
	return result
	
#lines below run the methods defined above
load_dic()