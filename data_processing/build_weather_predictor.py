"""

"""
from __future__ import division
import pandas as pd
from build_base_table import prep_analytics_base_table
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import f1_score, accuracy_score, precision_score, \
    recall_score


def run_model(Model, X_train, X_test, y_train, y_test):
    m = Model()
    m.fit(X_train, y_train)
    y_predict = m.predict(X_test)
    return (accuracy_score(y_test, y_predict),
            f1_score(y_test, y_predict),
            precision_score(y_test, y_predict),
            recall_score(y_test, y_predict))

if __name__ == "__main__":
    k = 5
    abt = prep_analytics_base_table(5)
    Y = abt.pop('Temp_Y')
    X = abt
    X_train, X_test, y_train, y_test = train_test_split(abt)
