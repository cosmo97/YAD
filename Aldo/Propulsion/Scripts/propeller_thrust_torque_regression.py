import os
from pickle import FALSE
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

PROPELLERS_FOLDER = "Aldo/Propulsion/Datasets/Propellers"
TEST_TRAIN_DATASET_RATIO = 0.3
PLOT_DATA = True


def create_dataset():
    propellers_dataset = pd.read_csv(PROPELLERS_FOLDER + "/Propellers.csv")
    torque_thrust_dataset_ = []
    propeller_num = 1
    torque_thrust_dataset_cols_ = [
        "Rotation speed (rpm)", "Torque (N⋅m)", "Thrust (kgf)"]
    for propeller in np.array(propellers_dataset):
        tests_file_list = os.listdir(PROPELLERS_FOLDER+'/'+propeller[0])
        for test_file in tests_file_list:
            test_dataset = pd.read_csv(
                PROPELLERS_FOLDER+'/'+propeller[0]+'/'+test_file)
            temp_dataset_ = test_dataset[torque_thrust_dataset_cols_]
            temp_dataset_[
                "Propeller diameter [in]"] = propeller[1]
            temp_dataset_[
                "Propeller pitch [in]"] = propeller[2]
            temp_dataset_[
                "Propeller num"] = propeller_num
            torque_thrust_dataset_.append(temp_dataset_)
        propeller_num = propeller_num + 1
    result = pd.concat(torque_thrust_dataset_)
    return result


def torque_regression(dataset_):
    # extract data
    input_columns_ = [
        "Rotation speed (rpm)", "Propeller diameter [in]", "Propeller pitch [in]", "Propeller num"]
    output_columns_ = ["Torque (N⋅m)"]
    x_ = np.array(dataset_[input_columns_])
    y_ = np.array(dataset_[output_columns_])

    # split in test and train datasets
    x_train_, x_test_, y_train_, y_test_ = train_test_split(
        x_, y_, test_size=TEST_TRAIN_DATASET_RATIO, random_state=1)

    # definition of the function to be optimised
    def fct_torque(X, k1, k2, k3, k4):
        rot_speed_ = X[:, 0].flatten()
        diameter_ = X[:, 1].flatten()
        pitch_ = X[:, 2].flatten()
        return k1*(rot_speed_**k2)*(diameter_**k3)*(pitch_**k4)

    # optimise fct and find parameters
    coeff, coeff_var = curve_fit(fct_torque, x_train_, y_train_.flatten())
    k1, k2, k3, k4 = coeff

    print(
        f"\nTorque[Nm] = {k1:.2e} * rot_speed[rpm]^{k2:.2e} * diameter[in]^{k3:.2e} * pitch[in]^{k4:.2e}")

    # compute parameters std dev
    coeff_std_dev = np.sqrt(np.diag(coeff_var))

    # compute their min and max values with a 66% confidence interval
    k1_min = k1 - coeff_std_dev[0]
    k1_max = k1 + coeff_std_dev[0]
    k2_min = k2 - coeff_std_dev[1]
    k2_max = k2 + coeff_std_dev[1]
    k3_min = k3 - coeff_std_dev[2]
    k3_max = k3 + coeff_std_dev[2]
    k4_min = k4 - coeff_std_dev[3]
    k4_max = k4 + coeff_std_dev[3]

    # predict test data
    y_hat_test_ = fct_torque(x_test_, k1, k2, k3, k4)

    # compute MSE on test data
    MSE_ = mean_squared_error(y_test_, y_hat_test_)
    MAE_ = mean_absolute_error(y_test_, y_hat_test_)
    print(f"TORQUE MSE = {MSE_}")
    print(f"TORQUE MAE = {MAE_}")

    # predict data on whole dataset for plots
    y_hat_ = fct_torque(x_, k1, k2, k3, k4)
    y_hat_min_ = fct_torque(x_, k1_min, k2_min, k3_min, k4_min)
    y_hat_max_ = fct_torque(x_, k1_max, k2_max, k3_max, k4_max)

    # plot
    if PLOT_DATA is True:
        num_propellers = int(max(x_[:, 3]))
        for propeller in range(1, num_propellers+1):
            propeller_indices = [i for i, x in enumerate(
                x_[:, 3]) if x == propeller]
            plt.scatter(x_[propeller_indices, 0], y_hat_[
                        propeller_indices], label="estimated torque", s=10)
            plt.scatter(x_[propeller_indices, 0], y_hat_max_[
                        propeller_indices], label="estimated best case torque", s=10)
            plt.scatter(x_[propeller_indices, 0], y_hat_min_[
                        propeller_indices], label="estimated worst case torque", s=10)
            plt.scatter(x_[propeller_indices, 0], y_[
                propeller_indices], label="true torque", s=5)
            plt.xlabel("w [rpm]")
            plt.ylabel("C [Nm]")
            plt.title(f"Propeller {propeller} torque")
            plt.legend()
            plt.grid()
            plt.show()


def thrust_regression(dataset_):
    # extract data
    input_columns_ = [
        "Rotation speed (rpm)", "Propeller diameter [in]", "Propeller pitch [in]", "Propeller num"]
    output_columns_ = ["Thrust (kgf)"]
    x_ = np.array(dataset_[input_columns_])
    y_ = np.array(dataset_[output_columns_])

    # split in test and train datasets
    x_train_, x_test_, y_train_, y_test_ = train_test_split(
        x_, y_, test_size=TEST_TRAIN_DATASET_RATIO, random_state=1)

    # definition of the function to be optimised
    def fct_thrust(X, k1, k2, k3, k4):
        rot_speed_ = X[:, 0].flatten()
        diameter_ = X[:, 1].flatten()
        pitch_ = X[:, 2].flatten()
        return k1*(rot_speed_**k2)*(diameter_**k3)*(pitch_**k4)

    # optimise fct and find parameters
    coeff, coeff_var = curve_fit(fct_thrust, x_train_, y_train_.flatten())
    k1, k2, k3, k4 = coeff

    print(
        f"\nThrust[Kgf] = {k1:.2e} * rot_speed[rpm]^{k2:.2e} * diameter[in]^{k3:.2e} * pitch[in]^{k4:.2e}")

    # compute parameters std dev
    coeff_std_dev = np.sqrt(np.diag(coeff_var))

    # compute their min and max values with a 66% confidence interval
    k1_min = k1 - coeff_std_dev[0]
    k1_max = k1 + coeff_std_dev[0]
    k2_min = k2 - coeff_std_dev[1]
    k2_max = k2 + coeff_std_dev[1]
    k3_min = k3 - coeff_std_dev[2]
    k3_max = k3 + coeff_std_dev[2]
    k4_min = k4 - coeff_std_dev[3]
    k4_max = k4 + coeff_std_dev[3]

    # predict data
    y_hat_test_ = fct_thrust(x_test_, k1, k2, k3, k4)

    # compute MSE on test data
    MSE_ = mean_squared_error(y_test_, y_hat_test_)
    MAE_ = mean_absolute_error(y_test_, y_hat_test_)
    print(f"THRUST MSE = {MSE_}")
    print(f"THRUST MAE = {MAE_}")

    # predict data on whole dataset for plots
    y_hat_ = fct_thrust(x_, k1, k2, k3, k4)
    y_hat_min_ = fct_thrust(x_, k1_min, k2_min, k3_min, k4_min)
    y_hat_max_ = fct_thrust(x_, k1_max, k2_max, k3_max, k4_max)

    # plot
    if PLOT_DATA is True:
        num_propellers = int(max(x_[:, 3]))
        for propeller in range(1, num_propellers+1):
            propeller_indices = [i for i, x in enumerate(
                x_[:, 3]) if x == propeller]
            plt.scatter(x_[propeller_indices, 0], y_hat_[
                        propeller_indices], label="estimated thrust", s=10)
            plt.scatter(x_[propeller_indices, 0], y_hat_max_[
                        propeller_indices], label="estimated best case thrust", s=10)
            plt.scatter(x_[propeller_indices, 0], y_hat_min_[
                        propeller_indices], label="estimated worst case thrust", s=10)
            plt.scatter(x_[propeller_indices, 0], y_[
                        propeller_indices], label="true thrust", s=5)
            plt.xlabel("w [rpm]")
            plt.ylabel("T [Kgf]")
            plt.title(f"Propeller {propeller} thrust")
            plt.legend()
            plt.grid()
            plt.show()


def main():
    dataset_ = create_dataset()
    torque_regression(dataset_)
    thrust_regression(dataset_)


if __name__ == "__main__":
    main()
