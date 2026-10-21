"""Explicit supplied main-case data, separate from the smaller worked examples."""
MAIN_INPUTS = {
'lab_01_flow': '''### Main-case input reference

| Input | Value / units | Role |
| --- | --- | --- |
| Gravity | 9.81 m/s² | Constant used in head and power conversions |
| Length / static rise | 120 / 12 m | Given base geometry |
| Base internal diameter | 0.065 m | Reference case; design alternatives 0.050, 0.065, 0.080 m |
| Density / dynamic viscosity | 998 kg/m³ / 0.001 Pa s | Constant assumed water properties |
| Roughness / total fitting K | 0.000045 m / 8 dimensionless | Supplied pipe-loss inputs |
| Fixed delivery | 0.003 m³/s = 3 L/s | Required design service, not uncontrolled flow |
| Operating time | 4000 h/year | Assumed duty duration |
| Motor / drive efficiency | 0.90 / 0.96, dimensionless | Assumed electrical conversion efficiencies |

Curve coefficients and operating limits are stated above; cost and changed-duty
inputs are supplied in their own sections. All are teaching assumptions, not
manufacturer measurements. Head, speed, efficiency, power and energy are calculated.
''',
'lab_02_heat': '''### Main-case input reference

These supplied synthetic inputs define the main case, not the smaller example.

| Input | Value / units | Role |
| --- | --- | --- |
| Hot / cold mass flow | 1.2 / 1.0 kg/s | Given process flow / water delivery |
| Hot specific heat capacity | 3800 J/(kg K) | Constant assumed process-fluid property |
| Cold specific heat capacity | 4180 J/(kg K) | Constant assumed water property |
| Hot / cold inlet temperature | 85 / 15 °C | Given inlet conditions |
| Cold outlet temperature | 55 °C | Required target |
| Clean overall coefficient Uclean | 650 W/(m² K) | Assumed clean performance on the stated heat-transfer area basis |
| LMTD correction factor | 1, dimensionless | Ideal countercurrent geometry |

Capacity rates Ch and Cc (W/K), duty (W), hot outlet (°C), LMTD (K) and
area (m²) are calculated. Specific heat capacity cp differs from capacity rate
C = mass flow × cp. Fouling, cost, area alternatives and operating hours are
separate supplied inputs in later sections. No property lookup is implied.
''',
'lab_03_distillation': '''### Main-case input reference

Use a hypothetical binary mixture. Compositions are mole fractions of the more
volatile component, not mass fractions. All properties are teaching assumptions.

| Input | Value / units | Role |
| --- | --- | --- |
| Feed F | 100 kmol/h | Given base feed rate |
| Feed zF | 0.45 mol/mol | Given composition |
| Distillate xD / bottoms xB | 0.95 / 0.05 mol/mol | Product targets |
| Relative volatility alpha | 2.4, dimensionless | Assumed constant equilibrium parameter |
| Feed condition q | 1, dimensionless | Saturated-liquid assumption |
| Baseline reflux R = L/D | 2.5, dimensionless | Initial chosen operating condition |

Product flows, minimum reflux, stages and vapour circulation are calculated.
Tray efficiency, spacing, capacity/height limits, latent heat and prices are
separately supplied in their sections. The earlier example has different targets.
''',
'lab_04_absorption': '''### Main-case input reference

Use the hypothetical isothermal, nonreacting system. Flows are solute-free molar
flows; X and Y are mole ratios, not mole fractions.

| Input | Value / units | Role |
| --- | --- | --- |
| Gs | 100 kmol carrier/h | Given gas-carrier flow |
| Yin | 0.030 mol solute/mol carrier | Given inlet ratio |
| Yout | 0.003 mol solute/mol carrier | Required outlet ratio |
| Xin | 0 mol solute/mol solvent | Fresh solvent assumption |
| Equilibrium slope m | 1.5, dimensionless | Assumed Y* = mX model parameter |
| Baseline Ls/Lmin | 1.5, dimensionless | Initial chosen solvent policy |

Minimum and selected solvent rates, rich-solvent ratio, removal and contact count
are calculated. HETP, tray efficiency, dry-bed properties, adverse equilibrium,
height limits and costs are separate supplied assumptions in later sections.
The smaller example has different solvent flow and gas-outlet target.
'''
}
