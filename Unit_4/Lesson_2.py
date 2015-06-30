from __future__ import division
import math
import glob

# Training a dictionary
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
clean_dict(spam_dict, ham_email, spam_email, 0.005)

def prior_prob(word, word_count_ham, word_count_spam, 
               total_count_ham, total_count_spam, adjust): 
    # avoid situation P(email|ham) = 0 or P(email|spam) = 0
    if word_count_ham == 0 or word_count_spam == 0: 
        word_count_ham += adjust
        word_count_spam += adjust
    return word_count_ham/total_count_ham, word_count_spam/total_count_spam

def prior_prob_laplace(word, word_count_ham, word_count_spam, 
                       total_count_ham, total_count_spam, alpha, beta): 
    word_count_ham += alpha
    word_count_spam += beta
    return word_count_ham/(total_count_ham + 1), word_count_spam/(total_count_spam + 1)

def spam_prob(email_file, email_words, alpha, beta): 
    log_given_ham, log_given_spam = 0, 0
    unique_words = []
    for each_word in email_words: 
        if each_word in unique_words: 
            continue
        unique_words.append(each_word)
    for word, count in spam_dict.iteritems(): 
        word_given_ham, word_given_spam = \
        prior_prob_laplace(word, count[0], count[1], ham_email, spam_email, alpha, beta)
        if word in unique_words: 
            log_given_ham += math.log(word_given_ham)
            log_given_spam += math.log(word_given_spam)
        else: 
            log_given_ham += math.log(1 - word_given_ham)
            log_given_spam += math.log(1 - word_given_spam)
    
    p_ham = ham_email/(ham_email + spam_email)
    p_spam = spam_email/(ham_email + spam_email)
    p_given_ham = math.exp(log_given_ham)
    p_given_spam = math.exp(log_given_spam) 
    p_email = p_ham * p_given_ham + p_spam * p_given_spam
    if p_email == 0: 
        return [0, 0]
    p_ham_given_email = math.log(p_ham) + log_given_ham - math.log(p_email)
    p_spam_given_email = math.log(p_spam) + log_given_spam - math.log(p_email)
    return [p_ham_given_email, p_spam_given_email]

# Optimizing and predicting
ham_email_test = 'Canopy/Data/enron2/ham/*.txt'
spam_email_test = 'Canopy/Data/enron2/spam/*.txt'
for alpha_test in [0.5, 1]: 
    for beta_test in [0.5, 1]: 
        low_p_email_ham, low_p_email_spam = 0, 0 
        log_ham_prob, log_spam_prob = 0, 0
        print "running [%.1f, %.1f]" % (alpha_test, beta_test)
        for file_name in glob.glob(ham_email_test):
            email_test = open(file_name, 'r').read().split()
            ham_prob_test = spam_prob(file_name, email_test, alpha_test, beta_test)[0]
            if ham_prob_test > 0: 
                ham_prob_test = 0
            log_ham_prob += ham_prob_test
        for file_name in glob.glob(spam_email_test):
            email_test = open(file_name, 'r').read().split()
            spam_prob_test = spam_prob(file_name, email_test, alpha_test, beta_test)[1]
            if spam_prob_test > 0: 
                spam_prob_test = 0
            log_spam_prob += spam_prob_test
        print "Alpha = %.1f, Beta = %.1f: log(ham prob) = %.1f, log(spam prob) = %.1f" %\
               (alpha_test, beta_test, log_ham_prob, log_spam_prob)
