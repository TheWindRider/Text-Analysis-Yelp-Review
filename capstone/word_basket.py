import time
import pandas
import Orange

REVIEW_FILE = 'Documents/Thinkful Project/all_review.basket'
RESULT_FILE = 'Documents/Thinkful Project/result.csv'

review_data = Orange.data.Table(REVIEW_FILE)
start_time = time.time()
assoc_rules = Orange.associate.AssociationRulesSparseInducer(
              review_data, support=0.01, confidence=0, max_item_sets=500000)
print time.time() - start_time, len(assoc_rules)

def filter_rules(assoc_rules, interest): 
    rule_left, rule_right, support, confidence, lift = [], [], [], [], []
    for rule in assoc_rules: 
        left_words = rule.left.getmetas(str).keys()
        right_words = rule.right.getmetas(str).keys()
        capital_right_words = [word for word in right_words if word[0].isupper()]
        capital_left_words = [word for word in left_words if word[0].isupper()]
        group = 0
        if rule.lift < 1 or len(capital_right_words) > 0 or \
           left_words == ['+'] or left_words == ['-']: continue
        if right_words == ['+'] or right_words == ['-']: group = 1
        if '+' in left_words or '-' in left_words: 
            if len(capital_left_words) == 0: group = 2
            else: group = 3
        if group != interest: continue
        rule_left.append(left_words)
        rule_right.append(right_words)
        support.append(rule.support)
        confidence.append(rule.confidence)
        lift.append(rule.lift)
    interest_rules = pandas.DataFrame({'left': rule_left, 'right': rule_right, 
                     'support': support, 'confidence': confidence, 'lift': lift})
    return interest_rules

# Collect metrics of intersting rules
# Rules with sentiment on the right-hand side
sentiment_predictor = filter_rules(assoc_rules, 1)
sentiment_predictor.to_csv(RESULT_FILE, index=False)
# Rules with sentiment but no category on the left-hand side
other_keyword = filter_rules(assoc_rules, 2)
other_keyword.to_csv(RESULT_FILE, index=False)
# Rules with sentiment and category on the left-hand side
category_keyword = filter_rules(assoc_rules, 3)
category_keyword.to_csv(RESULT_FILE, index=False)