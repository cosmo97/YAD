from pandas import read_csv
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

TEST_TRAIN_DATASET_RATIO = 0.3
K_FOLD_SPLITS = 10
K_FOLD_REPEAT = 3


def extract_data_from_csv(csv_file_path_, input_columns_, output_columns_):
    dataset_ = read_csv(csv_file_path_)
    x_ = np.array(dataset_[input_columns_])
    y_ = np.array(dataset_[output_columns_])
    return x_, y_


def preprocess_data(x_, y_):
    x_train_, x_test_, y_train_, y_test_ = train_test_split(
        x_, y_, test_size=TEST_TRAIN_DATASET_RATIO, random_state=1)
    preprocesser_ = StandardScaler()
    x_train_ = preprocesser_.fit_transform(x_train_)
    x_test_ = preprocesser_.fit_transform(x_test_)
    y_train_ = preprocesser_.fit_transform(y_train_)
    y_test_ = preprocesser_.fit_transform(y_test_)
    return x_train_, x_test_, y_train_, y_test_


def fit_ridge_model_to_data(x_train_, y_train_):
    cross_validation_ = RepeatedKFold(
        n_splits=K_FOLD_SPLITS, n_repeats=K_FOLD_REPEAT, random_state=1)
    model_ = RidgeCV(alphas=np.arange(0, 1, 0.01), cv=cross_validation_,
                     scoring='neg_mean_absolute_error')
    model_.fit(x_train_, y_train_)
    return model_


def test_model(model_, x_test_, y_test_):
    y_test_hat_ = model_.predict(x_test_)
    MSE_ = mean_squared_error(y_test_, y_test_hat_)
    MAE_ = mean_absolute_error(y_test_, y_test_hat_)
    return MSE_, MAE_, y_test_, y_test_hat_
