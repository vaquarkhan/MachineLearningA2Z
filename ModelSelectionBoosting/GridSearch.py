# -*- coding: utf-8 -*-

# read dataset
import pandas as pd
dataset = pd.read_csv('Social_Network_Ads.csv')
x = dataset.iloc[:, [2,3]].values
y = dataset.iloc[:, 4].values

# split dataset into train and test
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=1/5, random_state=0)

# scale all the features
from sklearn.preprocessing import StandardScaler
sc_x = StandardScaler()
x_train = sc_x.fit_transform(x_train)
x_test = sc_x.transform(x_test)

from sklearn.svm import SVC
model = SVC(kernel='rbf', random_state=0)
model.fit(x_train, y_train)

# predict on the test data and learn about performance using confusion matrix
y_pred = model.predict(x_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

# apply k-fold cross validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=model, X=x_train, y=y_train, cv=10)
print(accuracies.mean())

# Utilize grid search to find optimal kernel algorithm with hyper tuned params
from sklearn.model_selection import GridSearchCV
# pick parameters with set of values to try to find optimal model params
params = [{'C': [1, 10, 100], 'kernel': ['linear']},
          {'C': [1, 10, 100], 'kernel': ['rbf'], 'gamma': [0.5, 0.1, 0.01]}]
grdSearch = GridSearchCV(estimator=model, param_grid=params, scoring='accuracy', cv=10)
grdSearch.fit(x_train, y_train)
print(grdSearch.best_score_)
print(grdSearch.best_params_)

# define a scatter plot visualization func
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def visualize(x_set, y_set):
    cmap = ListedColormap(('red', 'blue'))
    X1, X2 = np.meshgrid(np.arange(start = x_set[:, 0].min() - 1, stop = x_set[:, 0].max() + 1, step = 0.01),
                         np.arange(start = x_set[:, 1].min() - 1, stop = x_set[:, 1].max() + 1, step = 0.01))
    plt.contourf(X1, X2, model.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
                 alpha = 0.75, cmap = cmap)
    plt.xlim(X1.min(), X1.max())
    plt.ylim(X2.min(), X2.max())
    for i, j in enumerate(np.unique(y_set)):    
        plt.scatter(x_set[y_set == j,0], x_set[y_set == j,1], c=cmap(j))
    plt.show()

# visualize the train data
visualize(x_train, y_train)

# visualize the test data
visualize(x_test, y_test)

# visualize the prediction data
visualize(x_test, y_pred)
