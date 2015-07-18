import re
import pandas
from textblob import TextBlob
from __future__ import division
from collections import defaultdict
""" POS tag reference
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
"""
DROP_TAG = set(['CC', 'CD', 'DT', 'IN', 'POS', 'PRP', 'PRP$', 'SYM', 'TO'])
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
                sentiment_dict[word][0] += 1
        elif star <= 2: 
            num_negative += 1
            for word in word_set: 
                sentiment_dict[word][1] += 1
        n += 1
for k, v in sentiment_dict.iteritems(): 
    pos_freq, neg_freq = v[0]/num_positive, v[1]/num_negative
    if pos_freq > 0.4 and neg_freq > 0.4 and abs(math.log(pos_freq/neg_freq)) < 0.1: 
        common_words[k] = (pos_freq, neg_freq)
    if pos_freq > 0.01 and neg_freq > 0.01 and abs(math.log(pos_freq/neg_freq)) > 1: 
        bias_words[k] = (pos_freq, neg_freq)
sentiment_dict = None

# 2nd Run - Use the filters to generate positive/negative word baskets
n = 0
with open('Documents/Thinkful Project/yelp_text.txt', 'rb') as text: 
    with open('Documents/Thinkful Project/positive_review.basket', 'w') as pos_out: 
        with open('Documents/Thinkful Project/negative_review.basket', 'w') as neg_out:
            for line in text: 
                if n % 50000 == 0: print n
                star = review['rating'][n]
                if star == 3: 
                    n += 1
                    continue
                line_clean = re.sub('\.{2,}', ', ', line.decode('utf8').rstrip('\n')).replace('=', ' ')
                blob_review = TextBlob(line_clean).lower()
                word_set = set(blob_review.tags) 
                word_set -= set(common_words.keys())
                word_string = ','.join(x[0] for x in word_set if 
                                       x[1] not in DROP_TAG and 'http' not in x[0])
                if star >= 4: 
                    pos_out.write(word_string.encode('utf8') + '\n')
                elif star <= 2: 
                    neg_out.write(word_string.encode('utf8') + '\n')
                n += 1