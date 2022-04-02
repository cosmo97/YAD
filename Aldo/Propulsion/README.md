# Propulsion
This subsystem is composed by motors, propellers and ESCs.

# Requirements
The entire propulsion system must generate a thrust of at least 2 times the
weight of the drone, T_tot > 500 grams. So for a quadcopter it will consist of
4 units with a thrust of at least 125 grams each.

# Design

## Thrust mathematical formula

$$
T_{prop}(I_a,\eta_{T \tau}) = \frac{1}{K_V}I_a\cdot \eta_{T \tau}
$$
$I_a$ and $\eta_{T \tau}$ can be found solving the following system of equations:

$$
\begin{cases}
\eta_{T \tau} = f(\omega) & \text{(I)} \\
\eta_{prop} = f(\omega) & \text{(II)} \\
a I_a^2 \eta_{prop} + b I_a^{\frac{3}{2}} \eta_{T \tau}^{\frac{3}{2}} +c I_a \eta_{prop} = 0 & \text{(III)} \\
\omega =  V_b K_V - R_a I_a K_V & \text{(IV)}
\end{cases}
$$
Where:
$$
a = -R_a \sqrt{2\rho A} \\
b = - \left( \frac{1}{K_V} \right) ^ {\frac{3}{2}} \\
c = V_b  \sqrt{2\rho A}
$$
These reduce to only **two equations** after empirically determining $\eta_{T \tau}(\omega)$ and $\eta_{prop}(\omega)$, and substituting them in $(III)$.

### Mathematical steps
Given the following mathematical formula:
$$
\eta_{T \tau} = \frac{T_{prop}} {\tau_{mot}} \\
\eta_{prop} = \frac{P_{prop}} {P_e} \\
K_V = \frac{\omega} {V_a} \\
K_{\tau} = \frac{1} {K_V} = \frac{\tau_{mot}} {I_a} \\
P_e = V_a\cdot I_a \\
V_a = V_b - R_a I_a
$$

#### Equation III

The equation III can be found by starting from the following [relationship](https://uav.jreyn.net/quadcopter-design/step-3-static-thrust-and-power):
$$
P_{prop} = \frac{{T_{prop}}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
$$
We can write:
$$
P_e \eta_{prop} = \frac{{(\tau_{mot} \eta_{T \tau)}}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
V_a I_a \eta_{prop} = \frac{{(K_{\tau} I_a \eta_{T \tau)}}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
(V_b - R_a I_a) I_a \eta_{prop} = \frac{{(\frac{1}{K_V} I_a \eta_{T \tau)}}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
V_b I_a - R_a I_a^2 \eta_{prop} = \frac{{(\frac{1}{K_V})^{\frac{3}{2}} I_a ^{\frac{3}{2}} \eta_{T \tau}^{\frac{3}{2}}}} {\sqrt{2 \rho A}} \\
V_b I_a{\sqrt{2 \rho A}} - R_a I_a^2 \eta_{prop}{\sqrt{2 \rho A}} - {\left(\frac{1}{K_V}\right)^{\frac{3}{2}} I_a ^{\frac{3}{2}} \eta_{T \tau}^{\frac{3}{2}}} = 0
$$
Gathering the terms and ordering the equation we obtain:
$$
a I_a^2 \eta_{prop} + b I_a^{\frac{3}{2}} \eta_{T \tau}^{\frac{3}{2}} +c I_a \eta_{prop} = 0
$$

#### Equation IV

The equation IV can be found by starting from the following relationship:
$$
\omega = K_V V_a \\
\omega = K_V (V_b - R_a I_a) \\
\omega = K_V V_b - K_V R_a I_a
$$


