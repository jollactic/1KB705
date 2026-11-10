# Tutor guide — optional absorption workshop

Use with [the student notebook](lab.ipynb) and [the executed solution](lab_solution.ipynb).
This is optional self-study, not assessed main-lab work. Support a four-hour route
through balances, supplied stepping and one robust height/cost comparison. The
separate sensitivity section and rate-model extension are further exploration.

## Establish the composition and flow basis first

Gs and Ls are **solute-free molar flows**. Gas composition Y is moles of
solute per mole of carrier, and liquid X is moles of solute per mole of solvent.
They differ from mole fractions y and x:

$$
Y=\frac{y}{1-y},\quad y=\frac{Y}{1+Y},\qquad
X=\frac{x}{1-x},\quad x=\frac{X}{1+X}.
$$

This basis keeps carrier and solvent flows constant as solute transfers. Total
mixture flows need not be constant. Fractions may be numerically close to ratios
in dilute systems, but exchanging them silently changes the equations.
Equilibrium Y* = mX with m = 1.5 is a synthetic linear model; it is
not a property correlation for a named gas/solvent pair. Assume isothermal,
nonreacting operation and no carrier/solvent loss.

## Worked example: derive two contacts from top conditions

The smaller example uses Gs = 100, Ls = 300 kmol/h, Xin = 0 and
Yout = 0.002. The main case later uses a different Yout and Ls. Starting
at the top gas composition, equilibrium gives Xn = Yn/m; the operating balance
then gives:

$$
Y_{n+1}=Y_{out}+\frac{L_s}{G_s}(X_n-X_{in}).
$$

At contact one, X1 = 0.002/1.5 = 0.0013333 and next Y = 0.006.
At contact two, X2 = 0.006/1.5 = 0.004 and next Y = 0.014.
For the optional continuation to Yin = 0.03, contact three reaches 0.03.
The minimum solvent for this small example is 140 kmol/h, so Ls = 300
is above it. At Ls = 400, the first next-Y is 0.007333 and second
0.021556; three full contacts still suffice. Larger steps do not necessarily
change an integer count immediately.

Ask students to name the physical relation for each move. Horizontal means
equilibrium; vertical means the operating balance. They are not two independent
equilibrium contacts. The plotted first two contacts are demonstrations, not a
given equipment height.

## Main balance and minimum solvent

Main inputs are Gs = 100 kmol/h, Yin = 0.03, Yout = 0.003, Xin = 0
and m = 1.5. Entering and leaving solute are 3 and 0.3 kmol/h, so
removal is 2.7 kmol/h or 90%. Gas mole fractions are 0.029126 and
0.002991. Removal percentage should use solute flows, not assume equal total
gas mixture flow when comparing fractions.

For the baseline chosen Ls = 202.5 kmol/h:

$$
X_{out}=X_{in}+\frac{G_s}{L_s}(Y_{in}-Y_{out})=0.0133333,
$$

equivalent to liquid mole fraction 0.0131579. The liquid gains 202.5 ×
0.0133333 = 2.7 kmol/h, matching gas removal.

At a limiting bottom pinch Xout = Yin/m. Substitute this into the balance:

$$
L_{min}=G_s\frac{Y_{in}-Y_{out}}{Y_{in}/m-X_{in}}=135\ \mathrm{kmol/h}.
$$

At baseline solvent flow the top driving force is Yout − mXin = 0.003;
the bottom force is Yin − mXout = 0.010. Both are positive. At Lmin,
the limiting driving force vanishes and a finite equilibrium-stage count cannot
cross the pinch. A numerical failure near a pinch has physical meaning.

## Contact counts and the baseline height models

At 1.1, 1.5 and 2 times nominal Lmin, solvent flows are 148.5, 202.5
and 270 kmol/h; nominal full-contact counts are ten, five and three. Count
the final contact in full when its vertical move reaches or exceeds Yin.
Do not compare a rounded count with a fractional-stage result without stating
the convention.

For fresh solvent, the recurrence can be checked independently with absorption
factor A = Ls/(mGs): Y(N+1)/Yout = 1 + A + ... + A^N. This is
a tutor check, not a required student derivation or new coding task.

Five nominal ideal contacts convert either to nine trays at overall efficiency
0.60 and 4.05 m active height, **or** to 3–6 m packed height at HETP
0.6–1.2 m. HETP and tray efficiency are alternative equipment conversions.
Applying both to packing would double-count an unsupported inefficiency allowance.

The illustrative 1 m² section and 0.8 m³/s gas flow give superficial velocity
0.8 m/s. Dry Ergun predicts 47.927 Pa/m, or 144–288 Pa over 3–6 m.
This excludes wet loading, holdup, distributors, packing-specific geometry and
flooding. It cannot approve a real irrigated absorber or determine a safe diameter.

## Robust height/cost challenge: compare adverse cases fairly

Use adverse m = 1.8, conservative HETP = 1.2 m and maximum active packed
height 6 m. Installed packing-section cost is €20000 + €6000 per metre
of required active height. Annual solvent service is €60 per (kmol/h) circulation,
assuming 4000 h/year, over ten years without discounting. This combined service
allowance is not a calculated regeneration heat or solvent purchase rate.

| Ls kmol/h | Nominal contacts | Adverse contacts | Adverse height | Ten-year total | Decision |
| ---: | ---: | ---: | ---: | ---: | --- |
| 148.5 | 10 | No finite feasible separation | — | — | Reject: Ls below adverse minimum |
| 202.5 | 5 | 6 | 7.2 m | €184700 | Reject: active height |
| 243 | 4 | 5 | 6.0 m | €201800 | Eligible; least modelled cost |
| 270 | 3 | 4 | 4.8 m | €210800 | Eligible; more circulation cost |
| 337.5 | 3 | 3 | 3.6 m | €244100 | Eligible; least height, not least cost |

At adverse slope, Lmin = 162 kmol/h. Thus the cheapest low-solvent option
cannot be made feasible by adding height. The baseline 202.5 option remains
thermodynamically feasible but violates height. The final selected 243 kmol/h
candidate has five adverse contacts and exactly 6 m active height, with **no
additional height margin**. It is not the baseline five-contact design at
202.5 kmol/h; distinguish their nominal and adverse counts.

At fixed HETP, more solvent can reduce height while increasing total cost.
At larger HETP the selected candidate can fail. Ask “What was held fixed
when you compared costs?” and “Which uncertainty is covered, and which remains?”
A robust-to-equilibrium screen does not resolve transfer-performance or hydraulic
uncertainty.

## Further exploration and acceptable conclusions

The original fixed-flow sensitivity at m = 1.2, 1.5 and 1.8 gives minimum
solvent 108, 135 and 162 kmol/h and counts three, five and six at Ls =
202.5. This explains why nominal feasibility is insufficient for the height screen.
Students should revise the baseline policy rather than silently adding a tray
efficiency to an HETP estimate.

The optional transfer-unit model uses the integral of dY/(Y − Y*) along
the operating line, yielding NOG ≈ 4.643895 at baseline. It is not the
number of equilibrium contacts. Height needs an independent HOG; the illustrated
0.8 m gives about 3.715 m but is assumed, not derived from equilibrium.
Film coefficients, wetted interfacial area, properties and loading dependence are
needed to justify a real transfer-unit height.

A sound self-study conclusion chooses a feasible candidate under stated limits,
names the rejected pinch/height cases and requests equilibrium, HETP, wet pressure-
drop/capacity, liquid-distribution and cost evidence. It does not claim that the
lowest dry pressure drop or the shortest equilibrium height determines the best
industrial absorber. No formal submission is required.
