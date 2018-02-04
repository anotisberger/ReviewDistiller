#!/usr/bin/env python3
# Created by Ayelet Berger.
# Last modified on 2/2/2018.
# Code for scraping doctor review data from ZocDoc website

# Import required libraries:
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from time import time
from helper_functions.web_scraping import scrape_comments

def make_url_list():
	'''This function makes a list of all the search page url's for primary care
	physicians in Manhattan'''
	
	# First make a list of search pages to scrape. 
	# I copied and pasted urls for the results of search pages when 
	# I search for primary care physiscians in each zip code in Manhattan. 
	url_list_10001 = ['https://www.zocdoc.com/search?address=10001&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10002 = ['https://www.zocdoc.com/search?address=10002&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10003 = ['https://www.zocdoc.com/search?address=10003&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10003&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10003&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=a7d4f1e2-3cce-4131-b9b3-7b3c212c8741&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10004 = []
	url_list_10005 = []
	url_list_10006 = ['https://www.zocdoc.com/search?address=10006&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10007 = ['https://www.zocdoc.com/search?address=10007&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10009 = ['https://www.zocdoc.com/search?address=10009&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10010 = ['https://www.zocdoc.com/search?address=10010&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10011 = ['https://www.zocdoc.com/search?address=10011&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10011&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10011&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=09eedb5b-f78f-4033-91e6-8b6e6ae399b2&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false'
						'https://www.zocdoc.com/search?address=10011&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10011&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=20&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=66676b40-8af5-41dc-8762-903971892eba&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10012 = ['https://www.zocdoc.com/search?address=10012&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10013 = ['https://www.zocdoc.com/search?address=10013&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10014 = ['https://www.zocdoc.com/search?address=10014&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10016 = ['https://www.zocdoc.com/search?address=10016&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10016&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10016&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=88d02270-37ee-41e4-8b98-0d87aa4db032&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false',
						'https://www.zocdoc.com/search?address=10016&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10016&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=20&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=2f4eeda5-bae0-40bb-97f5-a123ccb97d03&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false',
						'https://www.zocdoc.com/search?address=10016&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10016&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=30&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=75ce2aec-171c-4fdc-b86f-209038d604f9&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10017 = ['https://www.zocdoc.com/search?address=10017&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10017&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10017&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=acd80637-00ff-4868-9bbc-99c8075dfdd7&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10018 = []
	url_list_10019 = ['https://www.zocdoc.com/search?address=10019&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10019&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10019&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=48779927-b043-4022-b858-b976a76317c1&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false',
						'https://www.zocdoc.com/search?address=10019&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10019&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=20&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=4ecf31ba-21b9-4c5a-af3e-a0765408ea12&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10020 = []
	url_list_10021 = ['https://www.zocdoc.com/search?address=10021&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10021&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10021&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=677d695a-e173-436f-9fdc-268a029fe175&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10022 = ['https://www.zocdoc.com/search?address=10022&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10022&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10022&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=848f2bd3-083e-4185-89c6-60ed429a70d6&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10023 = ['https://www.zocdoc.com/search?address=10023&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10023&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10023&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=1c58cda9-83f5-4483-be1b-51d74befc62d&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10024 = ['https://www.zocdoc.com/search?address=10024&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10025 = ['https://www.zocdoc.com/search?address=10025&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10025&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10025&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=3610a4e1-8268-48cf-b4a4-21b532f6a495&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false',
						'https://www.zocdoc.com/search?address=10025&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10025&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=20&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=deba01cb-c661-4f16-b0cc-5d06da1741e2&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10026 = ['https://www.zocdoc.com/search?address=10026&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10027 = ['https://www.zocdoc.com/search?address=10027&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10028 = ['https://www.zocdoc.com/search?address=10028&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10028&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10028&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=8a6dd473-0f33-4eff-ad8c-5911f9208c51&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false',
						'https://www.zocdoc.com/search?address=10028&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10028&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=20&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=ef426a6d-cded-4401-bec3-4043ccac1b10&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10029 = ['https://www.zocdoc.com/search?address=10029&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10030 = []
	url_list_10031 = ['https://www.zocdoc.com/search?address=10031&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10032 = ['https://www.zocdoc.com/search?address=10032&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10033 = ['https://www.zocdoc.com/search?address=10033&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10034 = ['https://www.zocdoc.com/search?address=10034&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10035 = ['https://www.zocdoc.com/search?address=10035&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10036 = ['https://www.zocdoc.com/search?address=10036&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10037 = ['https://www.zocdoc.com/search?address=10037&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10038 = ['https://www.zocdoc.com/search?address=10038&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10039 = ['https://www.zocdoc.com/search?address=10039&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10040 = ['https://www.zocdoc.com/search?address=10040&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10044 = []
	url_list_10065 = ['https://www.zocdoc.com/search?address=10065&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10075 = ['https://www.zocdoc.com/search?address=10075&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241']
	url_list_10128 = ['https://www.zocdoc.com/search?address=10128&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241',
						'https://www.zocdoc.com/search?address=10128&insurance_carrier=-1&day_filter=AnyDay&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=75&after_5pm=false&before_10am=false&sees_children=false&sort_type=Default&dr_specialty=153&ip=69.202.128.241#dr_specialty=153&address=10128&insurance_carrier=-1&insurance_plan=-1&reason_visit=75&gender=-1&language=-1&PatientTypeChild=&offset=10&referrerType=&sort_selection=0&name=&searchQuery=&searchQueryGuid=78a36a7b-7da8-4fbe-99c0-ce267ff0737c&hasNoSearchResults=false&hospitalid=-1&timeFilter=AnyTime&dayFilter=0&procedureChanged=false&languageChanged=false']
	url_list_10280 = []

	all_urls_list = list(set(url_list_10001)|set(url_list_10002)|
	                set(url_list_10003)|set(url_list_10004)|set(url_list_10005)|
	                set(url_list_10006)|set(url_list_10007)|set(url_list_10009)|
					set(url_list_10010)|set(url_list_10011)|set(url_list_10012)|
					set(url_list_10013)|set(url_list_10014)|set(url_list_10016)|
					set(url_list_10017)|set(url_list_10018)|set(url_list_10019)|
					set(url_list_10020)|set(url_list_10021)|set(url_list_10022)|
					set(url_list_10023)|set(url_list_10024)|set(url_list_10025)|
					set(url_list_10026)|set(url_list_10027)|set(url_list_10028)|
					set(url_list_10029)|set(url_list_10030)|set(url_list_10031)|
					set(url_list_10032)|set(url_list_10033)|set(url_list_10034)|
					set(url_list_10035)|set(url_list_10036)|set(url_list_10037)|
					set(url_list_10038)|set(url_list_10039)|set(url_list_10040)|
					set(url_list_10044)|set(url_list_10065)|set(url_list_10075)|
					set(url_list_10128)|set(url_list_10280))

	return all_urls_list



def get_doctor_links(searchpage_url):	
	'''This function gets all the links to specific doctors on a search page.'''

	r_searchpage = requests.get(searchpage_url)
	html_searchpage = r_searchpage.text
	soup_searchpage = BeautifulSoup(html_searchpage, "html5lib")
	docLinks_searchpage = soup_searchpage.find_all('a','js-profile-link ch-prof-link')
	
	docLinks_searchpage_tags=[]
	
	for item in docLinks_searchpage:
		docLinks_searchpage_tags += [item['href']]

	return docLinks_searchpage_tags


def scrape_all_the_data():
	# does everything
	
	# Make a list of urls to scrape:
	url_list = make_url_list()

	# Get the url extensions for all of the doctors in the search pages:
	all_doctor_tags = []

	for i in url_list:
		all_doctor_tags += get_doctor_links(i)
	
	all_doctor_tags = list(set(all_doctor_tags))

	base_url = 'https://www.zocdoc.com/'

	# Get all of the comments for each doctor and add them to a master dataframe
	all_reviews_combined = pd.DataFrame(columns = ['doctor','author','date',
	                        'verification','review','overall_rating',
	                        'bedside_manner_rating','wait_time_rating'])

	for doctor_tag in all_doctor_tags:
		print(doctor_tag)
		all_reviews_combined = pd.concat([all_reviews_combined,scrape_comments(base_url+doctor_tag)],ignore_index=True)

	all_reviews_combined.to_csv('zoc_doc_reviews_Manhattan.csv')

	
if __name__ == '__main__':
	scrape_all_the_data()