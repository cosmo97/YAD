\# Propulsion This subsystem is composed by motors, propellers and ESCs.

\# Requirements The entire propulsion system must generate a thrust of
at least 2 times the weight of the drone, T_tot \> 500 grams. So for a
quadcopter it will consist of 4 units with a thrust of at least 125
grams each.

\# Design

\## Thrust mathematical formula

*T*<sub>*p**r**o**p*</sub>(*I*<sub>*a*</sub>,*ω*) = *V*<sub>*b*</sub> ⋅ *I*<sub>*a*</sub> ⋅ *η*<sub>*p**r**o**p*</sub>
*I*<sub>*a*</sub> can be found solving the following equation:

$$a \\cdot I_a^{\\frac{3}{2}} \\cdot \\eta\_{prop}^{\\frac{3}{2}} + b \\cdot I_a \\cdot \\eta\_{prop} = 0$$
Where: -
*η*<sub>*p**r**o**p*</sub> = *f*(*ω*) = *f*(*V*<sub>*b*</sub>*K*<sub>*V*</sub>) -
$a = - V_b^{\\frac{3}{2}}$ -
$b = V_b^2 \\frac{D\_{prop}}{4} K_V \\tan (\\alpha\_{prop}) \\sqrt{2 \\rho A}$

\### Mathematical steps Given the hypothesis: - The motor resistance can
be considered negligible, so that
*V*<sub>*b*</sub> ≈ *V*<sub>*a*</sub> - Each propeller blade can be
approximated as a plate with a constant pitch and width. \<br\>

Given the following mathematical formulas: -
$\\eta\_{prop} = \\frac{T\_{prop}} {P_e}$ Propeller efficiency -
*P*<sub>*p**r**o**p*</sub> = *T*<sub>*p**r**o**p*</sub>*v*<sub>*p**r**o**p*</sub>
Propeller power -
$v\_{prop} = \\frac{D\_{prop}}{4}\\omega \\tan (\\alpha\_{prop})$
Propeller air velocity - $K_V = \\frac{\\omega} {V_b}$ Motor velocity
constant - *P*<sub>*e*</sub> = *V*<sub>*b*</sub>*I*<sub>*a*</sub>
Electrical power \#### Current equation proof

The current equation can be found by substituting the above formulas in
the following
\[relationship\](https://uav.jreyn.net/quadcopter-design/step-3-static-thrust-and-power):
$$P\_{prop} = \\frac{{T\_{prop}}^{\\frac{3}{2}}} {\\sqrt{2 \\rho A}} \\\\
$$
We can write:
$$T\_{prop} v\_{prop} = \\frac{{(P_e \\eta\_{prop})}^{\\frac{3}{2}}} {\\sqrt{2 \\rho A}} \\\\
P_e \\eta\_{prop} \\frac{D\_{prop}}{4} \\omega \\tan (\\alpha\_{prop}) = \\frac{{(V_b I_a \\eta\_{prop})}^{\\frac{3}{2}}} {\\sqrt{2 \\rho A}} \\\\
V_b I_a \\eta\_{prop} \\frac{D\_{prop}}{4} V_b K_V \\tan (\\alpha\_{prop}) = \\frac{{(V_b I_a \\eta\_{prop})}^{\\frac{3}{2}}} {\\sqrt{2 \\rho A}} \\\\
V_b^2 I_a \\eta\_{prop} \\frac{D\_{prop}}{4} K_V \\tan (\\alpha\_{prop}) \\sqrt{2 \\rho A} = {(V_b I_a \\eta\_{prop})}^{\\frac{3}{2}} \\\\
$$

Gathering the terms and ordering the equation we obtain:
$$a \\cdot I_a^{\\frac{3}{2}} \\cdot \\eta\_{prop}^{\\frac{3}{2}} + b \\cdot I_a \\cdot \\eta\_{prop} = 0$$
