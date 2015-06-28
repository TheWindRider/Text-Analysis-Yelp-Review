from __future__ import division
import math
import glob

spam_dict = {}
ham_email_path = 'Canopy/Data/enron1/ham/*.txt'
spam_email_path = 'Canopy/Data/enron1/spam/*.txt'
ham_email, spam_email = 0, 0
for file_name in glob.glob(ham_email_path): 
    ham_email += 1
for file_name in glob.glob(spam_email_path): 
    spam_email += 1

def prior_prob(word, word_count_ham, word_count_spam, 
               total_count_ham, total_count_spam, adjust): 
    # too (in)frequent in both ham and spam --> a word without much value
    if (word_count_ham/total_count_ham > 0.9 and 
        word_count_spam/total_count_spam > 0.9) or \
       (word_count_ham/total_count_ham < 0.001 and 
        word_count_spam/total_count_spam < 0.001): 
        print "Word '%s' count: %d in ham and %d in spam" % \
               (word, word_count_ham, word_count_spam)
        return None, None
    # avoid situation P(email|ham) = 0 or P(email|spam) = 0
    if word_count_ham == 0 or word_count_spam == 0: 
        print "Word '%s' count: %d in ham and %d in spam" % \
               (word, word_count_ham, word_count_spam)
        word_count_ham += adjust
        word_count_spam += adjust
    return word_count_ham/total_count_ham, word_count_spam/total_count_spam

target_email = 'Canopy/Data/enron2/ham/0007.1999-12-13.kaminski.ham.txt'
log_given_ham, log_given_spam = 0, 0
unique_words = []
email_words = open(target_email, 'r').read().split()
for each_word in email_words: 
    if each_word in unique_words: 
        continue
    unique_words.append(each_word)
    if spam_dict.get(each_word) is not None: 
        log_given_ham += math.log(spam_dict[each_word][0])
        log_given_spam += math.log(spam_dict[each_word][1])
        continue
    ham_occur, spam_occur = 0, 0
    for file_name in glob.glob(ham_email_path): 
        if each_word in open(file_name).read():
            ham_occur += 1
    for file_name in glob.glob(spam_email_path): 
        if each_word in open(file_name).read():
            spam_occur += 1 
    word_given_ham, word_given_spam = prior_prob(each_word, ham_occur, spam_occur, 
                                                 ham_email, spam_email, 0.5)
    if word_given_ham is None and word_given_spam is None: 
        continue
    """
    if max(word_given_ham, word_given_spam) > 0.9 or \
        min(word_given_ham, word_given_spam) < 0.01: 
        print "Probability of '%s' is %.3f given ham and %.3f given spam" % \
               (each_word, word_given_ham, word_given_spam)
    """
    spam_dict[each_word] = [word_given_ham, word_given_spam]
    log_given_ham += math.log(word_given_ham)
    log_given_spam += math.log(word_given_spam)

p_given_ham = math.exp(log_given_ham)
p_given_spam = math.exp(log_given_spam)
p_ham = ham_email/(ham_email + spam_email)
p_spam = spam_email/(ham_email + spam_email)
p_email = p_ham * p_given_ham + p_spam * p_given_spam
p_spam_given_email = p_spam * p_given_spam / p_email