import re
import json
from textblob import TextBlob
from collections import defaultdict 

DROP_TAG = set(['CC', 'CD', 'DT', 'EX', 'IN', 'MD', 'NNP', 'NNPS', 
                'POS', 'PRP', 'PRP$', 'SYM', 'TO', 'UH', 'WDT', 'WP', 'WRB'])

# Find relevant info about business: state and category
def business_dict(file_path): 
    business_lookup = {}
    with open(file_path) as data_file: 
        for line in data_file: 
            business_data = json.loads(line)
            business_id = business_data['business_id']
            state = business_data['state']
            category = business_data['categories']
            if business_lookup.get(business_id) is not None: 
                print "%s not uniuqe" % business_id
                break
            business_lookup[business_id] = (state, category)
    return business_lookup

# Count word frequencies by sentiment
def sentiment_dict(file_path, review): 
    n, num_positive, num_negative = 0, 0, 0
    sentiment_dict = defaultdict(lambda: [0,0])
    with open(file_path, 'rb') as text_file: 
        for line in text_file: 
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
    print "{0} positive reviews and {1} negative reviews".format(num_positive, num_negative)
    return sentiment_dict, num_positive, num_negative