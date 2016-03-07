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
	print "usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file"

#default settings
directory_path = "D:\\Python27\\Lib\\site-packages\\nltk\\nltk_data\\corpora\\reuters\\training"
dictionary_file = "dictionary.txt"
postings_file = "postings.txt"

#variables
DICTIONARY = {}
INDEX_OPTION = 1
#OPTIONS: 	0 = inverted index
#			1 = doc_freq


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
	if INDEX_OPTION = 0:
		for current_file in files_to_index:
			index_file_inverted(current_file)
	elif INDEX_OPTION = 1:
		for current_file in files_to_index:
			index_file_frequency(current_file)
	#calls write methods to dictionary.txt and postings.txt
	writeout()
	print "[DONE]"
	
#indexer method to add all words from a file to the dictionary and postings (inverted index)
def index_file_inverted(file):
	filename = basename(file)
	filepath = directory_path + os.path.sep + filename
	filetxt = open(filepath).read()
	#words are split by regex (by spaces and punctuation), then entered into the dict
	words = re.findall(r"[a-zA-Z]+(?:'[a-z])?", filetxt)
	words = [element.lower() for element in words]
	for word in words:
		if word in DICTIONARY:
			postings = DICTIONARY[word]
			if filename not in postings:
				postings.append(filename)
		else:
			DICTIONARY[word] = [filename]
	
#indexes documents with frequency included
def index_file_frequency(file):	
	filename = basename(file)
	filepath = directory_path + os.path.sep + filename
	filetxt = open(filepath).read()
	#words are split by regex, entered into dict
	words = re.findall(r"[a-zA-Z]+(?:'[a-z])?", filetxt)
	#to lower case, eliminate casing duplicates in dic
	words = [element.lower() for element in words]
	wordlist = frequency_processor(words)
	for entry in wordlist:
		word = entry[0]
		freq = entry[1]
		post = [filename, freq]
		if word in DICTIONARY:
			postings = DICTIONARY[word]
			postings.append(post)
		else :
			postings = []
			postings.append(post)
			DICTIONARY[word] = postings
	
#word frequency preprocessor
def frequency_processor(wordlist):
	encountered = {}
	end_list = []
	for word in wordlist:
		if word not in encountered:
			encountered[word] = 1
			freq = wordlist.count(word)
			item = [word, freq]
			end_list.append(item)
		#skip if already encountered
	return end_list	
	
#method to write to external files
def writeout():
	write_dic = open(dictionary_file, 'w')
	write_pos = open(postings_file, 'w')
	for word in DICTIONARY:
		postings = DICTIONARY[word]
		pointer = write_pos.tell()
		for item in postings:
			write_pos.write(item + " ")
		write_dic.write(word + "^" + str(pointer) + " "),
		write_pos.write('\n')
	write_dic.write("\n")
	for file in files_to_index:
		filename = basename(file)
		write_dic.write(filename + " ")

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

#view_dictionary()
