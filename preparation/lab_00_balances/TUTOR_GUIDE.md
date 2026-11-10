# Tutor guide — Lab 00: first mass and heat balances

For tutors; contains complete answers. Use beside [the student notebook](lab.ipynb)
and [the executed solution](lab_solution.ipynb). This is preparation, not another
assessed main lab. Core time is about three hours, with practice up to four.
No Python programming or differential-equation solving should be required.

## Teaching purpose and intervention pattern

The goal is to translate a physical description into a balance before using a
calculator. A student who copies a correct number but cannot identify the boundary
has not yet achieved that goal. Ask for these five items in order:

1. A boundary and named streams.
2. The conserved quantity and the time basis.
3. A statement about accumulation and reaction.
4. A symbolic equation, followed by numerical substitution with units.
5. A conservation check and a physical interpretation.

For a stuck group, start with “What crosses your boundary?” Then ask “What can
change inside it?” Only then point to the equation. Keep mass in kg, flow in
kg/time and fractions in kg/kg. The provided residuals check the chosen equations;
they cannot establish that a real apparatus satisfies the assumptions.

## Part 1: the balance recipe

For a nonreacting total-mass balance, accumulation rate equals input minus
output. At steady state it is zero. Constant inlet flow alone does not imply
steady state: the outflow and inventory must be considered too. Components need
production/consumption terms if reaction occurs, but these examples have none.

Use the dilution prediction to expose a common misconception: adding water
reduces salt **fraction**, but does not remove salt from the process. Distinguish
salt stored in a vessel from salt passing through it per hour.

## Part 2: mixing and dilution

The boundary encloses the mixer, with two inlets and one outlet. There is no
accumulation, reaction or material loss. Let A, B and C be solution mass flows
in kg/h, and w the salt mass fraction. Then:

$$
C=A+B,\qquad Cw_C=Aw_A+Bw_B.
$$

For A = 80 kg/h, wA = 0.10 and B = 20 kg/h pure water:

- C = 100 kg/h.
- Salt input is 80 × 0.10 = 8 kg/h; water brings no salt.
- wC = 8/100 = 0.08 = 8 wt%.
- Product water is 92 kg/h, equal to 72 kg/h from A plus 20 kg/h from B.

The two component balances sum to the total balance, so all three are not
independent equations. The water calculation is useful as a check, not as an
extra independent condition needed to solve the same unknowns.

With B = 40 kg/h, C = 120 kg/h and concentration is 8/120 = 6.667 wt%.
Salt flow remains 8 kg/h. With a 5 wt% target, C = 8/0.05 = 160 kg/h,
so the **total** pure-water feed must be 80 kg/h. This is 60 kg/h extra
relative to the original 20 kg/h, not 80 kg/h extra.

If a student obtains a concentration above 10 wt%, ask which inlet could have
supplied that enrichment. For positive flows and no separation/reaction, the
outlet fraction is a mass-flow-weighted average between the inlet fractions.
If the student uses 10 rather than 0.10, ask for the meaning of “per hundred”.

## Part 3: splitting is not separation

Both examples use the original mixer product: 100 kg/h at 8 wt%, not whatever
edited dilution setting a student last ran. State this reset explicitly.

A splitter sends 30 and 70 kg/h to its branches. Both remain at 8 wt%; salt
flows are 2.4 and 5.6 kg/h. It redirects a homogeneous mixture without sorting
its components. Multiplying concentration by the split fraction is incorrect.

For the evaporator, the boundary includes the vessel but not the heat source.
Salt is nonvolatile; vapour is pure water; no droplets, crystals or salt losses
leave by other routes. There are two unknown outlet flows:

$$
F=P+V,\qquad Fw_F=Pw_P.
$$

At F = 100 kg/h, wF = 0.08 and wP = 0.20, P = 40 kg/h and V =
60 kg/h. Salt check: 8 = 40 × 0.20. Water check: 92 = 32 + 60 kg/h.
The total balance alone cannot determine both P and V.

At wP = 0.10, P = 80 kg/h and V = 20 kg/h. At wP = 0.08, V = 0.
A requested wP = 0.05 would imply negative evaporation, signalling that this
operation cannot meet that target by pure-water removal. Do not “fix” this by
taking the absolute value of V.

No evaporation energy has been determined. Inlet/outlet phase conditions,
temperatures and latent/sensible enthalpy data are missing. This is an important
boundary between what conservation can determine and what additional property
information is needed.

## Part 4: heating and adiabatic temperature mixing

For the heater, steady mass flow is unchanged. Neglect work, kinetic/potential
changes and external loss. With constant cp and no phase change:

$$
\dot Q=\dot m(h_{out}-h_{in})=\dot m c_p(T_{out}-T_{in}).
$$

At 2 kg/s, cp = 4180 J/(kg K), and 20 to 50 °C, duty is 250800 W =
250.8 kW. A temperature difference of 30 °C equals 30 K; do not add 273.15
to the difference. Units reduce to J/s. Two hours requires 501.6 kWh of
**heat**. It is not automatically electrical energy; conversion efficiency
has not been specified. Doubling flow doubles duty. Changing the outlet to
40 °C at the original flow gives 167.2 kW.

The separate adiabatic mixer has 0.5 kg/s at 80 °C and 1.5 kg/s at 20 °C.
Use the same enthalpy reference and cp for both streams:

$$
(\dot m_A+\dot m_B)c_p(T_C-T_{ref})
=\dot m_Ac_p(T_A-T_{ref})+\dot m_Bc_p(T_B-T_{ref}).
$$

Reference terms and cp cancel, giving TC = (0.5 × 80 + 1.5 × 20)/2 =
35 °C. The unweighted 50 °C average assumes equal mass flows, which are not
present. Ask “Which stream carries more heat capacity per second?” A result
outside 20–80 °C violates this simplified adiabatic, same-liquid model.

## Part 5: accumulation and the end of model validity

Net flow is 2 − 1.5 = 0.5 kg/s, so M = 50 + 0.5t, with t in seconds.
At 10 min = 600 s, M = 350 kg and volume is 0.350 m³ using the separately
stated approximate density 1000 kg/m³. The tank fills at 30 kg/min.

Capacity 400 kg is reached at (400 − 50)/0.5 = 700 s = 11.667 min.
The calculation ends there: overflow or another physical/control change must
then enter the model. A straight-line continuation beyond capacity is not a
prediction of valid tank operation.

At outflow 2 kg/s, inventory stays 50 kg. At 2.5 kg/s it empties in 100 s;
a ten-minute continuation would be invalid. Equal total flows establish constant
mass inventory, not necessarily constant composition or temperature.

## Review, optional practice and acceptable explanations

For the optional 6 wt% dilution target, total water feed is 53.333 kg/h;
extra water relative to the original case is 33.333 kg/h. The optional
1 kg/s water-heating example, 15 to 55 °C, requires 167.2 kW and 668.8 kWh
over four hours. A mixer-plus-evaporator overall boundary gives 80 + 20 =
40 + 60 kg/h; the internal 100 kg/h stream cancels when unit balances are summed.

A good final explanation distinguishes inventories from rates, fractions from
component flows, and power from energy. It explains why an extra component
balance is needed and identifies the assumptions that permit a heat-capacity
formula. Do not require polished programming or turn the optional practice into
another compulsory design exercise.
