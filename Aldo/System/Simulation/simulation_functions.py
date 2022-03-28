import numpy as np


class simulator():
    def __init__(self, quadcopter_conf_, sim_conf_):
        # Extracting quadcopter and simulation configurations passed as dictionaries
        self.extract_quadcopter_conf(quadcopter_conf_)
        self.extract_sim_conf(sim_conf_)

    def extract_quadcopter_conf(self, quadcopter_conf_):
        self.D_prop_ = quadcopter_conf_[
            "propulsion"]["propeller"]["diameter"]  # Propeller diameter
        self.V_battery_ = quadcopter_conf_[
            "battery"]["voltage"]  # Battery max voltage
        self.eff_prop_ = quadcopter_conf_[
            "propulsion"]["propeller"]["efficiency"]  # Propeller efficiency
        self.eff_motor_ = quadcopter_conf_[
            "propulsion"]["motor"]["efficiency"]  # Motor efficiency
        self.R_motor_ = quadcopter_conf_[
            "propulsion"]["motor"]["resistance"]  # Motor resistance

    def extract_sim_conf(self, sim_conf_):
        # Gravity acceleration constant
        self.g_ = sim_conf_["physics"]["gravity"]
        self.air_density_ = sim_conf_["physics"]["air_density"]  # Air density

    def static_thrust_theoretical_estimate(self):
        # Problem: how to compute I_motor (the current flowing through the motor)?
        # It depends on the RPM that are a consequence of the working point given by
        # the intersection btw the load given by the aerodynamic friction

        ################### JUST TO SHOW A POSSIBLE IMPLEMENTATION ##################
        self.I_motor_ = 0  # Motor current
        self.V_motor_ = self.V_battery_ - self.I_motor_*self.R_motor_  # Motor voltage
        #############################################################################

        self.P_motor_ = self.V_motor_*self.I_motor_  # Motor power
        self.P_lift_ = self.P_motor_*self.eff_prop_  # Propeller lift
        self.T_static_ = ((self.P_lift_**2)*(np.pi) *
                          ((self.D_prop_**2)/2)*(self.air_density_))**(3/2)  # Static thrust in Newton
        self.T_static_mass_ = self.T_static_/self.g_  # Static thrust in Kg

    def static_thrust_empirical_estimate(self):
        pass
