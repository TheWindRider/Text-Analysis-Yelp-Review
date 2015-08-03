from __future__ import division
import re
import imp
import math
import pandas
from textblob import TextBlob

""" POS tag reference
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
"""
DROP_TAG = set(['CC', 'CD', 'DT', 'EX', 'IN', 'MD', 'NNP', 'NNPS', 
                'POS', 'PRP', 'PRP$', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WRB'])
DROP_WORD = set(['also', 'anyone', 'asked', 'been', 'did', 'even', 'ever', 'get', 'good', 'got', 
                 'have', 'had', 'just', 'make', 'next', 'not', 'only', 'other', 
                 'recommend', 'said', 'someone', 'then', 'told', 'very', 'was', 'were'])
KEY_WORD = set(['burger', 'hamburger', 'burgers', 'hamburgers'])

YELP_LKP_FILE ='Documents/Thinkful Project/thinkful course/capstone/yelp_lookup.py'
YELP_BIZ_FILE = 'Canopy/Data/yelp_challenge/business.json'
REVIEW_SUM_FILE = 'Documents/Thinkful Project/yelp_review.csv'
REVIEW_TEXT_FILE = 'Documents/Thinkful Project/yelp_text.txt'

review = pandas.read_csv(REVIEW_SUM_FILE)
lookup = imp.load_source('', YELP_LKP_FILE)
business_info = lookup.business_dict(YELP_BIZ_FILE)
sentiment_dict, num_positive, num_negative = lookup.sentiment_dict(REVIEW_TEXT_FILE, review)

common_words, bias_words = {}, {}
for k, v in sentiment_dict.iteritems(): 
    pos_freq, neg_freq = v[0]/num_positive, v[1]/num_negative
    if pos_freq > 0.25 and neg_freq > 0.25 and abs(math.log(pos_freq/neg_freq)) < 0.1: 
        common_words[k] = (pos_freq, neg_freq)
    if pos_freq > 0.005 and neg_freq > 0.005 and abs(math.log(pos_freq/neg_freq)) > 1: 
        bias_words[k] = (pos_freq, neg_freq)

def word_basket(review, business_info, key_word): 
    basket_file = ''
    if len(key_word) == 0: basket_file = 'Documents/Thinkful Project/all_review.basket'
    else: basket_file = 'Documents/Thinkful Project/keyword_review.basket'
    n = 0
    with open(REVIEW_TEXT_FILE, 'rb') as text: 
        with open(basket_file, 'w') as output: 
            for line in text: 
                star = review['rating'][n]
                labels = business_info[review['business_id'][n]][1]
                line_clean = re.sub('\.{2,}', ', ', line.decode('utf8').rstrip('\n')).replace('=', ' ')
                blob_review = TextBlob(line_clean)
                word_set = set(blob_review.tags) - set(common_words.keys())
                word_list = []
                for word in word_set: 
                    condition_1 = word[1] in DROP_TAG or word[0].lower() in DROP_WORD
                    condition_2 = 'http' in word[0] or len(word[0]) <= 2
                    if condition_1 or condition_2: continue
                    word_list.extend(word[0].lower().split(','))
                condition = True
                if len(key_word) == 0: 
                    condition = len(set(word_list)) == 0
                    word_set = set(word_list) | set(labels)
                else: 
                    condition = len(set(word_list) & key_word) == 0
                    word_set = set(word_list) - key_word
                if condition or star == 3: 
                    n += 1
                    continue
                word_string = ','.join(word_set)
                if star >= 4: word_string += ',+'
                elif star <= 2: word_string += ',-'
                output.write(word_string.encode('utf8') + '\n')
                n += 1