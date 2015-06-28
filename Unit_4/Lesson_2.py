from __future__ import division
import math
import glob

def clean_dict(spam_dict, ham_size, spam_size, pct): 
    to_be_removed = []
    for key, value in spam_dict.iteritems(): 
        # too infrequent --> biased estimation on prior probability
        if value[0] < ham_size * pct and value[1] < spam_size * pct: 
            to_be_removed.append(key)
    for key in to_be_removed: 
        del spam_dict[key]

spam_dict = {}
ham_email_path = 'Canopy/Data/enron1/ham/*.txt'
spam_email_path = 'Canopy/Data/enron1/spam/*.txt'
ham_email, spam_email = 0, 0
for file_name in glob.glob(ham_email_path): 
    ham_email += 1
    unique_words = []
    email_words = open(file_name, 'r').read().split()
    for curr_word in email_words: 
        if curr_word in unique_words: 
            continue
        unique_words.append(curr_word)
    for curr_word in unique_words: 
        if spam_dict.get(curr_word) is None:
            spam_dict[curr_word] = [1, 0]
        else: 
            spam_dict[curr_word][0] += 1
for file_name in glob.glob(spam_email_path): 
    spam_email += 1
    unique_words = []
    email_words = open(file_name, 'r').read().split()
    for curr_word in email_words: 
        if curr_word in unique_words: 
            continue
        unique_words.append(curr_word)
    for curr_word in unique_words: 
        if spam_dict.get(curr_word) is None:
            spam_dict[curr_word] = [0, 1]
        else: 
            spam_dict[curr_word][1] += 1
clean_dict(spam_dict, ham_email, spam_email, 0.001)

def prior_prob(word, word_count_ham, word_count_spam, 
               total_count_ham, total_count_spam, adjust): 
    # avoid situation P(email|ham) = 0 or P(email|spam) = 0
    if word_count_ham == 0 or word_count_spam == 0: 
        word_count_ham += adjust
        word_count_spam += adjust
    return word_count_ham/total_count_ham, word_count_spam/total_count_spam

target_email = 'Canopy/Data/enron2/spam/0002.2001-05-25.SA_and_HP.spam.txt'
log_given_ham, log_given_spam = 0, 0
unique_words = []
email_words = open(target_email, 'r').read().split()
for each_word in email_words: 
    if each_word in unique_words: 
        continue
    unique_words.append(each_word)

for word, count in spam_dict.iteritems(): 
    word_given_ham, word_given_spam = prior_prob(word, count[0], count[1], 
                                                 ham_email, spam_email, 0.5)
    if word in unique_words: 
        log_given_ham += math.log(word_given_ham)
        log_given_spam += math.log(word_given_spam)
    else: 
        log_given_ham += math.log(1 - word_given_ham)
        log_given_spam += math.log(1 - word_given_spam)

p_given_ham = math.exp(log_given_ham)
p_given_spam = math.exp(log_given_spam)
p_ham = ham_email/(ham_email + spam_email)
p_spam = spam_email/(ham_email + spam_email)
p_email = p_ham * p_given_ham + p_spam * p_given_spam
p_spam_given_email = p_spam * p_given_spam / p_email
print "Spam Probability: %.5f" % p_spam_given_email