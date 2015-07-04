from __future__ import division
import re
import time
import math
import pandas
import requests
from sklearn import metrics

APIKEY = '132bffd4da6364002cc3ce1617e0d46d:18:65473245'
section_list = ['Arts', 'Business', 'Obituaries', 'Sports', 'World']
section_size = []

"""
# Get NYT articles
for section_name in section_list: 
    web_url, headline, lead_paragraph = [], [], []
    for page_index in range(100): 
        print section_name + str(page_index)
        time.sleep(1)
        url_curr = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?' + \
                   'fq=section_name%3A%28%22' + section_name + \
                   '%22%29&sort=newest&fl=web_url%2Cheadline%2Clead_paragraph&page=' + \
                   str(page_index) + '&api-key=' + APIKEY
        data_curr = requests.get(url_curr)
        for article_index in range(10): 
            col_curr = data_curr.json()['response']['docs'][article_index]['web_url']
            web_url.append(('' if col_curr is None else col_curr).encode('utf8'))
            col_curr = data_curr.json()['response']['docs'][article_index]['headline']['main']
            headline.append(('' if col_curr is None else col_curr).encode('utf8'))
            col_curr = data_curr.json()['response']['docs'][article_index]['lead_paragraph']
            lead_paragraph.append(('' if col_curr is None else col_curr).encode('utf8'))

    dataframe_curr = pandas.DataFrame({'web_url': web_url, 
                                       'headline': headline, 
                                       'lead_paragraph': lead_paragraph})
    file_path = 'Documents/Thinkful Project/thinkful course/Unit_4/' + \
                 section_name + '_' + time.strftime("%m_%d") + '.txt'
    dataframe_curr.to_csv(file_path, sep='\t', index=False)
"""

# Training a dictionary
articles = {}
for section_name in section_list: 
    file_path = 'Documents/Thinkful Project/thinkful course/Unit_4/' + \
                 section_name + '_06_30.txt'
    dataframe_curr = pandas.read_csv(file_path, sep='\t')
    dataframe_curr.fillna(value='', inplace=True)
    articles[section_name] = dataframe_curr
    section_size.append(len(dataframe_curr))

def clean_dict(category_dict, category_size, pct): 
    to_be_removed = []
    for key, value in category_dict.iteritems(): 
        # too infrequent --> biased estimation on prior probability
        is_infreq = True
        for count in value: 
            if count > category_size * pct: 
                is_infreq = False
                break 
        if is_infreq: 
            to_be_removed.append(key)
    for key in to_be_removed: 
        del category_dict[key]

def find_vip_word(category_dict, section_index, top_n): 
    # custom scoring values both absolute and relative frequency
    word_list = [(k, (v[section_index]/sum(v) - 1/len(section_list)) * v[section_index]) 
                 for k, v in category_dict.iteritems()]
    word_list.sort(key=lambda tup: tup[1], reverse=True)
    if 0 < top_n < len(word_list): 
        return word_list[0:top_n]
    else: 
        return word_list

category_dict = {}
for section_index in range(len(section_list)):
    for headline, paragraph, url in articles[section_list[section_index]].itertuples(index=False): 
        unique_words = []
        paragraph = re.compile(r'([^A-Za-z0-9 ])').sub('', paragraph + ' ' + headline)
        for word in paragraph.split(): 
            if word not in unique_words: 
                unique_words.append(word)
        for word in unique_words: 
            if category_dict.get(word) is None: 
                category_dict[word] = [0] * len(section_list)
            category_dict[word][section_index] += 1
clean_dict(category_dict, 1000, 0.001)
for section_index in range(len(section_list)): 
    print section_list[section_index]
    print find_vip_word(category_dict, section_index, 10)

def prior_prob_laplace(word, word_count, total_count, alpha, beta): 
    prior_prob = []
    local_word_count, local_total_count = list(word_count), list(total_count)
    for i in range(len(word_count)): 
        local_word_count[i] += alpha - 1
        local_total_count[i] += alpha + beta - 2
        prior_prob.append(local_word_count[i]/local_total_count[i])
    return prior_prob

def category_prob(article_words, alpha, beta): 
    log_prior_prob = [0] * len(section_list)
    unique_words = []
    for word in article_words: 
        if word not in unique_words: 
            unique_words.append(word)
    for word, count in category_dict.iteritems():
        word_prior_prob = \
        prior_prob_laplace(word, count, section_size, alpha, beta)
        if word in unique_words: 
            for i in range(len(section_list)): 
                log_prior_prob[i] += math.log(word_prior_prob[i])
        else: 
            for i in range(len(section_list)): 
                log_prior_prob[i] += math.log(1 - word_prior_prob[i])
    # simplified with equal cateogry size
    post_prob = [math.exp(x) for x in log_prior_prob]
    sum_post_prob = sum(post_prob)
    if sum_post_prob == 0: 
        post_prob = [1/len(section_list)] * len(section_list)
    else: 
        post_prob = [x/sum_post_prob for x in post_prob]
    return post_prob

# Test with small amount of articles
unique_dates = []
alpha_test, beta_test = 1.05, 1.5
true_category, true_prob, predict_category = [], [], []
for section_name in section_list:
    for page_index in range(2):
        print section_name + str(page_index)
        time.sleep(1)
        url_curr = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?' + \
                   'fq=section_name%3A%28%22' + section_name + \
                   '%22%29&sort=newest&fl=headline%2Clead_paragraph%2Cpub_date&page=' + \
                   str(page_index) + '&api-key=' + APIKEY
        data_curr = requests.get(url_curr)
        for article_index in range(10):
            date_curr = data_curr.json()['response']['docs'][article_index]['pub_date']
            if date_curr[:10] not in unique_dates: 
                unique_dates.append(date_curr[:10])
            col_curr = data_curr.json()['response']['docs'][article_index]['lead_paragraph']
            if col_curr is not None: 
                col_curr += ' ' + data_curr.json()['response']['docs'][article_index]['headline']['main']
                paragraph_words = re.compile(r'([^A-Za-z0-9 ])').sub('', col_curr.encode('utf8')).split()
                prob = category_prob(paragraph_words, alpha_test, beta_test)
                max_prob = max(prob)
                true_category.append(section_name)
                true_prob.append(math.log(prob[section_list.index(section_name)]))
                predict_category.append(section_list[prob.index(max_prob)])
                
print sum(true_prob)
print metrics.confusion_matrix(true_category, predict_category)