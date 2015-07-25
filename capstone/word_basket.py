import time
import pandas
import Orange

REVIEW_FILE = 'Documents/Thinkful Project/all_review.basket'

review_data = Orange.data.Table(REVIEW_FILE)
start_time = time.time()
assoc_rules = Orange.associate.AssociationRulesSparseInducer(
              review_data, support=0.01, confidence=0, max_item_sets=500000)
print time.time() - start_time, len(assoc_rules)

# Collect metrics of all rules
rule_left, rule_right = [[],[],[]], [[],[],[]]
support, confidence, lift = [[],[],[]], [[],[],[]], [[],[],[]]
for rule in assoc_rules: 
    if rule.lift < 1: continue
    left_words = rule.left.getmetas(str).keys()
    right_words = rule.right.getmetas(str).keys()
    group = 2
    if '+' in left_words or right_words == ['+']: 
        group = 0
    elif '-' in left_words or right_words == ['-']: 
        group = 1
    else: continue
    rule_left[group].append(left_words)
    rule_right[group].append(right_words)
    support[group].append(rule.support)
    confidence[group].append(rule.confidence)
    lift[group].append(rule.lift)
pos_assoc = pandas.DataFrame({'left': rule_left[0], 'right': rule_right[0], 'support': support[0], 
                              'confidence': confidence[0], 'lift': lift[0]})
neg_assoc = pandas.DataFrame({'left': rule_left[1], 'right': rule_right[1], 'support': support[1], 
                              'confidence': confidence[1], 'lift': lift[1]})
pos_assoc.to_csv('Documents/Thinkful Project/thinkful course/capstone/positive_rule.csv', index=False)
neg_assoc.to_csv('Documents/Thinkful Project/thinkful course/capstone/negative_rule.csv', index=False)
print pos_assoc.sort('confidence', ascending=False)[0:15]
print pos_assoc.sort('lift', ascending=False)[0:15]
print neg_assoc.sort('confidence', ascending=False)[0:15]
print neg_assoc.sort('lift', ascending=False)[0:15]