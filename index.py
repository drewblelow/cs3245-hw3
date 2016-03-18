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
from nltk.stem.porter import PorterStemmer

#use message
def usage():
	print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

#default settings
directory_path = "D:\\Python27\\Lib\\site-packages\\nltk\\nltk_data\\corpora\\reuters\\training"
dictionary_file = "dictionary.txt"
postings_file = "postings.txt"

#variables
DICTIONARY = {}
LIST_DOC = []

#specified settings
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-i':
        directory_path = a
    elif o == '-d':
        dictionary_file = a
    elif o == '-p':
        postings_file = a
    else:
        assert False, "unhandled option"

#filepath handling for specified options			
if directory_path == "" or directory_path == None or dictionary_file == "" or dictionary_file == None or postings_file == None or postings_file == "":
    usage()
    sys.exit(2)

#get all files from specified path
files_to_index = [f for f in listdir(directory_path) if isfile(join(directory_path, f))]

#indexer methods	
#main indexing method to call other sub methods
def indexer():
	print("start indexing all files in"),
	print(directory_path),
	print("..."),
	#calls indexing method for files in the for loop
	for current_file in files_to_index:
		index_file(current_file)
	#calls write methods to dictionary.txt and postings.txt
	writeout()
	print "[DONE]"
	
#indexes documents with frequency included
def index_file(file):	
	filename = basename(file)
	filepath = directory_path + os.path.sep + filename
	filetxt = open(filepath).read()
	#words are split by regex, entered into dict
	words = re.findall(r"[a-zA-Z]+(?:'[a-z])?", filetxt)
	#to lower case, eliminate casing duplicates in dic
	words = [element.lower() for element in words]
	wordlist = {}
	stemmer = PorterStemmer()
	for word in words:
		stemmed = stemmer.stem(word)
		if word not in wordlist:
			wordlist[word] = 1
		else:
			freq = wordlist[word]
			freq = freq + 1
			wordlist[word] = freq
	for word in wordlist:
		frequency = wordlist[word]
		posting = [filename, frequency]
		if word not in DICTIONARY:
			DICTIONARY[word] = posting
		else:
			postings = DICTIONARY[word]
			postings.append(posting)
			DICTIONARY[word] = postings
	LIST_DOC.append([filename, count])			
	
#method to write to external files
def writeout():
	write_dic = open(dictionary_file, 'w')
	write_pos = open(postings_file, 'w')
	for word in DICTIONARY:
		postings = DICTIONARY[word]
		pointer = write_pos.tell()
		for item in postings:
			doc_id = item[0]
			freq = item[1]
			write_pos.write(doc_id + "_" + str(freq) + " ")
		write_dic.write(word + "^" + str(pointer) + " "),
		write_pos.write('\n')
	write_dic.write("\n")
	for item in LIST_DOC:
		filename = item[0]
		numwords = item[1]
		write_dic.write(filename + "_" + str(numwords) + " ")

#method to view dictionary, debugging use only
def view_dictionary():
	for word in DICTIONARY:
		print word,
		postings = DICTIONARY[word]
		for post in postings:
			print post,
		print "\n"
		
#lines below run the methods defined above	
indexer()