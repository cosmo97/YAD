import numpy as np
import pandas as pd
from scipy import optimize
from matplotlib import pyplot as plt

PROPELLERS_DATASET = "Aldo/Propulsion/Datasets/Propellers/Propellers.csv"
MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"

MIN_THRUST = 0.125
MAX_THRUST = 0.3125


def prop_torque(x, args):
    rot_speed_ = x[0]
    torque_ = x[1]
    diameter_ = args[0]
    pitch_ = args[1]

    ret = torque_ - 5.89e-14*(rot_speed_**1.96e+00) * \
        (diameter_**3.01e+00)*(pitch_**2.38e+00)

    return ret


def prop_thrust(x, args):
    rot_speed_ = x[0]
    thrust_ = x[2]
    diameter_ = args[0]
    pitch_ = args[1]

    ret = thrust_ - 1.76e-11*(rot_speed_**1.81e+00) * \
        (diameter_**2.49e+00)*(pitch_**1.51e+00)

    return ret


def motor_speed(x, args):
    rot_speed_ = x[0]
    Kv = args[2]

    ret = rot_speed_ - Kv*12

    return ret


def main():
    # Retrieve propellers parameters
    propellers_dataset = pd.read_csv(PROPELLERS_DATASET)
    motors_dataset = pd.read_csv(MOTORS_DATASET)

    solutions = []
    for propeller in np.array(propellers_dataset):
        for motor in np.array(motors_dataset):
            print(f"Solving {propeller[0]} - {motor[0]}")

            def func(x, args):
                return [
                    prop_torque(x, args),
                    prop_thrust(x, args),
                    motor_speed(x, args)
                ]

            res = optimize.fsolve(
                func,
                x0=[0, 0, 0],
                args=[propeller[1], propeller[2], motor[5]]
            )

            print(f"""
            Speed  [rpm]:  {res[0]}
            Torque  [Nm]:  {res[1]}
            Thrust [Kgf]: {res[2]}
            """)
            solutions.append([res[0], res[1], res[2]])

    solutions = np.array(solutions)
    plt.scatter(solutions[:, 0], solutions[:, 1])
    plt.show()


if __name__ == "__main__":
    main()
