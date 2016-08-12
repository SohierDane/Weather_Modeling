"""
Generates, cross validates, and compares several candidate regression models.
"""

from __future__ import division
import numpy as np
from build_base_table import prep_analytics_base_table
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV

if __name__ == "__main__":
    k = 5
    min_distance = 200
    abt = prep_analytics_base_table(k, min_distance)
    Y = abt.pop('Temp_Y')
    X = abt
    X_train, X_test, y_train, y_test = train_test_split(X, Y)

    models = dict()
    models['linear'] = LinearRegression(n_jobs=-1)
    models['rand_forest'] = GridSearchCV(RandomForestRegressor(n_jobs=-1), cv=5,
                                         param_grid={"max_depth": [3, 4, 5]})
    models['krr'] = GridSearchCV(KernelRidge(kernel='rbf', gamma=0.1), cv=5,
                                 param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3],
                                 "gamma": np.logspace(-2, 2, 5)})
    models['ada'] = GridSearchCV(AdaBoostRegressor(), cv=5, param_grid={
                                 "n_estimators": [40, 60, 80], "learning_rate":
                                 [0.5, 1]})
    models['grad_boost'] = GridSearchCV(GradientBoostingRegressor(), cv=5, param_grid={
                                 "n_estimators": [40, 60, 80], "learning_rate":
                                 [0.5, 1]})
    for key, model in models.iteritems():
        model.fit(X_train, y_train)
        print key+" scored "+str(model.score(X_test, y_test))
