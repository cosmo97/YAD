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
        motor_speed(rot_speed, Kv, 1.0, voltage,
                    current, resistance),
        motor_torque(torque, current, Kv, noload_current)
    ]


def solve_at_max_pwm(x):
    """TODO

    Args:
        df (_type_): _description_
    """

    result = optimize.fsolve(
        equations_at_max_pwm,
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

    return np.transpose(result)


def combination_filter(conf):
    """TODO

    Args:
        conf (_type_): _description_

    Returns:
        _type_: _description_
    """
    return \
        4*float(conf[25]) > MIN_THRUST \
        and (float(conf[7])+4*float(conf[14])+4*float(conf[19])) < MAX_WEIGHT \
        and 60*((0.001*float(conf[0]))/(4*float(conf[28]))) > MIN_HOVERING_TIME


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
    combination_df[["1", "3", "w", "2"]
                   ] = combination_df.apply(solve_at_max_pwm, axis=1)

    combination_df.to_csv("Aldo/Propulsion/Datasets/Temp.csv")
    result_at_max_pwm_df.to_csv("Aldo/Propulsion/Datasets/resssss.csv")


if False:
    # Compute static performance for each combination
    for current_combination in combinations:

        # Work point at controlled thrust
        def func_fixed_thrust(x, args):
            rot_speed, torque, current, pwm = x

            return [
                prop_torque(rot_speed, torque, args, pitch),
                prop_thrust(rot_speed, thrust, diameter, pitch),
                motor_speed(rot_speed, Kv, pwm, voltage,
                            current, resistance),
                motor_torque(torque, current, Kv, noload_current)
            ]

        result_fixed_thrust = optimize.fsolve(
            func_fixed_thrust,
            x0=[0, 0, 0, 0],
            args=current_combination
        )

    print(f"Found {len(configurations)} possible combinations")

    flt = np.array(list(filter(combination_filter, configurations)))
    print(f"Found {len(flt)} accettable combinations")

    for it in flt:
        print(f"""
        ========================================================================
        Configuration:
            Battery: {it[2]}
                Capacity: {it[0]} mAh
                Nominal voltage: {it[1]} V
                Weight: {it[7]} g
            Motors: {it[8]}
                Kv: {it[13]} rpm/V
                Weight: {it[14]} g
                Resistance: {it[15]} Ohm
            Propeller: {it[16]}
                Diameter: {it[17]} in
                Pitch: {it[18]} in
                Weight: {it[19]} g
        Results:
            Total weight: {float(float(it[7])+4*float(it[14])+4*float(it[19])) :.2f} g
            Hovering time: {float(60*((0.001*float(it[0]))/(4*float(it[28])))) :.2f} min
            Max PWM (single motor):
                Speed: {it[22]} rpm
                Torque: {float(it[23]) :.4f} Nm
                Current (single / total): {float(it[24]) :.2f} / {float(4*float(it[24])) :.2f} A
                Thrust (single / total): {float(it[25]) :.4f} / {float(4*float(it[25])) :.4f} Kgf
                Electrical Power: {float(float(it[24])*float(it[1])) :.2f} Watt
                Mechanical Power: {float((float(it[22])*np.pi/30)*float(it[23])) :.2f} Watt
            Hovering (single motor):
                Speed: {float(it[26]) :.2f} rpm
                Torque: {float(it[27]) :.4f} Nm
                Current (single / total): {float(it[28]) :.2f} / {float(4*float(it[28])) :.2f} A
                PWM: {100*float(it[29]) :.2f} %
                Electrical Power: {float(float(it[28])*float(it[1])) :.2f} Watt
                Mechanical Power: {float((float(it[26])*np.pi/30)*float(it[27])) :.2f} Watt
        """)

    thrust = np.array(flt[:, 25], dtype=float)
    battery_weight = np.array(flt[:, 7], dtype=float)
    motor_weight = np.array(flt[:, 14], dtype=float)
    total_weight = battery_weight + 4*motor_weight


if __name__ == "__main__":
    main()
