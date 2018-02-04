#!/usr/bin/env python3
# Created by Ayelet Berger.
# Last modified on 1/30/2018.

# Import required libraries
import numpy as np
import pandas as pd
from time import time
import requests
from bs4 import BeautifulSoup
import nltk
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import re
from gensim import corpora, models, similarities
from nltk.stem import PorterStemmer
from helper_functions.web_scraping import scrape_comments


def review_to_bow(review,stopword_list,dictionary):

	'''This function turns a review into a bag of words for use in the LDA
	model'''

	# First break up each review into a list of words (exclude stopwords). 
	tokenized_review = [word for word in re.findall('\w+',review.lower()) if 
		word not in stopword_list]	

	# Next stem the words
	ps = PorterStemmer()
	tokenized_and_stemmed_review = [ps.stem(word) for word in tokenized_review]

	# Translate the review into our bag of words model
	processed_review = dictionary.doc2bow(tokenized_and_stemmed_review)

	return processed_review

def get_lda_scores(review_bow, model, num_topics):
	'''This function returns a list of lda scores. Mostly just to reformat
	from the annoying list of tuples that the gensim function spits out'''

	topic_scores_as_tuples = model[review_bow]

	topic_scores = np.zeros(num_topics)

	for score_tuple in topic_scores_as_tuples:
		topic_scores[score_tuple[0]] = score_tuple[1]

	return topic_scores

def choose_topic(lda_scores):
	''' Given the lda_scores of a review (as a list), assign it a topic, or nan if it is 
	not single topic.'''

	topic_id = np.argmax(lda_scores)

	lda_scores.sort()

	if lda_scores[-1] >= 2*lda_scores[-2]:
		return topic_id
	else:
		return np.nan

def choose_a_review_for_each_topic(doctor_df, num_topics):
	'''This function returns a list of reviews that best match each of the
	topics in the lda model.'''

	index_best_for_each_topic = np.zeros(num_topics)

	doctor_df['topic_0_score'] = doctor_df['lda_scores'].apply(lambda x: x[0])
	doctor_df['topic_1_score'] = doctor_df['lda_scores'].apply(lambda x: x[1])
	doctor_df['topic_2_score'] = doctor_df['lda_scores'].apply(lambda x: x[2])

	index_best_for_each_topic[0] = doctor_df['topic_0_score'].argmax()
	index_best_for_each_topic[1] = doctor_df['topic_1_score'].argmax()
	index_best_for_each_topic[2] = doctor_df['topic_2_score'].argmax()

	distilled_reviews = []

	for i in range(num_topics):
		try:
			print(i)
			print(doctor_df.loc[i,'lda_scores'])

			distilled_reviews.append(str(doctor_df.loc[index_best_for_each_topic[i],'review']))

			print()
			print()

		except KeyError:
			distilled_reviews.append('This doctor does not have enough reviews')

	print(distilled_reviews)
	return distilled_reviews


def generate_summary(doctor_url):
	'''
	Chooses best review for each topic, calculates the review distribution 
	(how many reviews are about each topic), and calculates review stats 
	such as how many reviews the doctor has, how many unique patients, 
	'''

	# Load model and dictionary:
	lda_model = models.LdaModel.load('lda_model/lda.model')
	dictionary = corpora.Dictionary.load('lda_model/my_dictionary.dict')
	
	# Number of topics in the LDA model we are using:
	num_topics=3

	# Get the data from the doctor's ZocDoc page
	doctor_df = scrape_comments(doctor_url)

	# Clean up the dataframe to make sure there were no bugs in the website
	# and only use reviews that contain text. 
	doctor_df.drop_duplicates(inplace=True)
	doctor_df.dropna(subset=['review'], inplace=True)

	# Make a list of stopwords to leave out, including the doctor's name. 
	doctor_name = re.findall('\w+', doctor_df.doctor[0].lower())
	stopword_list = set(nltk.corpus.stopwords.words('english') + 
		list(ENGLISH_STOP_WORDS) + ['doctor','dr'] + doctor_name)

	# Create a new column in the dataframe that will contain the reviews
	# represented as a bag of words for the lda model. Also create a column 
	# with a list of LDA scores for each review. 
	doctor_df['clean_reviews'] = doctor_df['review'].apply(lambda x: 
		review_to_bow(x,stopword_list,dictionary))

	doctor_df['lda_scores'] = doctor_df['clean_reviews'].apply(lambda x: 
		get_lda_scores(x,lda_model,num_topics))


	# Choose a review for each topic, and display
	distilled_reviews = choose_a_review_for_each_topic(doctor_df, num_topics)

	# Next, determine what percent of the reviews is talking about which topic.
	doctor_df['topic'] = doctor_df['lda_scores'].apply(lambda x: choose_topic(x))

	num_reviews = int(doctor_df['review'].count())

	review_distribution = np.zeros(num_topics)

	for topic,count in doctor_df['topic'].value_counts().iteritems():
		review_distribution[int(topic)] = int((count/num_reviews)*100)


	# Finally, determine some statistics about this doctor's reviews. 
	# review_stats[0] should be the number of reviews
	# review_stats[1] should be the number of individual patients
	# review_stats[2] should be the number of patients who wrote more than one review. 

	review_stats = [num_reviews,
		len(doctor_df['author'].unique()),
		(doctor_df['author'].value_counts()>1).sum()]

	return distilled_reviews, review_distribution, review_stats


if __name__ == '__main__':

	# Ask for user input, assign to url variable.
	doctor_url = input("Enter the url for a doctor's ZocDoc page: ") # 'https://www.zocdoc.com/doctor/irina-lelchuk-do-66023?LocIdent=57389&reason_visit=75&insuranceCarrier=-1&insurancePlan=-1'

	generate_summary(doctor_url)