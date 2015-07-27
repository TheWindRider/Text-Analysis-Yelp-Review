import imp
import json
import pandas
from textblob import TextBlob

US_STATES = set(['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA', 
                 'HI','ID','IL','IN','IA','KS','KY','LA','ME','MD',
                 'MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ',
                 'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
                 'SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'])
YELP_LKP_FILE ='Documents/Thinkful Project/thinkful course/capstone/yelp_lookup.py'
YELP_BIZ_FILE = 'Canopy/Data/yelp_challenge/business.json'
YELP_DATA_FILE = 'Canopy/Data/yelp_challenge/review.json'
REVIEW_TEXT_FILE = 'Documents/Thinkful Project/yelp_text.txt'
REVIEW_LIMIT = [5, 500]

# Get state and category from business file
lookup = imp.load_source('', YELP_LKP_FILE)
business_info = lookup.business_dict(YELP_BIZ_FILE)

# Organize reviews into Business - User - Review(s) tree structure
n, review_tree = 0, {}
with open(YELP_DATA_FILE) as data_file: 
    for line in data_file: 
        review_data = json.loads(line)
        business_id = review_data['business_id']
        user_id = review_data['user_id']
        review_text = review_data['text'].replace('\n', ' ')
        review_rate = int(review_data['stars'])
        if business_info[business_id][0] not in US_STATES: 
            if len(review_text) < 3: 
                continue
            blob_review = TextBlob(review_text)
            if blob_review.detect_language() != 'en': 
                continue
        if n % 50000 == 0: print n
        n += 1
        if review_tree.get(business_id) is None: 
            review_tree[business_id] = {user_id: [(review_text, review_rate)]}
        elif review_tree[business_id].get(user_id) is None: 
            review_tree[business_id][user_id] = [(review_text, review_rate)]
        else: 
            review_tree[business_id][user_id].append((review_text, review_rate))

# Truncate on two conditions: 1 user-business has 5+ reviews; 1 business has 500+ reviews
def append_review(review_per_business): 
    n_per_business = 0
    for user_id, reviews in review_per_business.iteritems():
        n_per_user = min(len(reviews), REVIEW_LIMIT[0])
        for review in reviews[0: n_per_user]: 
            if n_per_business >= REVIEW_LIMIT[1]: return n_per_business
            business.append(business_id)
            user.append(user_id)
            text.append(review[0])
            rating.append(review[1])
            sentiment.append(TextBlob(review[0]).sentiment)
            n_per_business += 1
    return n_per_business
n = 0
business, user, text, rating, sentiment = [], [], [], [], []
for business_id, review_sub_tree in review_tree.iteritems(): 
    if n % 10000 == 0: print n
    num_review = append_review(review_sub_tree)
    n += 1
# Generate light-weight dataframe and review text separately
summary = pandas.DataFrame({'business_id': business, 'user_id': user, 'rating': rating, 
                            'polarity': [x.polarity for x in sentiment], 
                            'subjectivity': [x.subjectivity for x in sentiment]})
summary.to_csv('Documents/Thinkful Project/yelp_review.csv', sep=',', index=False)
with open('Documents/Thinkful Project/yelp_text.txt', 'w') as output: 
    for each_review in text: 
        output.write(each_review.encode('utf8') + '\n')