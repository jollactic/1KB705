# Instructor notes — draft for review

These labs are designed as computational design exercises, not laboratory
measurement protocols. Pilot the six-hour workload and review the intended
syllabus version before assigning. In this **design-support variant**, students
need only know how to run a cell, change a parameter and read a table or plot.
Numerical methods are supplied. No physical equipment or
hazardous-material handling is part of these exercises.

## Common facilitation

Start with a flowsheet and a prediction. At 90 minutes, check one hand calculation
and the student's units before discussing a recommendation. At three hours,
require a feasible candidate and its operating margin. If a pair is behind,
help identify the decisive table rows or plot region rather than assigning
algorithm implementation. Extensions are enrichment, not an assessment requirement.

Use the embedded diagram to establish the system boundary before equations.
Students should spend about 20 minutes of the model-development block running
the worked example and making the suggested small change. Ask them to predict
the result aloud before running it. The `ex_` variable prefix separates these
small examples from the main case. The separation examples show two steps;
the supplied main-case routine completes the staircase and all feasibility checks.
Keep the six-hour total by using this example as the start of model development,
rather than as an additional activity.

The supplied helper functions intentionally expose reference calculations.
Students should explain the balances, hand-check one quantity, interpret supplied
verification results and explain infeasible designs. Their deliverable is a
defended design decision, not new code. Use conservation and limiting cases to
distinguish numerical consistency from real equipment validation.

Assess model understanding (25%), design choices and tradeoffs (35%), robustness
and limits (25%), and communication/reproducibility (15%). For each major decision,
look for a requirement, at least two numerical facts, a rejected alternative,
and a reason new evidence might change the choice. The saved solution notebooks
illustrate the base settings; other feasible, well-supported choices are valid.
Require students to rerun downstream cells after editing a setting. The default
settings reproduce the reference recommendations for the current editions.

## Benchmark results

These values use the stated synthetic base cases and full-final-stage convention.

Completed, executed reference notebooks are saved as `lab_solution.ipynb` in each
lab folder. They include the small-change exercises, all core tasks, written
recommendations and optional extensions. Rebuild with `python build_solutions.py`.
The student notebooks are not modified by that command. Lab 1 now uses variable
pump efficiency and motor/drive losses, compares diameters at exactly 3 L/s using
speed control, and includes series/parallel pumps in its core. At default costs,
50 mm minimizes the ten-year pipe-plus-electricity total; 80 mm minimizes
electricity alone. This supersedes the previous uncontrolled-flow, constant-70%
efficiency comparison.

Each main solution section now answers the individual design questions explicitly:
the numerical evidence, selected policy, rejected alternative, margin and limits.
These discussions are maintained in `solution_discussion.py` for Labs 2–4 and
`flow_solution.py` for Lab 1. Extra reference
comparisons in the distillation and absorption solutions reproduce the alternative
cases quoted in the prose. The written answers assume default settings and do
not automatically change when a reader edits a parameter.

| Lab | Benchmarks |
| --- | --- |
| 1 | Uncontrolled 65 mm, speed 1: Q = 4.03456 L/s, electrical input = 1228.45 W; outside the assumed band. At controlled 3 L/s, 50/65/80 mm use 3549.47/2764.07/2581.29 kWh/year. Ten-year costs at €0.20/kWh: €13098.94/14028.14/17162.57. Duty A: parallel, 1436.91 W total. Duty B: series, 2479.49 W total. |
| 2 | Duty = 167.2 kW, hot outlet = 48.3333 °C, clean area = 8.13059 m². At added resistance 0.0006 m² K/W and fixed clean-sized area: cold outlet = 49.0093 °C. |
| 3 | D = 44.4444 kmol/h, B = 55.5556 kmol/h, R_min = 1.35209. At R = 2.5: 11 full ideal stages including the reboiler; ten ideal trays. At E_o = 0.65: 16 installed trays and 7.2 m active-height estimate. |
| 4 | L_min = 135 kmol/h; selected L = 202.5 kmol/h; X_out = 0.0133333; removal = 2.7 kmol/h. Five full ideal stages. At E_o = 0.60: nine trays, 4.05 m active height. Packed height = 3–6 m; illustrative dry gradient = 47.9272 Pa/m, giving about 144–288 Pa. |

Lab 1: the synthetic head and shaft-input curves define pump efficiency jointly.
Motor and drive efficiencies remain constant at 0.90 and 0.96. Neither an
intersection nor a low price makes a point eligible outside the assumed speed
or per-pump BEP band. Pair powers must sum both running pumps. The 80 mm line
for changed duties is deliberate: it is not the selected default 50 mm base line.
The declared six-hour allocation is 30/60/75/90/60/45 minutes, including a break.
Separate procurement checks from the synthetic feasibility screen. The original
3517 kWh figure was shaft energy under a different efficiency assumption and
must not be reused as electrical energy in this edition.

Lab 2: outlet temperatures can cross when comparing the two outlet streams at
opposite ends of a countercurrent exchanger. Local terminal driving forces must
remain positive. A fixed-area fouled exchanger has a lower duty, rather than the
same duty at a different LMTD chosen arbitrarily. With constant design temperatures,
the required fouled-sized area scales as U_clean/U_fouled: about 11.30 m² here.

Lab 3: the final horizontal step generally overshoots xB. Eleven stages is the
deliberately conservative integer count, not an interpolated value. The total
condenser is not a stage; the equilibrium partial reboiler is. Subtract the reboiler
before converting ideal trays to actual trays. Constant-alpha equilibrium lacks
azeotropes; applying it to a real mixture without checking VLE is inappropriate.

Lab 4: use mole ratios throughout, not a mixture of ratios and fractions.
The staircase starts at the top, and the final vertical move may exceed Yin.
For fresh solvent, the absorption factor A = L/(mG) gives the independent check
Y_(N+1)/Yout = 1 + A + ... + A^N. HETP and tray efficiency represent different
equipment models. The dry Ergun example is a screening exercise in model limits;
it is not a pressure-drop or flooding design method for irrigated industrial packing.

## Acceptance checks

- Balances close within numerical precision, and printed quantities have units.
- Numerical searches check feasibility and report non-convergence explicitly.
- Sensitivities hold the intended installed geometry or flow constant.
- Plots include readable labels, units and legends where needed.
- Recommendations acknowledge the missing physical properties, hydraulics,
  equipment data and capital costs rather than claiming a validated optimum.

`python validate_labs.py` checks authored notebook structure, executes the supplied
cells, and verifies selected physical benchmarks, limiting cases and invalid-input
behaviour. It does not execute student-written answers, validate Colab's live UI,
or measure completion time. No live Colab session has been used to test these drafts.
