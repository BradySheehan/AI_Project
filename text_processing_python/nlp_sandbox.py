import os
import sys
import operator
import re
import string


# TODO
	# determine which of the features are useful
	# do something with the n-grams
	# determine how to convert non-numeric values

class Author:
	def __init__(self, name, file):
		self.name = name;
		self.file = file;
		self.features = self.getFeatureVector(file);
		self.printFeatures();
		
	# can either print this all to a file or print it to console
	def printFeatures(self):
		for i in range(0, len(self.features)):
			print self.features[i],
		print;
		
	# creates the vector of features to be plugged into the Neural Net (much more to add)
	def getFeatureVector(self, file):
		features = [];
		features.append(file.averageWordLength);
		features.append(file.averageSentenceLength);
		for i in range(0, len(file.frequencies)):
			features.append(file.frequencies[i]);
		# for i in range(0, len(file.rarestWords)):
			# features.append(self.toBinary(file.rarestWords[i]));
		return features;
		
	# this is a pretty dumb, probably useless generic function for converting a string its binary representation
	# we probably want the type of conversion we did for Simon
	def toBinary(self, word):
		converted = ' '.join(format(ord(letter), 'b') for letter in word);
		print converted;


# should we make a class of features and seperate the file itself in a class from the features
# we compute from it??
# We also need to figure out how to convert all these metrics to numeric values (which might
# 	be a seperate class)

class File:
	path = "";
	uniqueWords = {};
	mostCommonWord = "";
	biGrams = [];
	triGrams = [];
	quadGrams = [];
	content = "";
	averageWordLength = 0;
	contentNoPunctuation = "";
	mostCommonFirstWord = 0;
	rarestWords = {};
	wordFrequency = {};
	numWords = 0;
	frequencies = [];
	# numWords;
	
	def __init__(self, path):
		self.path = path;
		self.content = self.getContent();
		self.contentNoPunctuation = self.getContentNoPunctuation();
		self.numWords = self.getNumWords();
		self.uniqueWords = self.getUniqueWords();
		self.mostCommonWord = self.getMostCommonWord();
		# self.biGrams = self.getNGrams(2);
		# self.triGrams = self.getNGrams(3);
		# self.quadGrams = self.getNGrams(4);
		self.averageSentenceLength = self.getAverageSentenceLength();
		self.averageWordLength = self.getAverageWordLength();
		self.contentNoPunctuation = self.getContentNoPunctuation();
		self.mostCommonFirstWord = self.getMostCommonFirstWord();
		self.wordFrequency = self.getWordsWithFrequency(50);
		self.rarestWords = self.getRarestWords(self.uniqueWords); 
		self.frequencies = self.getWordLengthFrequencies(self.contentNoPunctuation);

	def printFields(self):
		# print "Content:", self.content;
		# print "Word Count:", self.uniqueWords;
		# print "Most Common Word:", self.mostCommonWord;
		# print "\nBi-grams:", self.biGrams;
		# print "\nTri-grams:", self.triGrams;
		# print "\nQuad-grams:", self.quadGrams;
		# print "\nAverage Word Length:", self.averageWordLength, " letters";
		print "\nAverage Sentence Length: ", self.averageSentenceLength;
		# print "\nFILE no punctuation", self.contentNoPunctuation;
		# print "\nMost Common First Word: ", self.mostCommonFirstWord;
		# print "\nWords with frequency 50+: ", self.wordFrequency;
		print "\nRarest Words:", self.rarestWords;
		# print self.contentNoPunctuation;
		print "Word Length Frequencies:", self.frequencies;
		# print self.contentNoPunctuation;
		# self.toBinary("Hello there");

	# return entire file
	def getContent(self):
		content = open(self.path, "r").read();
		return content;

	def getNumWords(self):
		return len(self.contentNoPunctuation.split(" "));
	# return average sentence length
	def getAverageSentenceLength(self):
		# i don't think counting words this way will work unless you do it on the no punctuation file
		# since documents like the constitutition have weird punctuation attached to words
		# numWords = len(self.content.split(" ")); 
		# print "Number of Words =", self.numWords;
		numPeriods = self.content.count(".");
		averageSentenceLength = self.numWords/numPeriods;
		return averageSentenceLength;

	# return entire file without the punctuation
	def getContentNoPunctuation(self):
		f = open(self.path,"r");
		contentNoPunctuation = "";
		for line in f:
			contentNoPunctuation = contentNoPunctuation + re.sub('\W', ' ', str.replace(line, '\s+', ' ')).lower();
		return contentNoPunctuation;

	# average word length of the entire file
	def getAverageWordLength(self):
		words = self.contentNoPunctuation.split(" ");
		totalLength = 0;
		for i in range(0, self.numWords):
			totalLength = totalLength + len(words[i]);
		avgWordLength = totalLength/len(words);
		return avgWordLength;
			
	# frequencies of word lengths over entire document (percentage of 1-length words is stored at [0])
	def getWordLengthFrequencies(self, contentNoPunctuation):
		self.frequencies = 11 * [0];
		contentSplit = contentNoPunctuation.split();
		for i in range(0, len(contentSplit)):
			if len(contentSplit[i]) > 10:
				self.frequencies[10] = self.frequencies[10] + 1;
			else:
				self.frequencies[len(contentSplit[i])-1] = self.frequencies[len(contentSplit[i])-1] + 1;
		totalWords = 0;
		for i in range(0, len(self.frequencies)):
			totalWords = totalWords + self.frequencies[i];
		for i in range(0, len(self.frequencies)):
			self.frequencies[i] = float(self.frequencies[i]) / float(totalWords);
		return self.frequencies;
		
	# create dictionary for words and their number of occurences
	def getUniqueWords(self):
		uniqueWords = {};
		content2 = self.contentNoPunctuation.lower();
		words = content2.split(" ");
		for i in range(0, len(words)):
			if words[i] in uniqueWords and words[i] != '':
				uniqueWords[words[i]] = uniqueWords[words[i]] + 1;
			else:
				uniqueWords[words[i]] = 1;
		return uniqueWords;

	# most common word overall
	def getMostCommonWord(self):
		mostCommonWord = max(self.uniqueWords.iteritems(), key = operator.itemgetter(1))[0];
		return mostCommonWord;

	# n-grams as specified by argument passed
	def getNGrams(self, n):
		j = 0;
		nGrams = [];
		for i in range(j, len(self.content)):
			nGrams.append(self.content[i : (i + n)]);
			j = j + 1;
		return nGrams;

	def getMostCommonFirstWord(self):
		firstWords = {};
		content2 = re.sub('[\n]', ' ', self.content, flags = re.MULTILINE);
		content2 = re.sub("\s\s+", " ", content2);
		content2 = re.sub('^.\w|,|:|;', ' ', content2);
		content2 = re.sub('[--]', ' ', content2);
		words = content2.split(" ");
		for i in range(0,len(words)):
			str1 = re.match('\w+.', words[i], re.IGNORECASE);
			if str1 and i+1 != len(words) and words[i+1] != '':
				if firstWords.has_key(words[i+1]):
					firstWords.update({words[i+1]:firstWords[words[i+1]] + 1});
				else:
					firstWords.update({words[i+1]:1});
		mostCommonFirsWord = max(firstWords.iterkeys(), key = lambda k: firstWords[k]);
		return mostCommonFirsWord;

	def getWordsWithFrequency(self, frequency):
		wordFreq = {};
		for key, value in self.uniqueWords.iteritems():
			if value >= frequency:
				wordFreq.update({key:value});
		return wordFreq;

	# get all the words in this file that occur between 15 and 25 times
	def getRarestWords(self, wordCount):
		sortedWordCount = sorted(wordCount.items(), key = operator.itemgetter(1));
		rarestN = [];
		# for i in range(n, n + 500):
			# a,b = zip(sortedWordCount[i]);
			# str1 = re.match('\w+', ''.join(a), re.IGNORECASE);
			# if str1:
				# rarestN.append(sortedWordCount[i]);
		for i in wordCount:
			if wordCount[i] >= 15 and wordCount[i] <= 25:
				rarestN.append(i);
		return rarestN;


# file = File("Victorian_novels_from_PJ/Collins_50Anton.txt");
# file.printFields();

authors = ['Bronte','Collins','Dickens','Ibsen','James','Jewett','Meredith','Phillips','Shaw','Thackeray','Trollope','Wharton'];
for name in authors:
	print "NAME: " + name;
	file = File("/Users/matthewsobocinski/Desktop/Folders/AI/Project/output/" + name + ".txt");
	# file.printFields();
	author = Author(name, file);
	print;