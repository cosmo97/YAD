from cmath import nan
from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
import numpy as np

MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"


def import_data():
    motors_df = pd.read_csv(MOTORS_DATASET)
    labels = ["Motor diameter (mm)", "Motor height (mm)",
              "Motor weight (g)", "KV (rpm/V)", "Resistance (Ohm)"]
    resistance_df = motors_df[labels].dropna()
    return resistance_df


def compute_volume(resistance_df):
    resistance_df["Motor volume (mm^3)"] = np.pi * resistance_df["Motor height (mm)"] * \
        (resistance_df["Motor diameter (mm)"])**2 / 4
    return resistance_df


def plot(resistance_df):
    plt.scatter(resistance_df["Motor volume (mm^3)"],
                resistance_df["Resistance (Ohm)"])
    plt.scatter(resistance_df["Motor volume (mm^3)"],
                resistance_df["Estimated resistance (Ohm)"])
    plt.grid("minor")
    plt.xlabel("Motor volume (mm^3)")
    plt.ylabel("Resistance (Ohm)")
    plt.title("Motor resistance wrt volume")
    plt.show()


def compute_linear_model(resistance_df):
    X = np.array(resistance_df["Motor volume (mm^3)"]).reshape(-1, 1)
    y = np.array(resistance_df["Resistance (Ohm)"]).reshape(-1, 1)
    linear_model = LinearRegression().fit(X, y)
    return linear_model


def estimate_resistance(resistance_df, linear_model):
    X = np.array(resistance_df["Motor volume (mm^3)"]).reshape(-1, 1)
    resistance_df["Estimated resistance (Ohm)"] = linear_model.predict(X)
    return resistance_df


def main():
    resistance_df = import_data()
    resistance_df = compute_volume(resistance_df)
    linear_model = compute_linear_model(resistance_df)
    resistance_df = estimate_resistance(resistance_df, linear_model)
    print(f"Estimated resistance = {linear_model.coef_[0][0]} * Volume")
    plot(resistance_df)


if __name__ == "__main__":
    main()
