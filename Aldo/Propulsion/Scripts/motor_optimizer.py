import numpy as np
import pandas as pd
from scipy import optimize
from matplotlib import pyplot as plt

BATTERIES_DATASET = "Aldo/Propulsion/Datasets/Batteries/Batteries.csv"
MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"
PROPELLERS_DATASET = "Aldo/Propulsion/Datasets/Propellers/Propellers.csv"


MIN_THRUST = 0.500      # kgf. 2 times of the weight for control authority
HOVER_THRUST = 0.250    # kgf
MAX_WEIGHT = 250        # g. Maybe less for frame/board
MIN_HOVERING_TIME = 8  # min
MIN_ALLOWED_PWM = 0.01
MAX_ALLOWED_PWM = 1.00

# Todo: compute or add resistance for each motor
DEFAULT_RESISTANCE = 0.05  # Ohm


def motor_speed(rot_speed, Kv, pwm, voltage, current, resistance=DEFAULT_RESISTANCE):
    return rot_speed - Kv*(pwm*voltage - resistance*current)


def motor_torque(torque, current, Kv):
    return torque - current/(Kv*np.pi/30)


def prop_torque(rot_speed, torque, diameter, pitch):
    return torque - 5.75e-14*(rot_speed**1.85e+00) * \
        (diameter**3.44e+00)*(pitch**2.59e+00)


def prop_thrust(rot_speed, thrust, diameter, pitch):
    return thrust - 4.33e-12*(rot_speed**1.88e+00) * \
        (diameter**2.83e+00)*(pitch**1.60e+00)


def combination_filter(conf):
    # Configurations filtering
    return \
        4*float(conf[25]) > MIN_THRUST \
        and (float(conf[7])+4*float(conf[14])+4*float(conf[19])) < MAX_WEIGHT \
        and float(conf[29]) < MAX_ALLOWED_PWM \
        and float(conf[29]) > MIN_ALLOWED_PWM \
        and 60*((0.001*float(conf[0]))/(4*float(conf[28]))) > MIN_HOVERING_TIME


def main():
    # Retrieve propellers and motors parameters
    batteries_dataset = pd.read_csv(BATTERIES_DATASET)
    motors_dataset = pd.read_csv(MOTORS_DATASET)
    propellers_dataset = pd.read_csv(PROPELLERS_DATASET)

    # List of combinations
    configurations = []

    # Cycle to all possible configurations
    for battery in np.array(batteries_dataset):
        for motor in np.array(motors_dataset):
            for propeller in np.array(propellers_dataset):

                # Work point at 100% PWM
                def func_max_pwm(x, args):
                    rot_speed, torque, current, thrust = x
                    diameter, pitch, Kv, voltage, pwm = args

                    return [
                        prop_torque(rot_speed, torque, diameter, pitch),
                        prop_thrust(rot_speed, thrust, diameter, pitch),
                        motor_speed(rot_speed, Kv, pwm, voltage, current),
                        motor_torque(torque, current, Kv)
                    ]

                res_max_pwm = optimize.fsolve(
                    func_max_pwm,
                    x0=[0, 0, 0, 0],
                    args=[propeller[1], propeller[2],
                          motor[5], battery[1], MAX_ALLOWED_PWM]
                )

                # Work point at controlled thrust
                def func_fixed_thrust(x, args):
                    rot_speed, torque, current, pwm = x
                    diameter, pitch, Kv, voltage, thrust = args

                    return [
                        prop_torque(rot_speed, torque, diameter, pitch),
                        prop_thrust(rot_speed, thrust, diameter, pitch),
                        motor_speed(rot_speed, Kv, pwm, voltage, current),
                        motor_torque(torque, current, Kv)
                    ]

                res_fixed_thrust = optimize.fsolve(
                    func_fixed_thrust,
                    x0=[0, 0, 0, 0],
                    args=[propeller[1], propeller[2],
                          motor[5], battery[1], HOVER_THRUST]
                )

                # Save configurations and results
                configurations.append([
                    *battery, *motor, *propeller,
                    *res_max_pwm, *res_fixed_thrust
                ])

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
                PWM: {float(it[29]) :.2f} %
                Electrical Power: {float(float(it[28])*float(it[1])) :.2f} Watt
                Mechanical Power: {float((float(it[26])*np.pi/30)*float(it[27])) :.2f} Watt
        """)

    thrust = np.array(flt[:, 25], dtype=float)
    battery_weight = np.array(flt[:, 7], dtype=float)
    motor_weight = np.array(flt[:, 14], dtype=float)
    total_weight = battery_weight + 4*motor_weight


if __name__ == "__main__":
    main()
