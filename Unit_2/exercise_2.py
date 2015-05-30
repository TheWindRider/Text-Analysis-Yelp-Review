"""
# univariate - toy data
import os
import matplotlib.pyplot as plt
import scipy.stats as stats
x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]

os.chdir('Documents/Thinkful Project/thinkful course/Unit_2')
plt.boxplot(x)
plt.savefig('box.png')
plt.close()
plt.hist(x, histtype='bar')
plt.savefig('hist.png')
plt.close()
stats.probplot(x, dist = 'norm', plot = plt)
plt.savefig('qq.png')
plt.close()
"""
# univariate - lending
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import os

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)
os.chdir('Documents/Thinkful Project/thinkful course/Unit_2')

loansData.boxplot(column='Amount.Requested')
plt.savefig('loan_box.png')
plt.close()
loansData.hist(column='Amount.Requested')
plt.savefig('loan_hist.png')
plt.close()
stats.probplot(loansData['Amount.Requested'], dist="norm", plot=plt)
plt.savefig('loan_qq.png')