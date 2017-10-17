# Thinkful
Enrolled in a Thinkful course on Data Science
Course Material
------
Capstone Project
------
Some original and itermediate data files are too large to be uploaded to Github. Reproducing the results entails downloading files and organizing their locations, based on the following workflow logical order: 

1. review.json

Yelp review raw data, one of the files downloaded from [Yelp](http://www.yelp.com/dataset_challenge)

2. business.json
  
Yelp business raw data, another file in the downloads above

3. yelp_lookup.py, init.py

Two functions in yelp_lookup.py are to be called by other .py scripts, and init.py is supposed to be in the same folder to enable that mechanism

4. process_yelp_review.py

It calls 1, 2 and 3 then put review text into 5 and review summary info into 6

5. yelp_text.txt
  
The actual review text, and in this project, only English reviews are included

6. yelp_review.csv

Summary info of reviews with business and user IDs, and star ratings

7. extract_review.py

It calls 2, 3, 5 and 6 then parse review text and other relevant info into "word baskets" in 8

8. all_review.basket or keyword_review.basket

Depending on whether keywords are specified, .basket file prepares either all reivews or only those containing key words, in the format of 1 line per reivew with all useful words (sentiment treated as a word) separated by ','

9. generate_rule.py

It calls 8 and apply association model to generate rules
  
Each rule has 2 lists of words and 3 metrics (support, confidence and lift) which collectively quantify the strength of that association between one list and the other
