import math
import numpy as np
import pandas as pd
from scipy import optimize
from tqdm import tqdm

# Datasets
BATTERIES_DATASET = "Aldo/Propulsion/Datasets/Batteries/Batteries.csv"
MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"
PROPELLERS_DATASET = "Aldo/Propulsion/Datasets/Propellers/Propellers.csv"
RESULTS_DATASET_FOLDER = "Aldo/Propulsion/Datasets/Results/"

# Safety factors
SAFETY_FACTOR = 1.2

# System constraints
HOVERING_THRUST = 0.250  # kgf
MIN_PEAK_THRUST = 2 * HOVERING_THRUST  # kgf
MIN_HOVERING_PWM = 0.1  # 10 %
MAX_HOVERING_PWM = 0.9  # 90 %
MAX_WEIGHT = 250  # grams
MIN_HOVERING_TIME = 5  # minutes
MAX_COST = 100  # euros
# TODO insert cost for each component (at least battery and motor)

# Default values if NaN, TODO estimate resistance
DEFAULT_RESISTANCE = 0.0  # Ohm
DEFAULT_NOLOAD_CURRENT = 0.0  # Ampere


def motor_speed(rot_speed, kv, pwm, voltage, resistance, current):
    """TODO

    Args:
        rot_speed (_type_): _description_
        kv (_type_): _description_
        pwm (_type_): _description_
        voltage (_type_): _description_
        resistance (_type_): _description_
        current (_type_): _description_

    Returns:
        _type_: _description_
    """

    if math.isnan(resistance):
        resistance = DEFAULT_RESISTANCE

    return rot_speed - kv * (pwm * voltage - resistance * current)


def motor_torque(torque, current, noload_current, kv):
    """TODO

    Args:
        torque (_type_): _description_
        current (_type_): _description_
        noload_current (_type_): _description_
        kv (_type_): _description_

    Returns:
        _type_: _description_
    """

    if math.isnan(noload_current):
        noload_current = DEFAULT_NOLOAD_CURRENT

    return torque - (current - noload_current) / (kv * np.pi / 30)


def prop_torque(torque, rot_speed, diameter, pitch):
    """TODO

    Args:
        torque (_type_): _description_
        rot_speed (_type_): _description_
        diameter (_type_): _description_
        pitch (_type_): _description_

    Returns:
        _type_: _description_
    """

    return torque - 5.75e-14*(rot_speed**1.85e+00) * \
        (diameter**3.44e+00)*(pitch**2.59e+00)


def prop_thrust(thrust, rot_speed, diameter, pitch):
    """TODO

    Args:
        thrust (_type_): _description_
        rot_speed (_type_): _description_
        diameter (_type_): _description_
        pitch (_type_): _description_

    Returns:
        _type_: _description_
    """

    return thrust - 4.33e-12*(rot_speed**1.88e+00) * \
        (diameter**2.83e+00)*(pitch**1.60e+00)


def equations_at_peak(x, *args):
    """TODO

    Args:
        x (_type_): _description_
        args (_type_): _description_

    Returns:
        _type_: _description_
    """

    rot_speed, torque, current, thrust = x
    diameter, pitch, kv, voltage, noload_current, resistance = args

    return [
        prop_torque(torque, rot_speed, diameter, pitch),
        prop_thrust(thrust, rot_speed, diameter, pitch),
        motor_speed(rot_speed, kv, 1.0, voltage, resistance, current),
        motor_torque(torque, current, noload_current, kv)
    ]


def equations_at_hovering(x, *args):
    """TODO

    Args:
        x (_type_): _description_
        args (_type_): _description_

    Returns:
        _type_: _description_
    """

    rot_speed, torque, current, pwm = x
    diameter, pitch, kv, voltage, noload_current, resistance = args

    return [
        prop_torque(torque, rot_speed, diameter, pitch),
        prop_thrust(HOVERING_THRUST / 4, rot_speed, diameter, pitch),
        motor_speed(rot_speed, kv, pwm, voltage, resistance, current),
        motor_torque(torque, current, noload_current, kv)
    ]


def solve_equations(x,
                    equations,
                    x0=np.zeros(4),
                    bounds=([-math.inf] * 4, [math.inf] * 4)):
    """TODO

    Args:
        df (_type_): _description_
    """

    sol = optimize.least_squares(equations,
                                 x0,
                                 "2-point",
                                 bounds,
                                 args=(x[[
                                     "Propeller diameter (in)",
                                     "Propeller pitch (in)", "KV (rpm/V)",
                                     "Nominal voltage (V)",
                                     "No load current @10V (A)", "Resistance (Ohm)"
                                 ]]))

    return sol.x if sol.cost < 1e-8 else [math.nan] * 4


def main():
    """TODO

    Returns:
        _type_: _description_
    """

    tqdm.pandas()

    # Retrieve batteries/motors/propellers parameters
    batteries_df = pd.read_csv(BATTERIES_DATASET)
    motors_df = pd.read_csv(MOTORS_DATASET)
    propellers_df = pd.read_csv(PROPELLERS_DATASET)

    # DataFrame of all possible batteries/motors/propellers combinations
    combination_df = pd.merge(batteries_df, motors_df, how="cross")
    combination_df = pd.merge(combination_df, propellers_df, how="cross")

    # Solving total weight
    print("Solving total weight")
    combination_df["Total weight (g)"] = combination_df.progress_apply(
        lambda x: x["Battery weight (g)"] + 4 *
        (x["Motor weight (g)"] + x["Propeller weight (g)"]),
        axis=1,
        result_type="expand")

    # Save combinations before filter
    print(f"Total possible combinations: {len(combination_df)}")
    combination_df.to_csv(RESULTS_DATASET_FOLDER + "AllCombinations.csv")

    # Filtering weight
    combination_df = combination_df[combination_df["Total weight (g)"] *
                                    SAFETY_FACTOR < MAX_WEIGHT]

    # Solve system for peak thrust
    print("Solving peak")
    combination_df[[
        "Peak rotational speed (rpm)", "Peak torque (Nm)", "Peak current (A)",
        "Peak thrust (kgf)"
    ]] = combination_df.progress_apply(
        solve_equations,
        bounds=([0, 0, 0, 0], [math.inf, math.inf, math.inf, math.inf]),
        args=[equations_at_peak],
        axis=1,
        result_type="expand")

    # Solving total thrust
    print("Solving total thrust")
    combination_df["Total thrust (kgf)"] = combination_df.progress_apply(
        lambda x: 4 * x["Peak thrust (kgf)"], axis=1, result_type="expand")

    # Save combinations before filter
    print(f"Weight filtered combinations: {len(combination_df)}")
    combination_df.to_csv(RESULTS_DATASET_FOLDER +
                          "WeightFilteredCombinations.csv")

    # Filtering thrust
    combination_df = combination_df[
        combination_df["Total thrust (kgf)"] > SAFETY_FACTOR * MIN_PEAK_THRUST]

    # Solve system for hovering
    print("Solving hovering")
    combination_df[[
        "Hovering rotational speed (rpm)", "Hovering torque (Nm)",
        "Hovering current (A)", "Hovering PWM"
    ]] = combination_df.progress_apply(solve_equations,
                                       x0=[0, 0, 0, MAX_HOVERING_PWM],
                                       bounds=([0, 0, 0, MIN_HOVERING_PWM], [
                                           math.inf, math.inf, math.inf,
                                           MAX_HOVERING_PWM
                                       ]),
                                       args=[equations_at_hovering],
                                       axis=1,
                                       result_type="expand")

    # Solving hovering time
    print("Solving hovering time")
    combination_df["Hovering time (m)"] = combination_df.progress_apply(
        lambda x: 60 * (0.001 * x["Capacity (mah)"]) /
        (4 * x["Hovering current (A)"]),
        axis=1,
        result_type="expand")

    # Save combinations before filter
    print(f"Thrust filtered combinations: {len(combination_df)}")
    combination_df.to_csv(RESULTS_DATASET_FOLDER +
                          "ThrustFilteredCombinations.csv")

    # Filtering hovering time
    combination_df = combination_df[combination_df["Hovering time (m)"] >
                                    MIN_HOVERING_TIME * SAFETY_FACTOR]

    # Save hovering time filtered combinations
    print(f"Hovering time filtered combinations: {len(combination_df)}")
    combination_df.sort_values("Hovering time (m)",
                               inplace=True,
                               ascending=False)
    combination_df.to_csv(RESULTS_DATASET_FOLDER +
                          "HoveringTimeFilteredCombinations.csv")

    # Filtering current at hovering
    combination_df = combination_df[4 * combination_df["Hovering current (A)"] * SAFETY_FACTOR
                                    < (0.001*combination_df["Capacity (mah)"] * combination_df["Discharge (C)"])]

    # Save hovering current filtered combinations
    print(f"Hovering current filtered combinations: {len(combination_df)}")
    combination_df.to_csv(RESULTS_DATASET_FOLDER +
                          "HoveringCurrentFilteredCombinations.csv")


if __name__ == "__main__":
    main()
