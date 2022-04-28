import math
import numpy as np
import pandas as pd
from scipy import optimize
from tqdm import tqdm

# Datasets
BATTERIES_DATASET = "Aldo/Propulsion/Datasets/Batteries/Batteries.csv"
MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"
PROPELLERS_DATASET = "Aldo/Propulsion/Datasets/Propellers/Propellers.csv"

# System constraints
HOVERING_THRUST = 0.250              # kgf
MIN_PEAK_THRUST = 2*HOVERING_THRUST  # kgf
MAX_WEIGHT = 250                     # grams, maybe less for frame/board
MIN_HOVERING_TIME = 5                # minutes

# Default values if NaN, TODO
DEFAULT_RESISTANCE = 0.0      # Ohm
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

    return rot_speed - kv*(pwm*voltage - resistance*current)


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

    return torque - (current - noload_current)/(kv*np.pi/30)


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
        prop_thrust(HOVERING_THRUST, rot_speed, diameter, pitch),
        motor_speed(rot_speed, kv, pwm, voltage, resistance, current),
        motor_torque(torque, current, noload_current, kv)
    ]


def solve_equations(
        x, equations, x0=np.zeros(4), bounds=([-math.inf]*4, [math.inf]*4)):
    """TODO

    Args:
        df (_type_): _description_
    """

    sol = optimize.least_squares(
        equations, x0, "2-point", bounds,
        args=(x[[
                "Propeller diameter (in)",
                "Propeller pitch (in)",
                "KV (rpm/V)",
                "Nominal voltage (V)",
                "No load current (A)",
                "Resistance (Ohm)"
                ]]),
        method="dogbox"
    )

    return sol.x if sol.cost < 1e-4 else [math.nan]*4


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

    print(f"Possible combinations: {len(combination_df)}")

    # Filtering weight
    mask = (combination_df["Battery weight (g)"] +
            4 * (combination_df["Motor weight (g)"] +
                 combination_df["Propeller weight (g)"])) < MAX_WEIGHT
    combination_df = combination_df[mask]

    print(f"Weight filtered combination: {len(combination_df)}")

    # Solve system for peak
    print("Solving Peak")
    combination_df[[
        "Peak rotational speed (rpm)",
        "Peak torque (Nm)",
        "Peak current (A)",
        "Peak thrust (kgf)"
    ]] = combination_df.progress_apply(
        solve_equations,
        bounds=([0, 0, 0, 0], [math.inf, math.inf, math.inf, math.inf]),
        args=[equations_at_peak],
        axis=1,
        result_type="expand")

    # Filtering thrust
    mask = 4 * combination_df["Peak thrust (kgf)"] > MIN_PEAK_THRUST
    combination_df = combination_df[mask]

    print(f"Thrust filtered combination: {len(combination_df)}")

    # Solve system for hovering
    print("Solving Hovering")
    combination_df[[
        "Hovering rotational speed (rpm)",
        "Hovering torque (Nm)",
        "Hovering current (A)",
        "Hovering PWM"
    ]] = combination_df.progress_apply(
        solve_equations,
        x0=[0, 0, 0, 0.1],
        bounds=([0, 0, 0, 0.1], [math.inf, math.inf, math.inf, 1.0]),
        args=[equations_at_hovering],
        axis=1,
        result_type="expand")

    # Filtering hovering time
    mask = 60*(0.001*combination_df["Capacity (mah)"]) / \
        (4*combination_df["Hovering current (A)"]) > MIN_HOVERING_TIME
    combination_df = combination_df[mask]

    print(f"Hovering time combination: {len(combination_df)}")

    # Save combinations
    combination_df.to_csv("Aldo/Propulsion/Datasets/Combinations.csv")


if __name__ == "__main__":
    main()
