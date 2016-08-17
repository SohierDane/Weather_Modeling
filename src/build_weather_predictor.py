"""
Generate, cross validate, and compare several candidate regression models.
"""

from __future__ import division
import pickle
from build_base_table import prep_analytics_base_table
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


model_pickle_path = "weather_model.p"


def load_candidate_models():
    """
    Load the models to be tested.
    """
    models = dict()
    models['Linear Regression'] = LinearRegression(n_jobs=-1)
    models['Random Forest'] = GridSearchCV(
        RandomForestRegressor(n_jobs=-1), cv=5,
        param_grid={"max_depth": [3, 5]})
    models['Ada Boost'] = GridSearchCV(
        AdaBoostRegressor(), cv=5, param_grid={
            "loss": ['linear', 'square'], "learning_rate": [0.05, 0.1]})
    models['Gradient Boost'] = GridSearchCV(
        GradientBoostingRegressor(), cv=5, param_grid={
            "max_depth": [4, 5], "learning_rate": [0.05, 0.1, 0.5]})
    return models


def fit_n_score(model, X_train, X_test, y_train, y_test, model_nm):
    """
    Fits model & reports key metrics
    """
    model.fit(X_train, y_train)
    print "\n{0} metrics:".format(model_nm)
    print "\tCross validated R^2 of {:.4}".format(
        model.score(X_test, y_test))
    y_pred = model.predict(X_test)
    print "\tRMSE of {:.4}".format(str(mean_squared_error(
        y_test, y_pred)))
    print "\tMAE of {:.4}".format(str(mean_absolute_error(
        y_test, y_pred)))
    return model


def identify_best_model(abt):
    """
    Score the models, return best candidate.

    Does not report most important features as these are routinely just the
    temperatures ranked in order of X station distance.
    """
    Y = abt.pop('Temp_Y')
    X = abt
    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    models = load_candidate_models()
    best_score = -1
    best_model_nm = None
    for model_nm, model in models.iteritems():
        model = fit_n_score(model, X_train, X_test, y_train, y_test, model_nm)
        cv_score = model.score(X_test, y_test)
        if cv_score > best_score:
            best_model_nm = model_nm
            best_score = cv_score
            best_model = model
    print "Best scoring model: {0}".format(best_model_nm)
    return best_model


def model_temperature():
    """
    Generate, cross validate, and compare several candidate regression models.

    number of neighbors of 5 selected using cross validation.
    """
    num_neighbors = 5
    min_distance = 200
    abt = prep_analytics_base_table(num_neighbors, min_distance)
    return identify_best_model(abt)


def load_best_model():
    """
    Loads the best model from a prior run. Saves several minutes of time
    when running on a laptop.
    """
    global model_pickle_path
    return pickle.load(open(model_pickle_path, 'rb'))


def evaluate_station_density_importance(model):
    """
    Tests the impact of changing the number of neighbors used and
    the minimum distance.
    """
    neighbs_scores = {}
    for num_neighbors in range(1, 9):
        min_distance = 200
        abt = prep_analytics_base_table(num_neighbors, min_distance)
        Y = abt.pop('Temp_Y')
        X = abt
        X_train, X_test, y_train, y_test = train_test_split(X, Y)
        model = fit_n_score(model, X_train, X_test, y_train, y_test,
                            str(type(model)))
        neighbs_scores[num_neighbors] = model.score(X_test, y_test)
    dist_scores = {}
    for min_distance in range(100, 1100, 100):
        num_neighbors = 5
        abt = prep_analytics_base_table(num_neighbors, min_distance)
        Y = abt.pop('Temp_Y')
        X = abt
        X_train, X_test, y_train, y_test = train_test_split(X, Y)
        model = fit_n_score(model, X_train, X_test, y_train, y_test,
                            str(type(model)))
        dist_scores[min_distance] = model.score(X_test, y_test)
    return neighbs_scores, dist_scores


if __name__ == "__main__":
    model = model_temperature()
    pickle.dump(model, open(model_pickle_path, "wb+"))
