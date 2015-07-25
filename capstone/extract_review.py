from __future__ import division
import re
import math
import pandas
from textblob import TextBlob
from collections import defaultdict
""" POS tag reference
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
"""
DROP_TAG = set(['CC', 'CD', 'DT', 'EX', 'IN', 'MD', 'NNP', 'NNPS', 
                'POS', 'PRP', 'PRP$', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WRB'])
DROP_WORD = set(['also', 'anyone', 'asked', 'been', 'did', 'ever', 'get', 
                 'have', 'had', 'just', 'make', 'next', 'not', 'only', 'recommend', 
                 'said', 'someone', 'then', 'told', 'very', 'was', 'were'])
review = pandas.read_csv('Documents/Thinkful Project/yelp_review.csv')
n, num_positive, num_negative = 0, 0, 0
sentiment_dict = defaultdict(lambda: [0,0])
common_words, bias_words = {}, {}

# Do some word counts as next-step filters
with open('Documents/Thinkful Project/yelp_text.txt', 'rb') as text: 
    for line in text: 
        if n % 50000 == 0: print n
        line_clean = re.sub('\.{2,}', ', ', line.decode('utf8').rstrip('\n'))
        blob_review = TextBlob(line_clean).lower()
        word_set = set(blob_review.tags)
        star = review['rating'][n]
        if star >= 4: 
            num_positive += 1
            for word in word_set: 
                if word[1] not in DROP_TAG: sentiment_dict[word][0] += 1
        elif star <= 2: 
            num_negative += 1
            for word in word_set: 
                if word[1] not in DROP_TAG: sentiment_dict[word][1] += 1
        n += 1
for k, v in sentiment_dict.iteritems(): 
    pos_freq, neg_freq = v[0]/num_positive, v[1]/num_negative
    if pos_freq > 0.3 and neg_freq > 0.3 and abs(math.log(pos_freq/neg_freq)) < 0.1: 
        common_words[k] = (pos_freq, neg_freq)
    if pos_freq > 0.005 and neg_freq > 0.005 and abs(math.log(pos_freq/neg_freq)) > 1: 
        bias_words[k] = (pos_freq, neg_freq)

# 2nd Run - Use the filters to generate positive/negative word baskets
n = 0
with open('Documents/Thinkful Project/yelp_text.txt', 'rb') as text: 
    with open('Documents/Thinkful Project/all_review.basket', 'w') as output: 
        for line in text: 
            if n % 50000 == 0: print n
            star = review['rating'][n]
            if star == 3: 
                n += 1
                continue
            line_clean = re.sub('\.{2,}', ', ', line.decode('utf8').rstrip('\n')).replace('=', ' ')
            blob_review = TextBlob(line_clean)
            word_set = set(blob_review.tags) 
            word_set -= set(common_words.keys())
            word_list = []
            for word in word_set: 
                if word[1] in DROP_TAG or 'http' in word[0] \
                or word[0].lower() in DROP_WORD or len(word[0]) <= 2: continue
                word_list.append(word[0].lower())
            word_string = ','.join(set(word_list))
            if star >= 4:  word_string += ',+'
            elif star <= 2: word_string += ',-'
            output.write(word_string.encode('utf8') + '\n')
            n += 1