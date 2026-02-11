import numpy as np
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def train(X, y):
    # train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)

    # fit
    model.fit(X_train, y_train)

    # evaluate prediction
    y_pred = model.predict(X_test)

    r2 = r2_score(y_test, y_pred)
    mse = mean_absolute_error(y_test, y_pred)

    print("R2:", r2)
    print("Mean Absolute Error:", mse)

    return model


