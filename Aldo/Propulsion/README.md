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
\omega =  V_b K_V - R_a I_a K_V & \text{(VI)}
\end{cases}
$$
Where:
$$
\begin{align*}
a &= -R_a \sqrt{2\rho A} \\
b &= - \Bigl( \frac{1}{K_V} \Bigr) ^ {\frac{3}{2}} \\
c &= V_b  \sqrt{2\rho A}
\end{align*}
$$
These reduce to only **two equations** after empirically determining $\eta_{T \tau}(\omega)$ and $\eta_{prop}(\omega)$, and substituting them in $(III)$.

### Mathematical steps

Relevant formula:
$$
P_{prop} = \frac{{T_{prop}}^{\frac{3}{2}}} {\sqrt{2 \rho A}} \\
\eta_{T \tau} = \frac{T_{prop}} {\tau_{mot}} \\
\eta_{prop} = \frac{P_{prop}} {P_e} \\
K_V = \frac{\omega} {V_a} \\
K_T = \frac{1} {K_V} = \frac{\tau_{mot}} {I_a}
$$