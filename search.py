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
from operator import itemgetter

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
	NUM_DOCS = list_docs.length
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
			result = evaluate(line)
			out_writer.write(result + "\n")
	close(file)

#evaluate one query
def evaluate(query):
	word_score = {}
	seek_pos = open("postings.txt", 'r')
	seek_pos.seek(0,0)
	words = query.split()
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
	result = score_query(word_score)
	return result

#method scores the documents by word frequency
def score_documents(list_postings):
	score_list = []
	doc_frequency = list_postings.length * 1.0
	idf_score = float(math.log(NUM_DOCS/doc_frequency, 10))
	for post in list_postings:
		item = post.split("_")
		doc_id = item[0]
		term_frequency = item[1]
		tf_score = (1+ math.log(term_frequency, 10))
		tf_idf = tf_score*idf_score
		score_item = [doc_id, tf_idf]
		score_list.append(score_item)
	return score_list

#method scores the documents by query
def score_query(score_sheet):
	doc_scores = {}
	for entry in score_sheet:
		doc_id = entry[0]
		score = entry[1]
		if doc_id not in doc_scores:
			doc_scores[doc_id] = score
		else:
			current_score = doc_scores[doc_id]
			new_score = current_score + score
			doc_scores[doc_id] = new_score
	list_total_score = []
	for item in doc_scores:
		score = doc_scores[item]
		entry = [item, score]
		list_total_score.append(entry)
	#sort by doc score
	list_total_score.sort(key=itemgetter(1))
	output = score_to_string(list_total_score)
	return output
		
#score to string method
def score_to_string(list):
	if list.length <= 10:
		output = str(list[0][0])
		for item in list in range(1, list.length-1):
			output = output + " " + str(item[0])
		return output
	else:
		top10 = list[:10]
		output = str(list[0][0])
		for item in top10 in range(1,9):
			output = output + " " + str(item[0])
		return output
		
#lines below run the methods defined above
load_dic()
read_queries()