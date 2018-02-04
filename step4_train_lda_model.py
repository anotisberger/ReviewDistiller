#!/usr/bin/env python3
# Created by Ayelet Berger.
# Last modified on 1/30/2018.
# Code for training an LDA model

# Import required libraries:
import numpy as np
import pandas as pd

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import re

from gensim.models import Phrases
from gensim import corpora, models, similarities
from helper_functions.nlp_cleaning import make_stoplist, get_tokens



def train_lda_model():
	# train lda model from start to finish
	n_topics = 3
	
	# import data and clean up
	data = pd.read_csv('zoc_doc_reviews_Manhattan.csv')
	data.drop(['Unnamed: 0','verification','overall_rating','bedside_manner_rating','wait_time_rating'], 
		axis=1, inplace= True)
	data.drop_duplicates(inplace=True)
	data.dropna(subset=['review'], inplace=True)
	data.reset_index(inplace=True,drop=True)

	# make a stoplist that includes doctor names
	stoplist = make_stoplist(data['doctor'].unique())

	# Tokenize and lemmatize the reviews and save them in the dataframe.
	data['tokenized_reviews'] = data['review'].apply(lambda x: get_tokens(x,stoplist))

	lemmatizer = WordNetLemmatizer()
	data['lemmatized_reviews']=data['tokenized_reviews'].apply(lambda x: [lemmatizer.lemmatize(token) for token in x])

	# Compute bigrams.
	bigram = Phrases(list(data['tokenized_reviews']),min_count=100)

	# find bigrams in each review and add them to the dataframe
	data['bigrams'] = data['lemmatized_reviews'].apply(lambda x: [b for b in bigram[x] if '_' in b])


	# Next add a column in the dataframe that contains the full tokenized, lemmatized reviews, with the bigrams
	data['lemmatized_reviews_with_bigrams'] = np.nan
	data['lemmatized_reviews_with_bigrams'] = data['lemmatized_reviews']
	for row in range(data.shape[0]):
		for b in data.loc[row,'bigrams']:
			data.loc[row,'lemmatized_reviews_with_bigrams'].append(b)

	# Create a dictionary and prune extremes (words that show up too much or not enough)
	dictionary = corpora.Dictionary(list(data['lemmatized_reviews_with_bigrams']))
	dictionary.filter_extremes(no_below=50,no_above=0.5)

	# Create a corpus using the dictionary to define a bag of words model:
	corpus = [dictionary.doc2bow(doc) for doc in list(data['lemmatized_reviews_with_bigrams'])]

	# Train an lda model:
	ldamodel = models.LdaModel(corpus, id2word=dictionary, num_topics=n_topics)

	# Print topics and see if they make sense
	topic_list = ldamodel.print_topics()
	for index, i in enumerate(topic_list):
		str1 = str(i[1])
		for c in "0123456789+*\".":
			str1 = str1.replace(c, "")
		str1 = str1.replace("  ", " ")
		print(str1)

	# Save the dictionary, corpus, and model for future use
	dictionary.save('/tmp/bag_of_words_test.dict')
	corpora.MmCorpus.serialize('/tmp/bag_of_words_test.mm', corpus)
	ldamodel.save('lda_test.model')


	
if __name__ == '__main__':
	train_lda_model()