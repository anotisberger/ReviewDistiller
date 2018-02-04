#!/usr/bin/env python3
# Created by Ayelet Berger.
# Last modified on 2/2/2018.
# Helper functions that are used in more than one script.

import nltk
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import re

def make_stoplist(doctor_list):
	'''Make a stoplist that includes the doctor names'''

	# collect doctor names to include in stopwords:
	doctor_names = [[name for name in re.findall('\w+',full_name.lower())] for full_name in doctor_list]
	flattened_doctor_names = []
	for full_name in doctor_names:
		for name_part in full_name:
			flattened_doctor_names.append(name_part)

	flattened_doctor_names = list(set(flattened_doctor_names))

	stoplist = set(nltk.corpus.stopwords.words('english') + list(ENGLISH_STOP_WORDS)
			+ ['doctor','dr'] + flattened_doctor_names)

	return stoplist

def get_tokens(review,stoplist):
	'''Split a review into individual words and keep all the words that are longer than one character.'''
	tokens = []
	for word in re.findall('\\w+',review.lower()):
		if (len(word)>1 and word not in stoplist):
			tokens.append(word)
	return(tokens)


