import os
import numpy as np
import pandas as pd
import regression_methods
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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
    coeff, _ = curve_fit(fct_torque, x_, y_.flatten())
    k1, k2, k3, k4 = coeff
    print(
        f"Torque[Nm] = {k1:.1e} * rot_speed[rpm]^{k2:.1e} * diameter[in]^{k3:.1e} * pitch[in]^{k4:.1e}")

    # predict data
    y_hat_ = fct_torque(x_, k1, k2, k3, k4)

    # plot
    plt.scatter(x_[:, 0], y_, label="true torque")
    plt.scatter(x_[:, 0], y_hat_, label="estimated torque")
    plt.xlabel("w [rpm]")
    plt.ylabel("t [Nm]")
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
    coeff, _ = curve_fit(fct_thrust, x_, y_.flatten())
    k1, k2, k3, k4 = coeff
    print(
        f"Thrust[Kgf] = {k1:.1e} * rot_speed[rpm]^{k2:.1e} * diameter[in]^{k3:.1e} * pitch[in]^{k4:.1e}")

    # predict data
    y_hat_ = fct_thrust(x_, k1, k2, k3, k4)

    # plot
    plt.scatter(x_[:, 0], y_, label="true thrust")
    plt.scatter(x_[:, 0], y_hat_, label="estimated thrust")
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
