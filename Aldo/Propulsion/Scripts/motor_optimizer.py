import numpy as np
import pandas as pd
from scipy import optimize
from matplotlib import pyplot as plt

BATTERIES_DATASET = "Aldo/Propulsion/Datasets/Batteries/Batteries.csv"
MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"
PROPELLERS_DATASET = "Aldo/Propulsion/Datasets/Propellers/Propellers_ideal.csv"


MIN_THRUST = 0.500  # kgf. 2 times of the weight for control authority
MAX_WEIGHT = 250  # g. Maybe less for frame/board


def motor_speed(x, args):
    rot_speed = x[0]
    Kv = args[2]
    voltage = args[3]
    resistance = args[4]

    return rot_speed - Kv*voltage


def motor_torque(x, args):
    torque = x[1]
    I = x[3]
    Kv = args[2]

    return torque - I/Kv


def prop_torque(x, args):
    rot_speed = x[0]
    torque = x[1]
    diameter = args[0]
    pitch = args[1]

    return torque - 5.75e-14*(rot_speed**1.85e+00) * \
        (diameter**3.44e+00)*(pitch**2.59e+00)


def prop_thrust(x, args):
    rot_speed = x[0]
    thrust = x[2]
    diameter = args[0]
    pitch = args[1]

    return thrust - 4.33e-12*(rot_speed**1.88e+00) * \
        (diameter**2.83e+00)*(pitch**1.60e+00)


def main():
    # Retrieve propellers and motors parameters
    batteries_dataset = pd.read_csv(BATTERIES_DATASET)
    motors_dataset = pd.read_csv(MOTORS_DATASET)
    propellers_dataset = pd.read_csv(PROPELLERS_DATASET)

    # List of valid solutions
    solutions = []

    # Cycle to all propeller-motor possible configurations
    for battery in np.array(batteries_dataset):
        for motor in np.array(motors_dataset):

            # Check if motor is rated for that voltage
            if battery[1] != motor[7]:
                break

            for propeller in np.array(propellers_dataset):
                # Calculate the work point between propeller and motor curves
                def func(x, args):
                    return [
                        prop_torque(x, args),
                        prop_thrust(x, args),
                        motor_speed(x, args),
                        motor_torque(x, args)
                    ]

                res = optimize.fsolve(
                    func,
                    x0=[0, 0, 0, 0],
                    args=[propeller[1], propeller[2],
                          motor[5], motor[7], motor[8]]
                )

                # Solution validity checks
                solutions.append([
                    *battery, *motor, *propeller, *res
                ])

    # Filter invalid solutions
    print(f"Found {len(solutions)} possible combinations")
    # print(solutions)

    def combination_filter(solution):
        return \
            4*solution[25] > MIN_THRUST \
            and (solution[7]+4*solution[14]) < MAX_WEIGHT \
            # and (0.001*solution[0]/solution[26]) > 15/60

    filtered_solutions = np.array(list(filter(combination_filter, solutions)))
    print(f"Found {len(filtered_solutions)} accettable combinations")
    print(filtered_solutions)

    thrust = np.array(filtered_solutions[:, 25], dtype=float)
    battery_weight = np.array(filtered_solutions[:, 7], dtype=float)
    motor_weight = np.array(filtered_solutions[:, 14], dtype=float)
    total_weight = battery_weight+4*motor_weight

    plt.scatter(
        total_weight,
        thrust
    )
    plt.show()


if __name__ == "__main__":
    main()
