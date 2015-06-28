import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
import pandas
import numpy
import math
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from scipy.spatial.distance import minkowski
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

ny_house = pandas.read_csv('SQLite Data/RealEstate/rollingsales_manhattan.csv')
ny_house['sale_price'] = \
ny_house['SALE PRICE'].apply(lambda x: int(x.translate(None, '$, ')))
ny_house['land_area'] = \
ny_house['LAND SQUARE FEET'].apply(lambda x: int(x.translate(None, ',')))
ny_house['gross_area'] = \
ny_house['GROSS SQUARE FEET'].apply(lambda x: int(x.translate(None, ',')))
ny_house['class_category'] = \
ny_house['BUILDING CLASS CATEGORY'].apply(lambda x: x.split(' ')[0])
ny_house['sale_date'] = pandas.to_datetime(ny_house['SALE DATE'])
ny_house['age'] = 2015 - ny_house['YEAR BUILT']
ny_house['zip_code'] = ny_house['ZIP CODE']
ny_house.drop(['SALE PRICE', 'LAND SQUARE FEET', 'GROSS SQUARE FEET', 
               'BUILDING CLASS CATEGORY', 'SALE DATE', 'YEAR BUILT', 
               'ZIP CODE'], axis=1, inplace=True)

ny_house_data = ny_house[
(ny_house['sale_price'] > 0) & (ny_house['land_area'] > 0) &
(ny_house['sale_price'] < 1.0E+9) & (ny_house['land_area'] < 5.0E+5) & 
(ny_house['gross_area'] > 0) & (ny_house['age'] < 200)]
ny_house_data['sale_price_sqrt'] = \
ny_house_data['sale_price'].apply(lambda x: math.sqrt(x))
ny_house_train, ny_house_test = train_test_split(ny_house_data[
['sale_price', 'sale_price_sqrt', 'land_area', 'gross_area', 'class_category', 
 'sale_date', 'age', 'zip_code', 'NEIGHBORHOOD']], test_size=0.2)

# Linear Regression --> sale_price
linear_reg = sm.ols(formula="sale_price ~ land_area + age", 
                   data=ny_house_train).fit()
ny_house_test['sale_price_predict'] = linear_reg.predict(exog=dict(
                                      land_area=ny_house_test['land_area'], 
                                      age=ny_house_test['age']))
grid_land_area, grid_age = numpy.meshgrid(ny_house_test['land_area'], ny_house_test['age'])
grid_sale_price = linear_reg.predict(exog=dict(
                  land_area=grid_land_area.ravel(), 
                  age=grid_age.ravel())).reshape(grid_land_area.shape)

figure = plt.figure()
plot = figure.add_subplot(111, projection='3d')

plot.scatter(ny_house_test['land_area'], ny_house_test['age'], 
             ny_house_test['sale_price'], c='b', marker='o')
""" Alternative: plot predictions as points
plot.scatter(ny_house_test['land_area'], ny_house_test['age'], 
             ny_house_test['sale_price_predict'], c='r', marker='o')
"""
plot.plot_surface(grid_land_area, grid_age, grid_sale_price, cmap=cm.hot)
plot.set_xlabel('Land Area (feet^2)')
plot.set_ylabel('Age (years)')
plot.set_zlabel('Sale Price ($)')
plt.show()

# K-NN --> neighbourhood
def mixed_dist(x, y): 
    if x[-1] != y[-1]: 
        x[-1], y[-1] = 10000, 0  # arbitrary, about same scale as other
    else: 
        x[-1], y[-1] = 0, 0
    return minkowski(x, y, 2)
    
explain_var = ['land_area', 'age', 'sale_price_sqrt', 'zip_code']
for k in range(5,20): 
    for option in ['uniform', 'distance']: 
        """ treat categorical variable as continuous
        knn_estimator = KNeighborsClassifier(n_neighbors=k, weights=option)
        """
        knn_estimator = KNeighborsClassifier(n_neighbors=k, weights=option, 
                                             metric='pyfunc', func=mixed_dist)
        knn_estimator.fit(ny_house_train[explain_var], 
                          ny_house_train['NEIGHBORHOOD'])
        expected = ny_house_test['NEIGHBORHOOD']
        predicted = knn_estimator.predict(ny_house_test[explain_var])
        error_rate = (predicted != expected).mean()
        print("Error rate is %.3f using %d neighbour with %s weights"
               % (error_rate, k, option))

knn_estimator = KNeighborsClassifier(n_neighbors=15, weights='distance', 
                                     metric='pyfunc', func=mixed_dist)
knn_estimator.fit(ny_house_train[explain_var], 
                  ny_house_train['NEIGHBORHOOD'])
expected = ny_house_test['NEIGHBORHOOD']
predicted = knn_estimator.predict(ny_house_test[explain_var])

figure = plt.figure()
plot = figure.add_subplot(111, projection='3d')
plot.scatter(ny_house_test[predicted == expected]['land_area'], 
             ny_house_test[predicted == expected]['age'], 
             ny_house_test[predicted == expected]['sale_price'], c='b', marker='o')
plot.scatter(ny_house_test[predicted != expected]['land_area'], 
             ny_house_test[predicted != expected]['age'], 
             ny_house_test[predicted != expected]['sale_price'], c='r', marker='o')
plot.set_xlabel('Land Area (feet^2)')
plot.set_ylabel('Age (years)')
plot.set_zlabel('Sale Price ($)')
plt.show()