import os
import numpy as np
import pandas as pd
import regression_methods
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, mean_absolute_error

propellers_folder = "Aldo/Propulsion/Datasets/Propellers"
torque_thrust_dataset_path_ = "Aldo/Propulsion/Datasets/Propellers/Torque_thrust_regression_dataset.csv"


def create_dataset():
    propellers_dataset = pd.read_csv(propellers_folder + "/Propellers.csv")
    torque_thrust_dataset_ = []
    torque_thrust_dataset_cols_ = [
        "Rotation speed (rpm)", "Torque (N⋅m)", "Thrust (kgf)"]
    for propeller in np.array(propellers_dataset):
        tests_file_list = os.listdir(propellers_folder+'/'+propeller[0])
        for test_file in tests_file_list:
            test_dataset = pd.read_csv(
                propellers_folder+'/'+propeller[0]+'/'+test_file)
            temp_dataset_ = test_dataset[torque_thrust_dataset_cols_]
            temp_dataset_[
                "Propeller diameter [in]"] = propeller[1]
            temp_dataset_[
                "Propeller pitch [in]"] = propeller[2]
            torque_thrust_dataset_.append(temp_dataset_)
    result = pd.concat(torque_thrust_dataset_)
    result.to_csv(torque_thrust_dataset_path_)


def torque_regression():
    # extract data
    input_columns_ = [
        "Rotation speed (rpm)", "Propeller diameter [in]", "Propeller pitch [in]"]
    output_columns_ = ["Torque (N⋅m)"]
    x_, y_ = regression_methods.extract_data_from_csv(
        torque_thrust_dataset_path_, input_columns_, output_columns_)

    # definition of the function to be optimised
    def fct_torque(X, k1, k2, k3, k4):
        rot_speed_ = X[:, 0].flatten()
        diameter_ = X[:, 1].flatten()
        pitch_ = X[:, 2].flatten()
        return k1*(rot_speed_**k2)*(diameter_**k3)*(pitch_**k4)

    # optimise fct and find parameters
    coeff, coeff_var = curve_fit(fct_torque, x_, y_.flatten())
    k1, k2, k3, k4 = coeff

    print("########################################################################################################")
    print(
        f"Torque[Nm] = {k1:.2e}[Nm/rpm*in^2] * rot_speed[rpm]^{k2:.2e} * diameter[in]^{k3:.2e} * pitch[in]^{k4:.2e}")

    # compute parameters std dev
    std_dev = np.sqrt(np.diag(coeff_var))

    # compute their min and max values with a 95% confidence interval
    k1_min = k1 - 2*std_dev[0]
    k1_max = k1 + 2*std_dev[0]
    k2_min = k2 - 2*std_dev[1]
    k2_max = k2 + 2*std_dev[1]
    k3_min = k3 - 2*std_dev[2]
    k3_max = k3 + 2*std_dev[2]
    k4_min = k4 - 2*std_dev[3]
    k4_max = k4 + 2*std_dev[3]

    # predict data
    y_hat_ = fct_torque(x_, k1, k2, k3, k4)
    y_hat_min_ = fct_torque(x_, k1_min, k2_min, k3_min, k4_min)
    y_hat_max_ = fct_torque(x_, k1_max, k2_max, k3_max, k4_max)

    # compute MSE
    MSE_ = mean_squared_error(y_, y_hat_)
    print(f"TORQUE MSE = {MSE_}")
    print("########################################################################################################")

    # plot
    plt.scatter(x_[:, 0], y_, label="true torque")
    plt.scatter(x_[:, 0], y_hat_, label="estimated torque")
    plt.scatter(x_[:, 0], y_hat_max_, label="estimated best case torque")
    plt.scatter(x_[:, 0], y_hat_min_, label="estimated worst case torque")
    plt.xlabel("w [rpm]")
    plt.ylabel("C [Nm]")
    plt.legend()
    plt.grid()
    plt.show()


def thrust_regression():
    # extract data
    input_columns_ = [
        "Rotation speed (rpm)", "Propeller diameter [in]", "Propeller pitch [in]"]
    output_columns_ = ["Thrust (kgf)"]
    x_, y_ = regression_methods.extract_data_from_csv(
        torque_thrust_dataset_path_, input_columns_, output_columns_)

    # definition of the function to be optimised
    def fct_thrust(X, k1, k2, k3, k4):
        rot_speed_ = X[:, 0].flatten()
        diameter_ = X[:, 1].flatten()
        pitch_ = X[:, 2].flatten()
        return k1*(rot_speed_**k2)*(diameter_**k3)*(pitch_**k4)

    # optimise fct and find parameters
    coeff, coeff_var = curve_fit(fct_thrust, x_, y_.flatten())
    k1, k2, k3, k4 = coeff

    print("########################################################################################################")
    print(
        f"Thrust[Kgf] = {k1:.2e}[Kgf/rpm*in^2] * rot_speed[rpm]^{k2:.2e} * diameter[in]^{k3:.2e} * pitch[in]^{k4:.2e}")

    # compute parameters std dev
    std_dev = np.sqrt(np.diag(coeff_var))

    # compute their min and max values with a 95% confidence interval
    k1_min = k1 - 2*std_dev[0]
    k1_max = k1 + 2*std_dev[0]
    k2_min = k2 - 2*std_dev[1]
    k2_max = k2 + 2*std_dev[1]
    k3_min = k3 - 2*std_dev[2]
    k3_max = k3 + 2*std_dev[2]
    k4_min = k4 - 2*std_dev[3]
    k4_max = k4 + 2*std_dev[3]

    # predict data
    y_hat_ = fct_thrust(x_, k1, k2, k3, k4)
    y_hat_min_ = fct_thrust(x_, k1_min, k2_min, k3_min, k4_min)
    y_hat_max_ = fct_thrust(x_, k1_max, k2_max, k3_max, k4_max)

    # compute MSE
    MSE_ = mean_squared_error(y_, y_hat_)
    print(f"THRUST MSE = {MSE_}")
    print("########################################################################################################")

    # plot
    plt.scatter(x_[:, 0], y_, label="true thrust")
    plt.scatter(x_[:, 0], y_hat_, label="estimated thrust")
    plt.scatter(x_[:, 0], y_hat_max_, label="estimated best case thrust")
    plt.scatter(x_[:, 0], y_hat_min_, label="estimated worst case thrust")
    plt.xlabel("w [rpm]")
    plt.ylabel("T [Kgf]")
    plt.legend()
    plt.grid()
    plt.show()


def main():
    torque_regression()
    thrust_regression()


if __name__ == "__main__":
    main()
