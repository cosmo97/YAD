# Propulsion
This subsystem is composed by motors, propellers and ESCs.

# Requirements
The entire propulsion system must generate a thrust of at least 2 times the
weight of the drone, T_tot > 500 grams. So for a quadcopter it will consist of
4 units with a thrust of at least 125 grams each.

# Design

## Thrust mathematical formula

$$
T_{prop}(I_a,\omega) =  V_b \cdot I_a \cdot \eta_{prop}
$$
$I_a$ can be found solving the following equation:

$$
a \cdot I_a^{\frac{3}{2}} \cdot \eta_{prop}^{\frac{3}{2}} + b \cdot I_a \cdot \eta_{prop} = 0  
$$
Where:
- $\eta_{prop} = f(\omega) = f(V_b K_V)$
- $a = - V_b^{\frac{3}{2}}$
- $b = V_b^2 \frac{D_{prop}}{4} K_V \tan (\alpha_{prop}) \sqrt{2 \rho A}$

### Mathematical steps
Given the hypothesis:
- The motor resistance can be considered negligible, so that $V_b \approx V_a$
- Each propeller blade can be approximated as a plate with a constant pitch and width.
<br>

Given the following mathematical formulas:
- $\eta_{prop} = \frac{T_{prop}} {P_e}$ Propeller efficiency
- $P_{prop} = T_{prop} v_{prop}$ Propeller power
- $v_{prop} = \frac{D_{prop}}{4}\omega \tan (\alpha_{prop})$ Propeller air velocity
- $K_V = \frac{\omega} {V_b}$ Motor velocity constant
- $P_e = V_b I_a$ Electrical power
#### Current equation proof

The current equation can be found by substituting the above formulas in the following [relationship](https://uav.jreyn.net/quadcopter-design/step-3-static-thrust-and-power):
$$
P_{prop} = \frac{{T_{prop}}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
$$
We can write:
$$
T_{prop} v_{prop} = \frac{{(P_e \eta_{prop})}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
P_e \eta_{prop} \frac{D_{prop}}{4} \omega \tan (\alpha_{prop}) = \frac{{(V_b I_a \eta_{prop})}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
V_b I_a \eta_{prop} \frac{D_{prop}}{4} V_b K_V \tan (\alpha_{prop}) = \frac{{(V_b I_a \eta_{prop})}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
V_b^2 I_a \eta_{prop} \frac{D_{prop}}{4} K_V \tan (\alpha_{prop}) \sqrt{2 \rho A} = {(V_b I_a \eta_{prop})}^{\frac{3}{2}} \\
$$

Gathering the terms and ordering the equation we obtain:
$$
a \cdot I_a^{\frac{3}{2}} \cdot \eta_{prop}^{\frac{3}{2}} + b \cdot I_a \cdot \eta_{prop} = 0
$$



