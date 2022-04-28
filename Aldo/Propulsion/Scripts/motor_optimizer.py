import math
import numpy as np
import pandas as pd
from scipy import optimize

# Datasets
BATTERIES_DATASET = "Aldo/Propulsion/Datasets/Batteries/Batteries.csv"
MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"
PROPELLERS_DATASET = "Aldo/Propulsion/Datasets/Propellers/Propellers.csv"

# System constraints
MIN_THRUST = 0.500      # kgf, 2 times of the weight for control authority
HOVER_THRUST = 0.250    # kgf
MAX_WEIGHT = 250        # grams, maybe less for frame/board
MIN_HOVERING_TIME = 8   # minutes

# Default values if NaN, TODO
DEFAULT_RESISTANCE = 0.0      # Ohm
DEFAULT_NOLOAD_CURRENT = 0.0  # Ampere


def motor_speed(rot_speed, Kv, pwm, voltage, current, resistance):
    """TODO

    Args:
        rot_speed (_type_): _description_
        Kv (_type_): _description_
        pwm (_type_): _description_
        voltage (_type_): _description_
        current (_type_): _description_
        resistance (_type_): _description_

    Returns:
        _type_: _description_
    """

    if pwm > 1.0:
        pwm = 1.0

    if math.isnan(resistance):
        resistance = DEFAULT_RESISTANCE

    return rot_speed - Kv*(pwm*voltage - resistance*current)


def motor_torque(torque, current, Kv, noload_current):
    """TODO

    Args:
        torque (_type_): _description_
        current (_type_): _description_
        Kv (_type_): _description_
        noload_current (_type_): _description_

    Returns:
        _type_: _description_
    """

    if math.isnan(noload_current):
        noload_current = DEFAULT_NOLOAD_CURRENT

    return torque - (current + noload_current)/(Kv*np.pi/30)


def prop_torque(rot_speed, torque, diameter, pitch):
    """TODO

    Args:
        rot_speed (_type_): _description_
        torque (_type_): _description_
        diameter (_type_): _description_
        pitch (_type_): _description_

    Returns:
        _type_: _description_
    """

    return torque - 5.75e-14*(rot_speed**1.85e+00) * \
        (diameter**3.44e+00)*(pitch**2.59e+00)


def prop_thrust(rot_speed, thrust, diameter, pitch):
    """TODO

    Args:
        rot_speed (_type_): _description_
        thrust (_type_): _description_
        diameter (_type_): _description_
        pitch (_type_): _description_

    Returns:
        _type_: _description_
    """
    return thrust - 4.33e-12*(rot_speed**1.88e+00) * \
        (diameter**2.83e+00)*(pitch**1.60e+00)


def equations_at_max_pwm(x, args):
    """TODO

    Args:
        x (_type_): _description_
        args (_type_): _description_

    Returns:
        _type_: _description_
    """

    rot_speed, torque, current, thrust = x
    diameter, pitch, Kv, voltage, noload_current, resistance = args

    return [
        prop_torque(rot_speed, torque, diameter, pitch),
        prop_thrust(rot_speed, thrust, diameter, pitch),
        motor_speed(rot_speed, Kv, 1.0, voltage, current, resistance),
        motor_torque(torque, current, Kv, noload_current)
    ]


def equations_at_hovering(x, args):
    """TODO

    Args:
        x (_type_): _description_
        args (_type_): _description_

    Returns:
        _type_: _description_
    """

    rot_speed, torque, current, pwm = x
    diameter, pitch, Kv, voltage, noload_current, resistance = args

    return [
        prop_torque(rot_speed, torque, diameter, pitch),
        prop_thrust(rot_speed, HOVER_THRUST, diameter, pitch),
        motor_speed(rot_speed, Kv, pwm, voltage, current, resistance),
        motor_torque(torque, current, Kv, noload_current)
    ]


def solve_equations(x, equations):
    """TODO

    Args:
        df (_type_): _description_
    """

    return optimize.fsolve(
        equations,
        x0=[0, 0, 0, 0],
        args=x[[
            "Propeller diameter (in)",
            "Propeller pitch (in)",
            "KV [rpm/V]",
            "Nominal voltage [V]",
            "No load current (A)",
            "Resistance (Ohm)"
        ]]
    )


def main():
    """TODO

    Returns:
        _type_: _description_
    """

    # Retrieve batteries/motors/propellers parameters
    batteries_df = pd.read_csv(BATTERIES_DATASET)
    motors_df = pd.read_csv(MOTORS_DATASET)
    propellers_df = pd.read_csv(PROPELLERS_DATASET)

    # DataFrame of all possible batteries/motors/propellers combinations
    combination_df = pd.merge(batteries_df, motors_df, how="cross")
    combination_df = pd.merge(combination_df, propellers_df, how="cross")

    # Solve system for 100% pwm
    combination_df[[
        "Max PWM rotational speed (rpm)",
        "Max PWM torque (Nm)",
        "Max PWM current (A)",
        "Max PWM thrust (kgf)"
    ]] = combination_df.apply(
        solve_equations,
        args=[equations_at_max_pwm],
        axis=1,
        result_type="expand")

    # Solve system for hovering
    combination_df[[
        "Hovering rotational speed (rpm)",
        "Hovering torque (Nm)",
        "Hovering current (A)",
        "Hovering thrust (kgf)"
    ]] = combination_df.apply(
        solve_equations,
        args=[equations_at_hovering],
        axis=1,
        result_type="expand")

    combination_df.to_csv("Aldo/Propulsion/Datasets/Combinations.csv")


if __name__ == "__main__":
    main()
