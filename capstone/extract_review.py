import pandas
import operator
from textblob import TextBlob
from collections import defaultdict
""" POS tag reference
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
"""
KEEP_TAG = set(['JJ', 'RB'])
review = pandas.read_csv('Documents/Thinkful Project/yelp_review.csv')
n = 0
positive_dict, negative_dict = defaultdict(int), defaultdict(int)
sentiment_dict = {}
with open('Documents/Thinkful Project/yelp_text.txt', 'rb') as text: 
    for line in text: 
        n += 1
        blob_review = TextBlob(line.decode('utf8').rstrip('\n')).lower()
        word_set = set(blob_review.tags)
        if review['rating'][n-1] >= 4: 
            for word in word_set: 
                positive_dict[word] += 1
        elif review['rating'][n-1] <= 2: 
            for word in word_set: 
                negative_dict[word] += 1
"""
sorted_pos = sorted(positive_dict.items(), key=operator.itemgetter(1), reverse=True)
sentiment_dict = dict(positive_dict.items() + negative_dict.items() + 
                     [(k, [positive_dict[k], negative_dict[k]]) for k in 
                       set(positive_dict) & set(negative_dict)])
"""
for k, v in positive_dict.iteritems(): 
    if negative_dict.get(k) is None: 
        sentiment_dict[k] = [v, 0]
    else: 
        sentiment_dict[k] = [v, negative_dict[k]]
        del negative_dict[k]
for k, v in negative_dict.iteritems(): 
    sentiment_dict[k] = [0, v]