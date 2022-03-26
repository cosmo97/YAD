import simulation_utils
from simulation_functions import simulator

QUADCOPTER_CONF_YAML_PATH = "Aldo/System/Simulation/quadcopter_configuration.yaml"
SIM_CONF_YAML_PATH = "Aldo/System/Simulation/simulation_configuration.yaml"


def main():
    quadcopter_conf_ = simulation_utils.get_conf_from_yaml(
        QUADCOPTER_CONF_YAML_PATH)
    sim_conf_ = simulation_utils.get_conf_from_yaml(
        SIM_CONF_YAML_PATH)
    system_simulator_ = simulator(quadcopter_conf_, sim_conf_)


if __name__ == "__main__":
    main()
