import numpy as np
import pandas as pd
from scipy import optimize
from matplotlib import pyplot as plt

PROPELLERS_DATASET = "Aldo/Propulsion/Datasets/Propellers/Propellers.csv"
MOTORS_DATASET = "Aldo/Propulsion/Datasets/Motors/Motors.csv"

# For a 250 grams quadcopter you need a thrust of 0.25/4=62.5 Kgf
MIN_THRUST = 0.125   # 2 times min for control authority
MAX_THRUST = 0.3125  # 5 times max to discard uncontrollable motors


def prop_torque(x, args):
    """_summary_ TODO

    Args:
        x (list): TODO
        args (list): TODO

    Returns:
        _type_: TODO
    """
    rot_speed_ = x[0]
    torque_ = x[1]
    diameter_ = args[0]
    pitch_ = args[1]

    ret = torque_ - 5.89e-14*(rot_speed_**1.96e+00) * \
        (diameter_**3.01e+00)*(pitch_**2.38e+00)

    return ret


def prop_thrust(x, args):
    """TODO

    Args:
        x (_type_): TODO
        args (_type_): TODO

    Returns:
        _type_: TODO
    """
    rot_speed_ = x[0]
    thrust_ = x[2]
    diameter_ = args[0]
    pitch_ = args[1]

    ret = thrust_ - 1.76e-11*(rot_speed_**1.81e+00) * \
        (diameter_**2.49e+00)*(pitch_**1.51e+00)

    return ret


def motor_speed(x, args):
    """_summary_

    Args:
        x (_type_): TODO
        args (_type_): TODO

    Returns:
        _type_: TODO
    """
    rot_speed_ = x[0]
    Kv = args[2]

    ret = rot_speed_ - Kv*12

    return ret


def main():
    """_summary_

    Returns:
        _type_: TODO
    """
    # Retrieve propellers and motors parameters
    propellers_dataset = pd.read_csv(PROPELLERS_DATASET)
    motors_dataset = pd.read_csv(MOTORS_DATASET)

    # List of valid solutions
    solutions = []

    # Cycle to all propeller-motor possible configurations
    for propeller in np.array(propellers_dataset):
        for motor in np.array(motors_dataset):
            print(f"Solving {propeller[0]} - {motor[0]}")

            # Calculate the work point between propeller and motor curves
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

            # Solution validity checks
            if(res[2] > MIN_THRUST and res[2] < MAX_THRUST):
                solutions.append([
                    propeller[0]+"-"+motor[0], propeller[3]+motor[6], res[2]
                ])

                print(f"""
                Speed  [rpm]: {res[0]}
                Torque  [Nm]: {res[1]}
                Thrust [Kgf]: {res[2]}
                """)
            else:
                print(f"""
                No suitable solutions
                """)

    # Export only valid solutions
    solutions = np.array(solutions)
    weight = np.array(solutions[:, 1], dtype=float)
    thrust = np.array(solutions[:, 2], dtype=float)

    plt.scatter(weight, thrust)
    for i, sol in enumerate(solutions):
        plt.annotate(sol[0], (weight[i], thrust[i]))

    plt.show()


if __name__ == "__main__":
    main()
