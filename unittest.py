import re

DICTIONARY = {}

def test_indexer_freq():
	file = "sampletext.txt"
	filenumber = 69
	filetxt = open(file).read()
	#words are split by regex, entered into dict
	words = re.findall(r"[a-zA-Z]+(?:'[a-z])?", filetxt)
	#to lower case, eliminate casing duplicates in dic
	words = [element.lower() for element in words]
	wordlist = frequency_processor(words)
	for entry in wordlist:
		word = entry[0]
		freq = entry[1]
		post = [filenumber, freq]
		if word in DICTIONARY:
			postings = DICTIONARY[word]
			postings.append(post)
		else :
			postings = []
			postings.append(post)
			DICTIONARY[word] = postings		
				
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
		
def view_dictionary():
	for word in DICTIONARY:
		print word,
		postings = DICTIONARY[word]
		for post in postings:
			print post,
		print "\n"
		
test_indexer_freq()
view_dictionary()