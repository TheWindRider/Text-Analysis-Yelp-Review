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