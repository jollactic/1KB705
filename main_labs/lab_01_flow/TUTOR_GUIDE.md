# Tutor guide — Lab 01: flow, pumps and pipe selection

Tutor-only explanation for [the student notebook](lab.ipynb) and
[the solution](lab_solution.ipynb). Follow the **four-hour Parts 1–4 route**.
The former pump-arrangement task and separate report are not required. A short
decision in Part 4 replaces that report. All equipment curves, limits and costs
are synthetic teaching inputs, not manufacturer specifications.

## Session plan and the main conceptual distinction

| Part | Minutes | Tutor checkpoint |
| --- | ---: | --- |
| 1 | 20 | Student identifies open-tank surfaces and the trial-flow versus fixed-duty cases |
| 2 | 60 | Student explains head, BEP and all three power levels |
| 3 | 70 | All diameters compared at exactly 3 L/s, with speed adjusted |
| 4 | 90 | Feasible cost choice, one rejection and 100–150 word decision; includes break |

The most important distinction is **uncontrolled intersection versus controlled
delivery**. A pump does not simply deliver its BEP flow. A head intersection
does not prove acceptable operation. Minimum electricity does not necessarily
mean minimum lifecycle cost. Use these three distinctions to guide discussion.

## Worked example: account for every contribution

The small example tests 3 L/s in a 65 mm pipe. It is not imposing the pump's
uncontrolled operating flow. Density is 998 kg/m³, viscosity 0.001 Pa s,
roughness 0.000045 m, length 120 m, rise 12 m and g = 9.81 m/s².
The supplied total fitting coefficient is K = 8, dimensionless, referenced to
the pipe velocity. It is not a count of eight fittings.

Between open tank surfaces, pressure terms cancel and surface velocities are
negligible. Bernoulli reduces to:

$$
H_p=\Delta z+h_f+h_K,\qquad
h_f=f_D\frac{L}{D}\frac{v^2}{2g},\qquad h_K=8\frac{v^2}{2g}.
$$

At 0.003 m³/s, area πD²/4 gives v = 0.904075 m/s and Re ≈ 58647.
The supplied Haaland approximation gives Darcy f ≈ 0.022300. Pipe loss is
1.715095 m, fitting loss 0.333273 m, and required head 14.048368 m.
The equivalent pressure rise is ρgH ≈ 137.54 kPa. Head is energy per unit
weight, not a physical elevation change for every term.

The full-speed pump provides 40 − 1.5 × 10⁶(0.003)² = 26.5 m at this
trial flow. The head surplus means this is not its uncontrolled intersection.
The actual intersection is at higher flow. If a student equates 26.5 m with
system demand at 3 L/s, ask which curve that value came from.

At 50 mm and the same 3 L/s, pipe and fitting losses become about 6.348 and
0.952 m, with total 19.300 m. Diameter affects velocity and both loss terms.
The static 12 m remains; as flow tends to zero, dynamic losses vanish and
required head tends to 12 m. Do not evaluate 64/Re at Re = 0.

## Part 2: performance curves and energy accounting

Reference head is Href(q) = 40 − 1.5 × 10⁶q² m; reference shaft power is
900 + 40000q W, with q in m³/s. These two assumed curves jointly determine
pump efficiency, rather than an independent efficiency curve being fitted too:

$$
\eta_p=\frac{\rho gQH}{P_{shaft}},\qquad
P_{electric}=\frac{P_{shaft}}{0.90\times0.96}.
$$

At speed ratio s, head scales as s²Href(Q/s) and shaft power as
s³Pshaft,ref(Q/s). Corresponding points preserve modelled pump efficiency;
the actual system intersection need not remain at a corresponding point.
Approximate affinity scaling is an assumption, not measured speed-map data.

The reference BEP is about 2.862 L/s. The assumed band is 0.65–1.35 times
the BEP flow at the actual speed. Speed itself must lie between 0.6 and 1.1.
These are separate checks. They do not establish NPSH or mechanical suitability.

The full-speed, 65 mm uncontrolled intersection is 4.03456 L/s at 15.5835 m.
It lies beyond the assumed band despite being a valid hydraulic root. Hydraulic
output is 615.55 W, shaft input 1061.38 W, and electrical input 1228.45 W.
At 4000 h/year, electrical energy is 4913.81 kWh. Show that 615.55/1061.38
≈ 0.57995 and that electrical input exceeds shaft input.

The older 3517 kWh value belonged to a different, constant-efficiency shaft-energy
model. It is not the electrical answer in this lab. At shutoff, this model has
900 W shaft input but zero hydraulic output and efficiency. Nonzero consumption
does not make shutoff an acceptable duty. Negative-head extrapolation beyond
runout is outside the performance model.

## Part 3: derive the fixed-flow speed rather than guess it

For each diameter, calculate system head at **exactly 0.003 m³/s**. Then solve
Hrequired = 40s² − aQ²:

$$
s=\sqrt{\frac{H_{required}+aQ^2}{40}}.
$$

This equation represents variable-speed matching with no throttle or bypass.
Evaluate power and efficiency at that speed, then screen both speed and Q/(sQBEP).
Do not compare one candidate at 3 L/s with another at its uncontrolled flow.

| Internal diameter | Speed ratio | Pump efficiency | Electrical input | Annual electricity |
| --- | ---: | ---: | ---: | ---: |
| 50 mm | 0.9055 | 73.94% | 887.37 W | 3549.47 kWh |
| 65 mm | 0.8299 | 69.11% | 691.02 W | 2764.07 kWh |
| 80 mm | 0.8103 | 67.22% | 645.32 W | 2581.29 kWh |

All three pass the assumed default screening limits and deliver 43200 m³/year.
Specific energies are 0.082164, 0.063983 and 0.059752 kWh/m³. Derive the
conversion by dividing W by m³/s to obtain J/m³, then by 3.6 × 10⁶ J/kWh.

Larger pipes lower pump efficiency here because reducing speed at fixed flow
moves Q/s farther right relative to the scaled BEP. Nevertheless, electrical
input falls: the reduction in required head outweighs the efficiency change.
Ask “Which has improved: hydraulic duty, pump efficiency, or both?” rather
than accepting “the bigger pipe is more efficient” without a definition.

## Part 4: explain the cost choice and robustness

Given installed pipe costs are €6000, €8500 and €12000. At €0.20/kWh,
4000 h/year and ten undiscounted years, compute:

$$
C_{model}=C_{pipe}+10\,c_e E_{annual}.
$$

Totals are about €13098.94, €14028.14 and €17162.57. Thus **50 mm is
least cost**, while **80 mm uses least electricity**. Feasibility must precede
cost ranking; a cheap candidate outside operating limits is ineligible.

The 50-to-65 mm upgrade costs €2500 and saves 785.40 kWh/year, or
€157.08/year at the stated price. Simple payback is 15.92 years, beyond the
ten-year horizon. The 65-to-80 mm payback is about 95.74 years; the direct
50-to-80 mm payback about 30.99 years. At €0.10/kWh the 50 mm choice
remains preferred; at €0.40/kWh the 65 mm choice wins.

The selected 50 mm option remains screened feasible over the supplied roughness
range. Flow remains fixed by speed adjustment: it is wrong to describe this
sweep as roughness reducing delivered flow under the assumed control policy.
Discuss changed speed, electrical input and band checks instead.

Installation prices, efficiencies and the load profile are assumed. Quotes,
maintenance, discounting, motor/drive maps and measured pump data could change
the ranking. Constant motor efficiency is especially a simplification across
different loads. “Cheapest in this supplied table” is defensible; “the optimal
commercial pump system” is not.

## End-of-lab decision and tutor responses

A sufficient decision names the fixed duty, a feasible pipe/speed, electrical
energy, the cost criterion, a rejected alternative and one material assumption.
It need not repeat all calculations. The default recommendation is 50 mm at
s ≈ 0.9055, conditional on the supplied costs and screening limits.

Common prompts:

- “Which boundary does that power refer to: water, shaft or electrical supply?”
- “Are both pipes delivering the same annual volume?”
- “Did you test the band at this speed, or only at reference speed?”
- “What evidence would make you choose 65 mm instead?”

Accept other well-supported selections when students explicitly change a price
or state an energy-only objective. Require the objective to be stated. Do not
reintroduce the removed series/parallel task or ask for a separate Part 6 report.
The optional throttling discussion is outside the four-hour assessment: at a
fixed speed and fixed flow, excess head is dissipated in a valve, so diameter
savings cannot simply be copied from the variable-speed calculation.
