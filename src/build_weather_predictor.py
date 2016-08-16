"""
Generates, cross validates, and compares several candidate regression models.
"""

from __future__ import division
from build_base_table import prep_analytics_base_table
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV


def model_temperature():
    """
    Generates, cross validates, and compares several candidate regression models.
    """
    k = 5
    min_distance = 200
    abt = prep_analytics_base_table(k, min_distance)
    Y = abt.pop('Temp_Y')
    X = abt
    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    models = dict()
    models['Linear Regression'] = LinearRegression(n_jobs=-1)
    models['Random Forest'] = GridSearchCV(
        RandomForestRegressor(n_jobs=-1), cv=5,
        param_grid={"max_depth": [3, 5]})
    models['Ada Boost'] = GridSearchCV(
        AdaBoostRegressor(n_jobs=-1), cv=5, param_grid={
            "max_depth": [3, 5], "learning_rate": [0.5, 1]})
    models['Gradient Boost'] = GridSearchCV(
        GradientBoostingRegressor(n_jobs=-1), cv=5, param_grid={
            "max_depth": [3, 5], "learning_rate": [0.5, 1]})
    for model_nm, model in models.iteritems():
        model.fit(X_train, y_train)
        print model_nm+" scored "+str(model.score(X_test, y_test))


if __name__ == "__main__":
    model_temperature()
