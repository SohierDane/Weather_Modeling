"""

"""
from __future__ import division
import pandas as pd
from build_base_table import prep_analytics_base_table
from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline


if __name__ == "__main__":
    k = 5
    min_distance = 200
    abt = prep_analytics_base_table(k, min_distance)
    Y = abt.pop('Temp_Y')
    X = abt
    X_train, X_test, y_train, y_test = train_test_split(X, Y)
    m = RandomForestRegressor()
    m.fit(X_train, y_train)
    print "R^2 of "+str(m.score(X_test, y_test))
