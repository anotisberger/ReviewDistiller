#!/usr/bin/env python3
# Created by Ayelet Berger.
# Last modified on 1/31/2018.
# Helper functions for web scraping that are used in more than one script.

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

# These are functions for web scraping that are used in multiple scripts.

def scrape_comments(doctor_url):
    '''This function returns a dataframe with all the reviews for one doctor.'''

    start_time = time()    
    
    # Set up a dataframe
    doctor_df = pd.DataFrame(columns = ['doctor','author','date','verification','review','overall_rating','bedside_manner_rating','wait_time_rating'])
    
    # get the html and extract each review.
    r_doctor=requests.get(doctor_url)
    html_doctor=r_doctor.text
    soup_doctor = BeautifulSoup(html_doctor, "html5lib")
    
    doctor_name = soup_doctor.find_all('h1')[0].contents[1].contents[0]
    
    reviews = soup_doctor.find_all('div','sg-row profile-review')
    
    
    # For each review, extract information for all the fields in the dataframe.
    
    
    num_revs = len(reviews)
    
    for i in range(num_revs):
        try:
            date = reviews[i].contents[1].contents[1].contents[0]
        except:
            date = np.nan
            
        try:
            author = reviews[i].contents[1].contents[3].contents[0]
        except:
            author = np.nan
            
        try:
            verification = reviews[i].contents[1].contents[5].contents[0]
        except:
            verification = np.nan
        
        try:
            overall_rating = str(reviews[i].contents[3].contents[1].contents[1].contents[3])[44:45]
        except:
            overall_rating = np.nan
        
        try:
            bedside_manner_rating = str(reviews[i].contents[3].contents[1].contents[3].contents[3])[44:45]
        except:
            bedside_manner_rating = np.nan
        
        try:
            wait_time_rating = str(reviews[i].contents[3].contents[1].contents[5].contents[3])[44:45]
        except:
            wait_time_rating = np.nan
            
        try:
            review = reviews[i].contents[3].contents[3].contents[1].contents[1].contents[0]
        except:
            review = np.nan

        doctor_df.loc[i] = [doctor_name,author,date,verification,review,
            overall_rating,bedside_manner_rating,wait_time_rating]
    print(time()-start_time)
	
    return doctor_df
