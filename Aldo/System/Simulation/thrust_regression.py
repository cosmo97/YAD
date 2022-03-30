import numpy as np
from pandas import read_csv
from numpy import arange
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

thrust_dataset_csv_ = "Aldo/System/Simulation/data/thrust_dataset.csv"


def extract_data_from_csv():
    dataset_ = read_csv(thrust_dataset_csv_)
    x_ = np.array([dataset_["motor width (mm)"].values,
                   dataset_["motor height (mm)"].values,
                   dataset_["Kv (rms/V)"].values,
                   dataset_["propeller diameter (in)"].values,
                   dataset_["propeller pitch (in)"].values,
                   dataset_["battery (V)"].values,
                   dataset_["PWM throttle (%)"].values]).transpose()
    y_ = np.array(dataset_["Thrust (kgf)"].values).reshape(-1, 1)
    return x_, y_


def preprocess_data(x_, y_):
    x_train_, x_test_, y_train_, y_test_ = train_test_split(
        x_, y_, test_size=0.05, random_state=1)
    preprocesser_ = StandardScaler()
    x_train_ = preprocesser_.fit_transform(x_train_)
    x_test_ = preprocesser_.fit_transform(x_test_)
    y_train_ = preprocesser_.fit_transform(y_train_)
    y_test_ = preprocesser_.fit_transform(y_test_)
    return x_train_, x_test_, y_train_, y_test_


def fit_ridge_model_to_data(x_train_, y_train_):
    # define model evaluation method
    cross_validation_ = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # define model
    model_ = RidgeCV(alphas=arange(0, 1, 0.01), cv=cross_validation_,
                     scoring='neg_mean_absolute_error')
    # fit model
    model_.fit(x_train_, y_train_)
    return model_


def test_model(model_, x_test_, y_test_):
    y_test_hat_ = model_.predict(x_test_)
    MSE_ = mean_squared_error(y_test_, y_test_hat_)
    MAE_ = mean_absolute_error(y_test_, y_test_hat_)
    print(f"""
********TEST DATA*********
------TRUE-----PREDICTED--
{np.concatenate([y_test_, y_test_hat_], axis=1)}""")
    print(f"MSE: {MSE_}")
    print(f"MAE: {MAE_}")
    return MSE_, MAE_


def main():
    x_, y_ = extract_data_from_csv()
    x_train_, x_test_, y_train_, y_test_ = preprocess_data(x_, y_)
    ridge_model_ = fit_ridge_model_to_data(x_train_, y_train_)
    MSE_ridge_, MAE_ridge_ = test_model(ridge_model_, x_test_, y_test_)


if __name__ == "__main__":
    main()
