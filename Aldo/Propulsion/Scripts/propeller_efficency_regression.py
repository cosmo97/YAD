import os
import numpy as np
from pandas import read_csv

AIR_DENSITY = 1.2

propellers_folder = "Aldo/Propulsion/Datasets/Propellers"


def main():
    propellers_dataset = read_csv(propellers_folder + "/Propellers.csv")

    for propeller in np.array(propellers_dataset):

        tests_file_list = os.listdir(propellers_folder+'/'+propeller[0])
        print(f"Found {len(tests_file_list)} tests for {propeller[0]}")

        for test_file in tests_file_list:
            test_dataset = read_csv(
                propellers_folder+'/'+propeller[0]+'/'+test_file)
            print(test_dataset)


if __name__ == "__main__":
    main()
