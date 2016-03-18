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
NUM_DOCS = 0

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
	docs_line = dic_file.readline()
	list_docs = docs_line.split()
	for entry in list_docs:
		item = entry.split('_')
		filename = item[0]
		numwords = item[1]
		LIST_DOC[filename] = numwords
	NUM_DOCS = LIST_DOC.len
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
	word_score = {}
	seek_pos = open("postings.txt", 'r')
	seek_pos.seek(0,0)
	words = query.split()
	result = []
	for word in words:
		if word not in word_score:	
			if word in DICTIONARY:
				seek_pointer = DICTIONARY[word]
				seek_pos.seek(int(pointer))
				line = seek_pos.readline()
				seek_pos,seek(0,0)
				post_list = line.split()
				score = score_documents(post_list)
				word_score[word] = score
			else:
				#not encountered, score of 0
				word_score[word] = 0
		#else duplicate, skip word
	return result

#method scores the documents	
def score_documents(list_postings):
	doc_frequency = list_postings.len
	idf = math.log(doc_frequency, 10)
	for post in list_postings:
		item = post.split("_")
		doc_id = item[0]
		term_frequency = item[1]
		
	
#lines below run the methods defined above
load_dic()
read_queries()