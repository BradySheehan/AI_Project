import os
import sys
import operator
import re
import string

# note that the author class returns the works as a string and not as a list
class Author:
	def __init__(self, name):
		self.name = name;
		self.works = []; #strings referencing the work

	def getNoStopWords(self, work):
		return "";

	def getNoPunctuation(self, work):
		return "";

	# get the work as a string with normalized white space
	def getWork(self, workIndex):
		original = ''.join(open(self.works[workIndex], "r").read().split());
		return original;


# CURRENTLY THE FEATURES ARE ONLY WORKING WITH THE ORIGINAL WORK
# but it would be easy to change self.work to the file as a string
# with whatever characteristics we want
class Features:
	def __init__(self, author, workIndex):
		self.author = author;
		self.workIndex = workIndex;
		self.wordCount = self.getWordCount();
		self.work = author.getWork(workIndex);
		# self.avgWordLength = self.getAvgWordLength();
		# self.avgSenLength = self.getAvgSenLength();
		# self.wordLengthPercentages = self.getWordLengthPercentages();
		# self.senLengthPercentages = self.getSenLengthPercentages();
		# self.featureVector = self.getFeatureVector();

	# get the average word length of this work
	# (the sum of all the word lengths divided by the total number of words)
	# COULD CHOOSE TO IGNORE OR NOT IGNORE STOP WORDS
	def getAvgWordLength(self):
		words = self.split(" ");
		wordLengthsTotal = 0;
		for i in range(0, len(words)):
			wordLengthsTotal = wordLengthsTotal + len(words[i]);
		return float(wordLengthsTotal)/self.wordCount;

	# calculate the average number of words per sentence
	def getAvgSenLength(self):
		numSentences = len(re.findAll(r'[!.?]', self.work));
		return self.wordCount/numSentences;

	# create a vector of percentage for each word length 'n' in [0-10,11+]
	def getWordLengthPercentages(self):
		return 0.0;

	# create a vector of sentence length percentages for each sentence length in [?]
	def getSenLengthPercentages(self):
		return 0.0;

	def getWordCount(self):
		wordCount = len(re.findAll(r'\w+', self.work));
		return wordCount;

	# concatenate all of the above features into a numerical vector
	# this will need to be changes because the last two fields will be vectors
	def getFeatureVector(self):
		vector = [];
		vector.append(self.avgWordLength);
		vector.append(self.avgSenLength);
		vector.append(self.wordLengthPercentages);
		vector.append(self.senLengthPercentages);
		return vector;

# Class creates objects for each author in the directory structure
class Corpus:
	def __init__(self):
		self.authors = [];
		# names = ['Bronte','Collins','Dickens','Ibsen','James','Jewett','Meredith','Phillips','Shaw','Thackeray','Trollope','Wharton'];
		# self.names = ['A','B']; # temp for now
		self.authornames = [];
		self.initializeAuthors();

	def initializeAuthors(self):
		self.authornames = os.listdir("../authors/");
		for name in self.authornames:
			a = Author(name);
			a.works = os.listdir("../authors/"+name);
			self.authors.append(a);

	def printAuthorsAndWorks(self):
		for author in self.authors:
			print "Author: " + author.name;
			for i in range(0, len(author.works)):
				print "\tWork " + str(i) + ":\t" + author.works[i];

# Each input pair is two sets of vectors (possibly a vector of vectors)
# that define one input that will be given to the neural network
class InputPair:
	def __init__(self, work1, authorIndex1, work2, authorIndex2):
		self.author1 = authorIndex1;
		self.author2 = authorIndex2;
		self.work1 = work1;
		self.work2 = work2;
		self.feature1;
		self.feature2;
		self.initializeFeatureVectors();

	def initializeFeatureVectors():
		self.feature1 = Features(self.work1, self.author1);
		self.feature2 = Features(self.work2, self.author2);

	def printFeatureVectors():
		print "Author1: " + self.author1.name;
		print "\tFeatures: " + self.feature1;
		print "\nAuthor2: " + self.author2.name;
		print "\tFeatures: " + self.feature1;

a = Corpus();
a.printAuthorsAndWorks();

# # create an Author object for each author
# for name in range(0, len(names)):
# 	authors.append(Author(names[name]));

# # populate the Author's work list, then calculate a feature vector for each work
# for author in range(0, len(authors)):
# 	authors[author].works = os.listdir("../authors/" + names[author]);
# 	print authors[author].works;
# 	thisAuthorsWorks = authors[author].works;
# 	for work in range(0, len(thisAuthorsWorks)): # for each work by this Author, calculate the features
# 		features = Features(thisAuthorsWorks[work], author);
# 		vector = features.createFeatureVector();
# 		for feature in range(0, len(vector)):
# 			print vector[feature];
# 		print;




