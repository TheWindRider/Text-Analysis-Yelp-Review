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

# chi-square test
from scipy import stats
import pandas as pd
import collections

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

freq = collections.Counter(loansData['Open.CREDIT.Lines'])
chi, p = stats.chisquare(freq.values())
if p < 0.05: 
    print "Null hypothesis rejected, not even distribution"
else: 
    print "Cannot reject the null hypotheis on an even distribution"

# Linear Regression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loansData.dropna(inplace=True)

loansData['Interest.Rate'] = loansData['Interest.Rate'].apply(lambda x: float(x.rstrip('%'))/100)
loansData['Loan.Length'] = loansData['Loan.Length'].apply(lambda x: int(x.split(' ')[0]))
loansData['FICO.Score'] = loansData['FICO.Range'].apply(lambda x: int(x.split('-')[0]))
loansData.to_csv('Documents/Thinkful Project/thinkful course/Unit_2/loansData_clean.csv', header=True, index=False)

pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.show()

intrate = loansData['Interest.Rate']
loanamt = loansData['Amount.Requested']
fico = loansData['FICO.Score']

dep_var = np.matrix(intrate).transpose()
exp_1 = np.matrix(fico).transpose()
exp_2 = np.matrix(loanamt).transpose()
exp_both = np.column_stack([exp_1, exp_2])
exp_var = sm.add_constant(exp_both)
model = sm.OLS(dep_var, exp_var)
print model.fit().summary()
"""
# Logistics Regression
import pandas as pd
import statsmodels.api as sm
import math

def logistics_function (input_value, coeff_value): 
    p = 1/(1 + math.exp(-coeff_value.dot(input_value)))
    if p < 0.3: 
        print 'Grant ${0} loan with interest rate of {1}%'.format(loanamt, int(threshold * 100))
    else: 
        print 'Reject ${0} loan with interest rate of {1}%'.format(loanamt, int(threshold * 100))
    return p

threshold = 0.12
loanamt = 10000
fico = 720
loansData = pd.read_csv('Documents/Thinkful Project/thinkful course/Unit_2/loansData_clean.csv')
loansData['Interest.Rate.Ishigh'] = loansData['Interest.Rate'] >= threshold
loansData['Constant.Intercept'] = 1
explain_vars = ['Amount.Requested', 'FICO.Score', 'Constant.Intercept']

logit = sm.Logit(loansData['Interest.Rate.Ishigh'], loansData[explain_vars])
coeff = logit.fit().params
p_value = logistics_function([loanamt, fico, 1], coeff)