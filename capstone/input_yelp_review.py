import json
import numpy
import pylab
import pandas
import random
import matplotlib.pyplot as plt
from collections import defaultdict
from textblob import TextBlob

US_STATES = set(['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA', 
                 'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
                 'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
                 'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
                 'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'])

# Used to filter business by state
business_state = {}
with open('Canopy/Data/yelp_challenge/business.json') as data_file: 
    for line in data_file: 
        business_data = json.loads(line)
        business_id = business_data['business_id']
        state = business_data['state']
        if business_state.get(business_id) is not None: 
            print "%s not uniuqe" % business_id
            break
        business_state[business_id] = state

# Generate light-weight dataframw without review text
business, user, review, rating, sentiment = [], [], [], [], []
with open('Canopy/Data/yelp_challenge/review.json') as data_file: 
    for line in data_file: 
        review_data = json.loads(line)
        if business_state[review_data['business_id']] not in US_STATES: 
            if len(review_data['text']) < 3: 
                continue
            blob_review = TextBlob(review_data['text'])
            if blob_review.detect_language() != 'en': 
                continue
        business.append(review_data['business_id'])
        user.append(review_data['user_id'])
        review.append(review_data['text'])
        rating.append(review_data['stars'])
for each_review in review: 
    blob_review = TextBlob(each_review)
    sentiment.append(blob_review.sentiment)
summary = pandas.DataFrame({'business_id': business, 'user_id': user, 'rating': rating, 
                            'polarity': [x.polarity for x in sentiment], 
                            'subjectivity': [x.subjectivity for x in sentiment]})
summary.to_csv('Documents/Thinkful Project/yelp_review.csv', sep=',', index=False)

# Data for exploratory analysis
review = pandas.read_csv('Documents/Thinkful Project/yelp_review.csv')
n = 0
with open('Canopy/Data/yelp_challenge/review.json') as data_file: 
    for line in data_file: 
        n += 1
        if n < 1: continue
        if n > 10: break
        review_data = json.loads(line)
        blob_review = TextBlob(review_data['text'])
        print review_data['stars'], blob_review.sentiment.polarity
        print review_data['text'][0:200]

# Sentiment - Rating correlation
review.groupby('rating')['polarity'].describe()
review_sample = review.sample(frac=0.01)
fig = plt.figure()
plot = fig.add_subplot(1,1,1)
plot.scatter(review_sample['polarity'], review_sample['subjectivity'], 
             c=review_sample['rating'], marker='o')
plot.set_xlabel('Polarity')
plot.set_ylabel('Subjectivity')
plt.show()
# Correlation Coefficient

# User-Business n-n relationship
user_review, business_review, user_business_review = \
defaultdict(list), defaultdict(list), defaultdict(list)
for i in range(len(review)): 
    user, business, rating = review['user_id'][i], review['business_id'][i], int(review['rating'][i])
    user_review[user].append((business, rating))
    business_review[business].append((user, rating))
    user_business_review[(user, business)].append(rating)
hist_user, hist_business = defaultdict(int), defaultdict(int)
for k, v in user_review.iteritems(): 
    hist_user[len(v)] += 1
for k, v in business_review.iteritems(): 
    hist_business[len(v)] += 1
x_axis = numpy.arange(20)
y_value = hist_user.values()[0:10] + [0] + hist_user.values()[-10:-1]
x_name = hist_user.keys()[0:10] + ['...'] + hist_user.keys()[-10:-1]
pylab.bar(x_axis, y_value, align='center', width=0.5)
pylab.xticks(x_axis, x_name)
pylab.xlabel('# reviews per user')
pylab.ylabel('# users')
pylab.show()
y_value = hist_business.values()[0:10] + [0] + hist_business.values()[-10:-1]
x_name = hist_business.keys()[0:10] + ['...'] + hist_business.keys()[-10:-1]
pylab.bar(x_axis, y_value, align='center', width=0.5)
pylab.xticks(x_axis, x_name)
pylab.xlabel('# reviews per business')
pylab.ylabel('# businesses')
pylab.show()

# Possible Fake Review: one (user, business) pair but multiple reviews
multiple_review = {}
for k, v in user_business_review.iteritems(): 
    if len(v) > 1: 
        multiple_review[k] = (len(v), min(v), sum(v)/float(len(v)), max(v))
n = 0
with open('Canopy/Data/yelp_challenge/review.json') as data_file: 
    for line in data_file:
        if n > 5: break
        review_data = json.loads(line)
        user_business = (review_data['user_id'], review_data['business_id'])
        if multiple_review.get(user_business) is not None: 
            if multiple_review[user_business][0] > 5: 
                n += 1
                print multiple_review[user_business], review_data['stars']
                print review_data['text']