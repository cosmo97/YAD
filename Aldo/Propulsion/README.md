
# Propulsion

This subsystem is composed by motors, propellers and ESCs.

  

# Requirements

The entire propulsion system must generate a thrust of at least 2 times the
<<<<<<< HEAD
weight of the drone, $T_{tot} > 500 grams$. So for a quadcopter it will consist of
=======
weight of the drone, $T_{tot} > 500 grams$. So for a quadcopter it will consist of
>>>>>>> 03776286d7a8662f980028017ff2e1166fac313c
4 units with a thrust of at least 125 grams each.

  

# Design

## Mathematical formulas

### Propeller specific formulas

- $T= 2 \rho A \cdot v_{air,out}^2$ Propeller thrust
- $P_p= 2 \rho A \cdot v_{air,out}^3$ Propeller power
- $v_{air,out} = \lambda \omega R$ Velocity of air  accelerated by propeller
<br>

Source: [Aerodynamics of Rotor Blades for Quadrotors](https://arxiv.org/pdf/1601.00733.pdf)

### General knowledge formulas

- $\eta_{p} = \frac{P_{p}} {P_{m}}$ Propeller efficiency
-  $\eta_{m} = \frac{P_{m}} {P_{a}}$ Motor mechanical efficiency
- $\eta_{a} = \frac{P_{a}} {P_{e}}$ Motor electrical efficiency
-  $\eta_{esc} = \frac{P_{e}} {P_{b}}$ Esc efficiency
- $P_{m} = \tau \cdot \omega$ Mechanical power
- $P_{a} = V_a \cdot I_a$ Motor armature electrical power
- $P_{e} = V_{e} \cdot I_a$ Motor electrical power
- $P_{b} = V_{b,D_c} \cdot I_a$ Battery power
- $V_{b,D_c}=V_b \cdot D_c$ Duty cycle voltage
- $K_V = \frac{\omega} {V_a}$ Motor velocity constant
- $K_T = \frac{1}{K_V} = \frac{\tau}{I_a}$ Motor torque constant
- $V_a = V_e - R_a\cdot I_a$ Armature voltage
- $A=\pi\frac{D^2}{4}$ Propeller area