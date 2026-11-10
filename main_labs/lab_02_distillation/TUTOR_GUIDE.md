# Tutor guide — Lab 02: binary distillation

Use with [the student notebook](lab.ipynb) and [the executed solution](lab_solution.ipynb).
This is a main four-hour lab: 30/40/50/65/30/25 minutes for Parts 1–6,
including a break in Part 4. Broad purity and reflux sweeps are reference material,
not additional assessed studies. Students need no new stage-counting code.

## Before the session: separate three different calculations

The smaller worked example uses zF = 0.50, xD = 0.90, xB = 0.10 and
R = 3. The main baseline uses zF = 0.45, xD = 0.95, xB = 0.05 and
R = 2.5. The constrained policy selected later is R/Rmin = 1.8, or
R ≈ 2.43377. Write these labels on the board before discussing numerical results.
Do not mix a product flow from one case with operating lines from another.

All cases use a hypothetical binary, constant relative volatility alpha = 2.4,
constant molar overflow, saturated-liquid feed q = 1, a total condenser and an
equilibrium partial reboiler. Compositions are mole fractions of the more volatile
component. These are not validated properties of a named chemical pair.

## Worked example: balances and two graphical contacts

Around the whole column, reflux is internal and does not appear as an external
feed or product. At steady state:

$$
F=D+B,\qquad Fz_F=Dx_D+Bx_B,
\qquad D=F\frac{z_F-x_B}{x_D-x_B}.
$$

For the small example, F = 100 kmol/h gives D = B = 50 kmol/h.
Equilibrium and its inverse are:

$$
y^*(x)=\frac{\alpha x}{1+(\alpha-1)x},\qquad
x(y)=\frac{y}{\alpha-(\alpha-1)y}.
$$

Begin at (xD,xD). The total condenser gives the starting relation between the
distillate/reflux composition and entering overhead vapour. A horizontal move
keeps vapour y constant and finds its equilibrium liquid x. A vertical move
keeps this liquid x constant and finds the next vapour y from an operating line.

At R = 3, the rectifying line is y = 0.75x + 0.225. The first contact
takes y = 0.9 to x = 0.789474; the next operating-line value is y =
0.817105. The second contact gives x ≈ 0.650534 and next y ≈ 0.712901.
These first two liquid compositions are above zF = 0.5, so using the rectifying
line for both is valid. Two illustrated contacts are not the full column count.

When R rises to 5, the first equilibrium x is unchanged because starting y is
unchanged. The first next-y becomes 0.807895; the second equilibrium x falls
to 0.636665. This is a useful subtle check: reflux changes the operating-line
move before it changes the next equilibrium move.

## Part 2: main balances and minimum reflux

For the main specifications, D = 44.4444 and B = 55.5556 kmol/h.
Light-component flows are 42.2222 and 2.7778 kmol/h, summing to the entering
45 kmol/h. Total flow and component residuals should vanish before stage work.

The q = 1 feed line is vertical at x = zF. At x = 0.45, equilibrium gives
y* = 0.662577. The line from this pinch point to (0.95,0.95) has slope:

$$
m_{pinch}=\frac{x_D-y^*(z_F)}{x_D-z_F}=0.574847,
\qquad R_{min}=\frac{m_{pinch}}{1-m_{pinch}}=1.35209.
$$

At this limiting reflux, operating and equilibrium curves meet and composition
progress tends to zero. The ideal stage requirement tends to infinity. A finite
numerical answer exactly at the pinch would be suspect, not a better design.
This feed-pinch result relies on the prescribed equilibrium shape and feed state.

Tutor prompt: “Which balance sets the product flows, and which relation tells
you whether vapour and liquid can approach equilibrium?” These are different
pieces of the model and should not be conflated.

## Part 3: main staircase and counting conventions

At baseline R = 2.5, the first three equilibrium liquid fractions are about
0.887850, 0.799901 and 0.690752. The first incoming vapour values are
0.950000, 0.905607 and 0.842786. These printed coordinates allow a hand
check of the two alternating operations without writing a loop.

After equilibrium contact 6, the construction switches operating lines as liquid
x falls below zF. For the stripping line, use the line joining the feed-line
intersection to (xB,xB); continuing the rectifying line below the feed ignores
the change in liquid flow introduced by the feed.

Baseline count is **11 full ideal contacts**, including the equilibrium partial
reboiler and excluding the total condenser. The final horizontal step may pass
xB and is counted in full. A fractional last-stage interpolation is a different
convention; do not mark a reasoned alternative wrong without checking conventions.
Require students to state which one they use. Feed-line switching identifies a
feed region, not a fully optimized physical feed-tray location.

## Part 4: screen constraints before ranking costs

The required product specifications stay fixed. Given screening limits are
8 m active tray height and 190 kmol/h vapour circulation. Overall efficiency
is 0.65 and spacing 0.45 m. Subtract the ideal reboiler before converting
ideal trays into actual trays:

$$
N_{actual}=\left\lceil\frac{N_{ideal}-1}{0.65}\right\rceil,
\quad Z=0.45N_{actual},\quad V=(R+1)D.
$$

| R/Rmin | Full ideal contacts | Actual trays | Active height | Vapour kmol/h | Screen |
| ---: | ---: | ---: | ---: | ---: | --- |
| 1.1 | 18 | 27 | 12.15 m | 110.547 | Reject: height |
| 1.5 | 13 | 19 | 8.55 m | 134.584 | Reject: height |
| 1.8 | 11 | 16 | 7.20 m | 152.612 | Eligible |
| 2.0 | 11 | 16 | 7.20 m | 164.630 | Eligible |
| 2.2 | 10 | 14 | 6.30 m | 176.649 | Eligible |
| 3.0 | 9 | 13 | 5.85 m | 224.723 | Reject: vapour capacity |

The supplied approximate duty uses latent heat 30000 kJ/kmol with negligible
sensible changes: QR = V × 30000/3600 kW. The unit conversion matters:
kmol/h times kJ/kmol is kJ/h; dividing by 3600 gives kJ/s = kW.
It is an illustrative equal-latent-heat model, not a complete mixture enthalpy model.

At ratio 1.8, QR ≈ 1271.77 kW. Installed cost is €50000 + €3000 per
actual tray + €250 per (kmol/h) of V, giving about €136153. Add ten years
of heat at €0.03/kWh and 4000 h/year: total ≈ **€1662271**, the least
cost among eligible supplied candidates. Ratio 2.0 retains the same rounded
tray count while increasing circulation and heat cost. The lowest-heat policy
fails height; the fewest-stage policy fails capacity.

At 120 kmol/h feed, D and V rise by 20% at a fixed reflux policy; ideal
stages stay unchanged in this composition-based model. Ratio 1.8 still passes
at V = 183.134 kmol/h, with margin 6.866 kmol/h. Ratio 2.0 now fails
at 197.557 kmol/h. A new duty does not necessarily change the preferred policy,
but it can materially reduce operating margin.

If students choose another eligible policy, ask for the objective or changed
assumption that supports it. Do not accept an ineligible option solely because
it has the lowest total in the unfiltered table. The V limit stands in for
capacity; it is not a flooding calculation or evidence of a selected diameter.

## Parts 5–6: actual height and a concise recommendation

At the baseline 11 ideal contacts, ten ideal trays remain after subtracting the
reboiler. Overall efficiencies 0.50, 0.65 and 0.80 give 20, 16 and 13
actual trays, or 9.00, 7.20 and 5.85 m active height. Overall efficiency
converts column totals; Murphree efficiency describes a local tray approach to
equilibrium and should not be substituted without a tray model.

Active height is not vessel height. Mention overhead disengagement, bottom sump,
feed/draw allowances, supports and access. The efficiency assumption needs vendor,
pilot or comparable-service evidence. Changing it could invalidate the height screen.

A 100–150 word recommendation should name the selected ratio, both constraint
margins, the changed-feed result and at least one missing physical input. Real
VLE, enthalpies, efficiency, hydraulics and utility costs are needed before purchase.
Students need not reproduce the full table in prose. The optional purity and
equilibrium-data discussions must not displace the required four-hour work.
