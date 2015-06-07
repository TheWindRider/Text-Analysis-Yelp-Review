"""
# Univariate - toy data
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

# Univariate - lending
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

# Chi-Squared Test
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

# Multivariate Analysis
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from IPython.core.display import HTML

def short_summary(est):
    return HTML(est.summary().tables[1].as_html())

loansData = pd.read_csv('SQLite Data/LoanStats3b.csv')
loansData = loansData[['int_rate', 'annual_inc', 'home_ownership']]
loansData.dropna(inplace=True)
loansData.to_csv('Documents/Thinkful Project/thinkful course/Unit_2/LoanStats3b_clean.csv', header=True, index=False)

loansData['int_rate'] = loansData['int_rate'].apply(lambda x: float(str(x).rstrip('%'))/100)
loansData['log_annual_inc'] = np.log1p(loansData.annual_inc)
loansData['home_is_own'] = loansData['home_ownership'] == 'OWN'
loansData['home_is_rent'] = loansData['home_ownership'] == 'RENT'
loansData['home_is_mortgage'] = loansData['home_ownership'] == 'MORTGAGE'

model_1 = smf.ols(formula = 'int_rate ~ 1 + log_annual_inc', data = loansData).fit()
print "Model_1 R Squared: {0}".format(model_1.rsquared)
print model_1.summary().tables[1]
model_2 = smf.ols(formula = 'int_rate ~ 1 + log_annual_inc + C(home_ownership)', data = loansData).fit()
print "Model_2 R Squared: {0}".format(model_2.rsquared)
print model_2.summary().tables[1]
model_3 = smf.ols(formula = 'int_rate ~ 1 + log_annual_inc * C(home_ownership)', data = loansData).fit()
print "Model_3 R Squared: {0}".format(model_3.rsquared)
print model_3.summary().tables[1]
model_4 = smf.ols(formula = 'int_rate ~ 1 + (home_is_own + home_is_rent + home_is_mortgage) * log_annual_inc', data = loansData).fit()
print "Model_4 R Squared: {0}".format(model_4.rsquared)
print model_4.summary().tables[1]

# Time Series
import pandas as pd
import statsmodels.api as sapi

loansData = pd.read_csv('SQLite Data/LoanStats3b.csv', low_memory = False)
loansData['issue_d_format'] = pd.to_datetime(loansData['issue_d']) 
dfts = loansData.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x : x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']
loan_count_series = pd.Series()
for i in loan_count_summary.index: 
    if i+1 in loan_count_summary.index: 
        loan_count_series[i+1] = loan_count_summary[i+1] - loan_count_summary[i]
sapi.graphics.tsa.plot_acf(loan_count_series)
sapi.graphics.tsa.plot_pacf(loan_count_series)

print "There is and is only lag-1 autocorrelation after 1 degree of differencing"
"""
# Markov Chain
import pandas as pd
stock = pd.DataFrame({'bull': [.9, .15, .25], 'bear': [.075, .8, .25], 'stag': [.025, .05, .5]},
index=["bull", "bear", "stag"])
stock = stock[['bull', 'bear', 'stag']]
curr_stock = [stock]
trans = 1
cnt = True
while trans < 50 and cnt: 
    curr_stock.append(curr_stock[trans - 1].dot(stock))
    trans += 1
    if trans in [2, 5, 10]: 
        print "probability after %d transitions:" % trans
        print curr_stock[trans - 1]
    for i,j in [(i,j) for i in ['bull', 'bear', 'stag'] for j in ['bull', 'bear', 'stag']]: 
        if abs(curr_stock[trans-1][i][j] - curr_stock[trans-2][i][j]) > 0.0001: 
            break
        cnt = False
print "steady after %d transitions:" % trans
print curr_stock[-1]