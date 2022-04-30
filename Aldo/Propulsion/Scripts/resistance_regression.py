from cmath import nan
from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error, mean_absolute_error

MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"

motors_df = pd.read_csv(MOTORS_DATASET)

labels = ["Stator diameter (mm)", "Stator height (mm)", "Motor diameter (mm)", "Motor height (mm)",
          "Motor weight (g)", "KV (rpm/V)", "Resistance (Ohm)"]

resistance_df = motors_df[labels].dropna()

resistance_df["Motor volume (mm^3)"] = resistance_df["Motor height (mm)"] * \
    resistance_df["Motor diameter (mm)"]

plt.scatter(resistance_df["Motor height (mm)"],
            resistance_df["Resistance (Ohm)"])
plt.grid("minor")
plt.xlabel("Stator height (mm)")
plt.ylabel("Resistance (Ohm)")
plt.title("Motor resistance wrt height")
plt.show()

plt.scatter(resistance_df["Motor volume (mm^3)"],
            resistance_df["Resistance (Ohm)"])
plt.grid("minor")
plt.xlabel("Stator volume (mm^3)")
plt.ylabel("Resistance (Ohm)")
plt.title("Motor resistance wrt volume")
plt.show()

plt.scatter(resistance_df["KV (rpm/V)"],
            resistance_df["Resistance (Ohm)"])
plt.grid("minor")
plt.xlabel("KV (rpm/V)")
plt.ylabel("Resistance (Ohm)")
plt.title("Motor resistance wrt kv")
plt.show()
