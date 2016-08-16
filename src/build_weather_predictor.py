"""
Generate, cross validate, and compare several candidate regression models.
"""

from __future__ import division
from build_base_table import prep_analytics_base_table
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LassoCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


def load_candidate_models():
    """
    Load the models to be tested.
    """
    models = dict()
    models['Linear Regression'] = LinearRegression(n_jobs=-1)
    models['Lasso Regression'] = LassoCV(n_jobs=-1, cv=5)
    models['Random Forest'] = GridSearchCV(
        RandomForestRegressor(n_jobs=-1), cv=5,
        param_grid={"max_depth": [3, 5]})
    models['Ada Boost'] = GridSearchCV(
        AdaBoostRegressor(), cv=5, param_grid={
            "loss": ['linear', 'square'], "learning_rate": [0.5, 1]})
    models['Gradient Boost'] = GridSearchCV(
        GradientBoostingRegressor(), cv=5, param_grid={
            "max_depth": [3, 5], "learning_rate": [0.1, 0.5, 1]})
    return models


def identify_best_model(abt):
    """
    Score the models, return best candidate
    """
    Y = abt.pop('Temp_Y')
    X = abt
    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    models = load_candidate_models()
    best_score = -1
    best_model_nm = None
    for model_nm, model in models.iteritems():
        model.fit(X_train, y_train)
        cv_score = model.score(X_test, y_test)
        if cv_score > best_score:
            best_model_nm = model_nm
        print model_nm + " metrics:"
        print "\tCross validated R^2 of {:.4}".format(str(cv_score))
        y_pred = model.predict(X_test)
        print "\tRMSE of {:.4}".format(str(mean_squared_error(
            y_test, y_pred)))
        print "\tMAE of {:.4}".format(str(mean_absolute_error(
            y_test, y_pred)))
    print "Best scoring model: "+best_model_nm
    return models[best_model_nm]


def model_temperature():
    """
    Generate, cross validate, and compare several candidate regression models.
    """
    k = 5
    min_distance = 200
    abt = prep_analytics_base_table(k, min_distance)
    model = identify_best_model(abt)


if __name__ == "__main__":
    model_temperature()
