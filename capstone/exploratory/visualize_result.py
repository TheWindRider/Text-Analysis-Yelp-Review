import numpy
import pandas
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

RESULT_FILE = 'Documents/Thinkful Project/result.csv'
TOP_N = 10

rules = pandas.read_csv(RESULT_FILE)
def top_rules(criteria): 
    output = rules.sort(criteria, ascending=False)[0:TOP_N]
    axis.clear()
    axis.barh(numpy.arange(TOP_N), output[criteria])
    axis.set_xlabel(criteria)
    axis.set_yticklabels(zip(output['left'], output['right']))
    plt.draw()

output = rules.sort('lift', ascending=False)[0:TOP_N]
fig, axis = plt.subplots()
plt.subplots_adjust(left=0.25)
axis.barh(numpy.arange(TOP_N), output['lift'])
axis.set_xlabel('Lift')
axis.set_yticklabels(zip(output['left'], output['right']))
rax = plt.axes([0.05, 0.4, 0.15, 0.15])
choose_criteria = RadioButtons(rax, ('lift', 'confidence', 'support'))
choose_criteria.on_clicked(top_rules)
plt.show()