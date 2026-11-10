# Tutor guide — optional heat-recovery workshop

For tutors supporting interested students using [the notebook](lab.ipynb) and
[the executed solution](lab_solution.ipynb). This workshop is optional and unassessed.
The suggested four-hour route covers the example, balances/checks, one area/cost
comparison and reflection. The separate robustness section is further exploration.
Do not create a compulsory submission or require repeated parameter sweeps.

## Keep the two cases separate

| Quantity | Small example | Main case |
| --- | ---: | ---: |
| Hot mass flow | 1.0 kg/s | 1.2 kg/s |
| Cold mass flow | 0.5 kg/s | 1.0 kg/s |
| Hot cp | 4180 J/(kg K) | 3800 J/(kg K) |
| Cold cp | 4180 J/(kg K) | 4180 J/(kg K) |
| Hot inlet | 70 °C | 85 °C |
| Cold inlet | 15 °C | 15 °C |
| Cold target | 35 °C | 55 °C |
| Clean U | 650 W/(m² K) | 650 W/(m² K) |

U is explicitly supplied, not derived from the four stream temperatures. It
represents the combined heat-transfer resistance on a common area basis. Its
assumed constant value is not a manufacturer guarantee. Distinguish specific heat
cp in J/(kg K) from heat-capacity rate C = mass flow × cp in W/K.

## Worked example: follow the calculation order

Assume steady operation, ideal countercurrent flow, no external heat loss or phase
change, and constant properties. First calculate the cold duty:

$$
Q=C_c(T_{c,out}-T_{c,in})=0.5(4180)(35-15)=41800\ \mathrm W.
$$

Use the same duty on the hot side: Th,out = 70 − 41800/4180 = 60 °C.
Countercurrent terminal differences pair streams at the same physical end:
70 − 35 = 35 K and 60 − 15 = 45 K. Their logarithmic mean is
about 39.79 K. Area is Q/(U LMTD) ≈ **1.616 m²**.

Ask “Which quantities are calculated, and which was U supplied as?” A student
should not need to guess where 650 originated or treat it as a conversion factor.
The units W / [(W/(m² K))K] reduce to m².

At a 45 °C cold target, duty becomes 62.7 kW, hot outlet 55 °C and area
about 3.022 m². At a 75 °C target the first terminal difference is negative
(70 − 75 = −5 K), so reject the passive-exchanger target before taking a
logarithm. A calculator returning an invalid log is a physical warning, not
something to fix by taking absolute temperature differences.

## Main balance, feasibility and crossed outlets

Ch = 4560 W/K and Cc = 4180 W/K. Required duty is 167.2 kW, giving
hot outlet 48.3333 °C. Terminal differences are 30 and 33.3333 K, LMTD
about 31.64 K, and clean area **8.13059 m²**. Maximum ideal duty is
min(Ch,Cc)(85 − 15) = 292.6 kW; target effectiveness is 0.57143.

The cold outlet at 55 °C exceeds the hot outlet at 48.3333 °C because
they are at opposite ends. It does not imply heat moves from cold to hot
locally. Have students place both paired temperature differences on the diagram.
The straight segments joining terminal values are schematic, not computed profiles.

The independent effectiveness–NTU calculation recovers both outlets. NTU ≈
1.2643 and Cr ≈ 0.9167. Zero UA means unchanged outlet temperatures;
large UA approaches the ideal maximum duty. At Cr = 1, use the analytical
limit epsilon = NTU/(1 + NTU), not the general expression's 0/0 form.
Agreement verifies model implementation; it does not establish actual U, flow
distribution or acceptable pressure drop.

## Fouling: fixed duty and fixed area are different questions

Added resistance Rf changes U through 1/Uf = 1/Uclean + Rf. At Rf =
0.0006 m² K/W, Uf = 467.63 W/(m² K). With the clean-sized installed
area held fixed, duty falls to 142.159 kW and cold outlet to 49.0093 °C.
It is wrong to keep target duty and both target outlets fixed while retaining
the same area after U decreases.

To retain the target duty and terminal temperatures, area must instead rise
by factor Uclean/Uf = 1.39 to **11.30152 m²**. The larger unit gives
about 60.80 °C when clean at those flows, requiring control if 55 °C is
an exact target. Discuss bypass or duty control rather than claiming extra
area always produces an unqualified improvement.

## Same-service comparison: heat recovery plus trim heating

The boundary now includes recovery and an ideal electric trim heater. All options
must deliver 1 kg/s at 55 °C. Heater power is the positive deficit from
167.2 kW; excess recovery earns no export credit. Given installed exchanger cost
is €4000 + €700A, electricity €0.10/kWh, time 4000 h/year, horizon ten
years, with no discounting, heater capital or exchanger pumping cost.

| Area | Recovered heat at default Rf | Trim heating | Ten-year modelled total |
| ---: | ---: | ---: | ---: |
| 8.13059 m² | 142.159 kW | 25.041 kW | €109856 |
| 11.30152 m² | 167.2 kW | Essentially zero | €11911 |
| 14 m² | 183.136 kW available | Zero; control excess | €13800 |

The small unit's trim electricity is 25.041 × 4000 ≈ 100164 kWh/year.
Its low purchase cost does not make it the cheapest way to supply equal service.
The middle area wins at default fouling. At zero additional resistance the
smallest wins; at Rf = 0.001 the largest supplied candidate wins. This is
a discrete, conditional comparison, not optimization over every possible area.

Microscopic numerical trim power near the target is rounding, not a practical
heater specification. With the exact design areas, equality should hold within
floating-point tolerance. Students must not assign negative trim demand or sell
excess heat at an unstated price.

## Operating envelope and tutor prompts

At the default chosen area and fouling condition, the tested cold-flow range
0.5–1.0 kg/s reaches at least 55 °C. Lower flow gives hotter water but
less delivered water; it cannot replace a 1 kg/s requirement without changing
the service. The 0.5 kg/s point gives about 74.09 °C and 123.50 kW;
1.8 kg/s gives 40.24 °C and 189.91 kW. More recovered heat need not be
at a sufficiently useful temperature.

Ask “Are you holding duty, area or temperature fixed?” before helping with
algebra. Ask “What extra service completes the smaller exchanger's duty?” before
comparing costs. Ask “Is this heat duty or electrical input?” The trim heater
uses efficiency one by explicit assumption; an exchanger's heat duty is not its
electricity use.

Real design still requires fluid properties, flow-dependent coefficients, geometry,
pressure losses, pumping power, fouling/cleaning data and actual costs. For the
optional heat-loss question, measure all four temperatures and both mass flows:
hot enthalpy loss minus cold gain estimates external loss. A low cold outlet
alone cannot distinguish fouling from heat lost to the room.
