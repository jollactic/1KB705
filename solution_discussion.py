"""Question-by-question model answers for the design-support lab variant.

Numbers refer to the default settings, not every possible student design.
"""

DISCUSSIONS = {
    'lab_01_flow': [r'''
**Where is energy added and lost?** The pump supplies mechanical energy to the
water between Tank A and Tank B. Wall friction dissipates energy along the pipe;
separation and mixing in bends and valves cause additional local losses. The
12 m rise stores gravitational potential energy rather than dissipating it.
With both surfaces open to air and tank velocities negligible, Bernoulli gives

$$
H_p=\Delta z+h_{\mathrm{pipe}}+h_{\mathrm{fittings}}.
$$

**One hand check.** At 3 L/s and a 65 mm internal diameter,

$$
v=\frac{0.003}{\pi(0.065)^2/4}=0.9041\ \mathrm{m/s}.
$$

Using the supplied combined coefficient, the bends and valves lose
$8(0.9041)^2/(2\times9.81)=0.3333$ m. The pipe loses 1.7151 m, so the
total requirement is $12+1.7151+0.3333=14.0484$ m. The coefficient 8 is
dimensionless and represents all specified bends and valves together.

**Pressure versus head.** Head is energy per unit weight, measured in metres.
The equivalent pressure is $\Delta p=\rho gH$, about 137.54 kPa for this
14.0484 m total head. This is the required pump pressure rise expressed on the
same energy basis; it is not the pressure at every location in the pipe.

**What can a larger pipe reduce?** It lowers velocity and therefore both pipe
and fitting losses under the lab's fixed-K assumption. It does not remove
the 12 m elevation requirement. At negligible flow, friction losses tend to
zero and the system head tends to 12 m.

**Prediction and observed smaller-pipe result.** I predict greater loss with a
50 mm pipe. At the same 3 L/s, the worked comparison gives about 6.348 m
pipe loss and 0.952 m fitting loss: 19.300 m total. This supports the prediction.
Restoring 65 mm is necessary before quoting the following base-case results.
''', r'''
**Does the base case meet the duty?** Yes: the 65 mm pipe and full-speed pump
deliver 4.03456 L/s, exceeding 3 L/s by 1.03456 L/s, or about 34.5% of the
required throughput. The operating head is 15.5835 m, shaft power is 879.35 W,
annual energy is 3517.4 kWh at 4000 h/year, and specific electricity use is
0.060543 kWh/m³. The latter follows from dividing power in W by flow in m³/s
and by $3.6\times10^6$ J/kWh.

**What does the intersection mean?** At this flow, the pump supplies exactly
the head required by elevation and losses. At a lower trial flow, the pump
curve lies above the system curve; at a higher trial flow it lies below it.
The steady operating point therefore depends on both pump and piping, rather
than being an independently imposed pump flow.

**What does the residual check establish?** A mismatch smaller than 0.001 m
shows that the numerical solution satisfies the two supplied equations to the
required tolerance. It does not verify the assumed manufacturer curve, actual
roughness or fittings, efficiency, suction conditions or cavitation margin.
Numerical convergence is distinct from experimental validation.

**Would it meet 4.5 L/s?** No. The same equipment still delivers 4.03456 L/s:
its shortfall would be 0.46544 L/s, about 10.3% of the new requirement.
Changing the requirement in the notebook changes the pass/fail decision,
not the hydraulic operating point. A speed, pump or piping change is needed.
''', r'''
**Selection criterion and shortlist.** I first enforce the 3 L/s throughput
constraint, then minimize kWh per cubic metre among the feasible candidates.
All three 0.8-speed candidates fail the nominal flow requirement, including
the 80 mm pipe at 2.9294 L/s. The six full-speed or 1.1-speed candidates
remain on the hydraulic shortlist.

**Selected design and margin.** The 80 mm pipe at speed ratio 1.0 gives
4.20830 L/s and about 790.78 W shaft power, with specific electricity use
0.052197 kWh/m³. Its nominal flow margin is 1.20830 L/s, or 40.3% of the
required 3 L/s. It is also the least-specific-energy feasible candidate in
the supplied table. Relative to the original 65 mm full-speed case, specific
energy falls by about 13.8%.

**Would I buy the larger pipe without its price?** I would carry it forward
as the preferred energy-based candidate, but would not approve procurement.
Installed pipe cost, service life, electricity price, operating hours and
maintenance are needed to compare lifecycle cost. A cheaper 65 mm installation
could be economically preferable despite greater electricity use. A claimed
economic optimum is therefore unsupported.

**Can an infeasible low-power option stay on the shortlist?** No, unless the
requirement is explicitly revised. The 80 mm, 0.8-speed option uses only about
521.5 W but misses the duty. Its low power partly reflects its lower delivered
flow. Compare specific energy as well as power, and enforce capacity first.
If the required flow rises to 4.5 L/s, my full-speed choice also fails; the
1.1-speed 65 and 80 mm candidates then deserve comparison.
''', r'''
**Worst-roughness feasibility.** For the selected 80 mm, full-speed design,
roughness $2\times10^{-4}$ m gives about 4.18676 L/s. The flow margin remains
1.18676 L/s above the 3 L/s duty, so no selection change is required solely
on this sensitivity. Specific energy becomes about 0.053251 kWh/m³.

**Which uncertainty matters most?** Over these particular stated ranges,
efficiency changes specific energy by 45.45% from minimum to maximum,
whereas roughness changes it by about 2.80%. These are max/min minus one
comparisons, not statistical confidence intervals. Different uncertainty
ranges could produce a different ranking.

**Why does efficiency not move the operating point?** Efficiency is absent
from both head curves. It appears only in

$$
P_{\mathrm{shaft}}=\frac{\rho gQH}{\eta}.
$$

Thus lower efficiency means more shaft input for the same modelled hydraulic
output. A real efficiency curve depends on flow and speed, and motor/drive
losses are not separately included here.

**What is needed before procurement?** Request tested head and efficiency
curves for the actual impeller and speed, the permitted operating range,
required NPSH, motor rating and speed-control limits. Establish available
NPSH from the suction tank level and pressure, liquid temperature/vapour
pressure, and suction-line losses. Confirm pipe dimensions, elevations and
fitting data. My recommendation is robust to the specified roughness range,
but it remains conditional on those equipment and suction checks.
'''],

    'lab_02_heat': [r'''
**Hand check and energy balance.** The cold stream requires
$1.0\times4180\times(55-15)=167200$ W, or 167.2 kW. The hot capacity
rate is $1.2\times3800=4560$ W/K, giving a hot outlet of
$85-167200/4560=48.3333$ °C. The hot and cold duties agree.

**Where are the driving forces?** At the hot-inlet/cold-outlet end,
$\Delta T_1=85-55=30$ K. At the hot-outlet/cold-inlet end,
$\Delta T_2=48.3333-15=33.3333$ K. Both are positive. The maximum duty is
$\min(4560,4180)(85-15)=292.6$ kW, so the target is feasible in the
ideal model and uses 57.14% of this maximum.

**Why can the outlets cross?** The 55 °C cold outlet and 48.3333 °C hot
outlet are at opposite ends. The hot stream remains warmer than the adjacent
cold stream at each terminal location. Comparing the two outlet temperatures
alone is not a test of local heat-transfer direction. The connecting lines
in the temperature figure are schematic, not calculated profiles.

**Plant measurements.** Measure both mass flows, all four temperatures,
stream compositions and relevant heat capacities. Record uncertainties and
steady-state conditions so the two duties can be compared meaningfully.
Check ambient losses and changes in inventory before attributing a duty
imbalance to the exchanger itself.
''', r'''
**Agreement of methods.** The supplied effectiveness–NTU calculation gives
the same 55 °C cold outlet, 48.3333 °C hot outlet and 167.2 kW duty as
the LMTD calculation at 8.13059 m² clean area. NTU is about 1.2643 and
the capacity ratio is about 0.9167.

**Physical limiting cases.** At zero UA or zero area, there is no heat
transfer: both streams leave at their inlet temperatures. With increasingly
large UA, effectiveness tends to one; the smaller-capacity stream approaches
the other stream's inlet temperature. A finite, ideal exchanger cannot
exceed the maximum duty. For equal capacity rates the analytical expression
must use its limit, $\varepsilon=NTU/(1+NTU)$.

**What do the checks prove?** Agreement and limiting cases support the
implementation and internal consistency of the ideal thermal model. They
do not prove actual equipment performance. Confirm U at the actual velocities,
temperature-dependent properties, fouling behaviour, external heat losses,
flow distribution and whether the geometry is truly countercurrent.

**Readiness decision.** I would submit the calculation for thermal review
and proceed to hydraulic/geometric design, not purchase. Allowable pressure
drop, channel dimensions, pumping power and mechanical requirements have
not been checked. A model can pass thermal verification while describing
equipment that is impractical or hydraulically unsuitable.
''', r'''
**Chosen allowance and area.** I use the default added resistance
0.0006 m² K/W. It lowers U from 650 to about 467.63 W/(m² K).
The clean-sized area of 8.13059 m² then gives only 142.16 kW and a cold
outlet of 49.0093 °C. It cannot meet the stated 55 °C target.

**Added area percentage.** Retaining the target duty and terminal temperatures
requires 11.3015 m². Since thermal resistance increases by a factor
$1+650(0.0006)=1.39$, the required area increases by **39%**. The supplied
fixed-area curves instead let duty and outlets change as resistance grows;
these are different design questions.

**Decision and alternative.** If 55 °C at 1 kg/s is a process requirement
through the stated fouling condition, I would specify the enlarged thermal
area, subject to hydraulic review. Accepting 49 °C would violate that
requirement. A smaller unit could be defended only with an explicitly
permitted lower temperature, supplemental heating or a justified cleaning
policy; it is not an equivalent design by itself.

**Clean operation and control.** The enlarged exchanger gives about 60.80 °C
when clean at these flows. If 55 °C is an exact target, use suitable bypass
or temperature/flow control. Extra installed area is not automatically a
safe operating margin if excessive outlet temperature is undesirable.
''', r'''
**Qualifying tested flows.** At the chosen fouling-sized area and design
resistance, the sweep meets at least 55 °C for tested cold flows from
0.5 through 1.0 kg/s. The explicitly included 1.0 kg/s point gives exactly
55 °C. Higher tested flows fall below target. This is a sampled thermal
envelope under fixed U, not a certified continuous operating range.

**Selected operating policy.** I retain 1.0 kg/s as the nominal design flow
because it meets the original throughput and temperature requirement.
Lower flows give hotter water but deliver less water and less total heat;
they should not be presented as equivalent ways to meet a 1 kg/s duty.
The nominal point has no temperature margin at the specified design fouling,
so control, cleaning or an additional justified allowance deserves review.

**Heat recovery versus temperature.** At 0.5 kg/s the model gives about
74.09 °C and 123.50 kW; at 1.8 kg/s it gives 40.24 °C and 189.91 kW.
More recovered heat does not guarantee a useful delivery temperature.

**Missing hydraulic work.** Establish channel/tube geometry, velocities,
Reynolds numbers, pressure drop, pump duty and allowable mechanical loads.
U generally changes with flow through convection coefficients; heat losses
and fouling can also vary. These omissions make the constant-U envelope
provisional even though its energy balances close.
'''],

    'lab_03_distillation': [r'''
**Duty and diagram.** The feed is 100 kmol/h at zF = 0.45. Overhead vapour
enters a total condenser; part returns as reflux and the remainder leaves
as distillate. Bottom liquid exchanges material with the partial reboiler
and leaves as bottoms. Reflux is internal to the overall column balance.

**Balance check.** Product flows are D = 44.4444 and B = 55.5556 kmol/h.
For the light component, $44.4444(0.95)+55.5556(0.05)$ is approximately
45 kmol/h, matching $100(0.45)$. Rounding the printed flows may leave
a small residual; the calculation uses their unrounded values.

**Why minimum reflux is not an operating design.** For saturated-liquid feed,
the feed line is vertical at zF. The pinch construction gives Rmin = 1.35209.
At that limiting reflux the operating and equilibrium curves touch at the
feed pinch and the local composition change per stage tends to zero.
Infinitely many contacts would be required to cross it in the ideal model.
A finite column therefore needs reflux above this limit. This conclusion
depends on the stated constant-volatility, q = 1 model; a real mixture's
equilibrium curve and feed condition must be checked.
''', r'''
**Chosen reflux and one contact.** I use R = 2.5, above Rmin = 1.35209.
The first horizontal move takes vapour y = 0.95 to the equilibrium liquid
x = 0.887850. At that same x, the vertical move reaches the rectifying
line at y = 0.905607. The horizontal move applies equilibrium; the vertical
move applies the section material balance.

**Feed switch and counting convention.** The supplied construction switches
to the stripping operating line after equilibrium contact 6, where liquid
composition falls below zF. The base solution needs 11 full ideal contacts,
including an equilibrium partial reboiler and excluding the total condenser.
The final contact is counted in full even when it passes the specified xB.
Thus ten ideal trays remain before an efficiency conversion. The switching
contact locates the feed region under this convention, not an independently
optimized physical feed-tray location.

**Higher-reflux comparison.** At R = 3 the same model needs ten full ideal
contacts instead of eleven, while vapour circulation rises from 155.56 to
177.78 kmol/h, about 14.3%. At R = 4 it needs nine contacts and
222.22 kmol/h of vapour. More circulation can reduce contact requirements,
but also affects utilities and column diameter. The calculation alone
does not show that the higher-reflux design is cheaper.
''', r'''
**Preliminary reflux policy.** I retain R = 2.5 for further design review,
not as a proven optimum. The sweep gives 18, 13, 11, 10 and 9 full ideal
contacts at R/Rmin = 1.1, 1.5, 2.0, 2.5 and 3.0 respectively. Stage
reduction becomes less pronounced as reflux increases. Within each integer
stage-count plateau, extra reflux increases vapour circulation without
reducing the reported number of full contacts.

**Is 0.98 purity justified if 0.95 suffices?** Not on the supplied evidence.
At R/Rmin = 1.5, the 0.95 case gives 13 contacts, 44.444 kmol/h distillate
and 134.584 kmol/h vapour. The 0.98 case gives 14 contacts,
43.011 kmol/h distillate and 139.347 kmol/h vapour. It increases separation
effort and reduces distillate product flow without a stated benefit for
the higher purity. A product premium or downstream requirement could
change that decision. The 0.90 option is not eligible if 0.95 is mandatory.

**Why no economic optimum yet?** Minimum reflux would need infinite stages;
minimum stages drives greater circulation. Convert circulation to utility
duties using enthalpies and latent heats. Add tray efficiency, diameter,
hydraulics, condenser/reboiler areas, utility prices, operating hours and
equipment costs. Compare actual product value and recovery as well as purity.
''', r'''
**Selected efficiency assumption.** I use overall tray efficiency 0.65
provisionally. With ten ideal trays, rounding $10/0.65$ upward gives
16 installed trays and 7.20 m active height at 0.45 m spacing. At 0.50
and 0.80 efficiency the estimates are 20 and 13 trays, or 9.00 and
5.85 m. The default 0.65 is a teaching assumption, not evidence about
a particular tray. Comparable-mixture operating data, pilot work or a
validated tray/vendor correlation would justify an equipment estimate.

**Overall versus Murphree efficiency.** Overall efficiency relates total
ideal trays to total actual trays for the column. Murphree efficiency
describes an individual tray's composition change relative to its local
equilibrium limit. The latter belongs in a tray-by-tray model; substituting
it directly for overall efficiency is not generally justified.

**Active versus vessel height.** The lab uses tray count times spacing
as an active-height convention. A vessel also needs overhead disengagement
space, bottom sump space, feed and draw-off allowances, and supports or
access provisions. The separate condenser and reboiler require layout too.

**Effect on reflux policy.** The 13–20 tray range is material: uncertainty
could change capital cost and whether a height limit is met. Higher reflux
may reduce ideal stages, but could also change loading and efficiency.
I would compare reflux policies across a credible efficiency range before
fixing the vessel; I would not assume more reflux is automatically preferable.
'''],

    'lab_04_absorption': [r'''
**Removal and basis check.** Incoming solute is $G_sY_{in}=100(0.03)=3$
kmol/h; outgoing solute is $100(0.003)=0.3$ kmol/h. Removal is therefore
2.7 kmol/h, or 90%. The solvent gains the same amount. Using mole ratios
with solute-free flows keeps the carrier and solvent basis constant even
though total mixture flows change as solute transfers.

**Compositions.** Gas mole fractions are approximately 0.029126 in and
0.002991 out. The rich-solvent ratio is Xout = 0.0133333, or a mole
fraction of 0.0131579. Ratios and fractions must not be interchanged in
the operating-line equations.

**Driving forces and feasibility.** At the top, compare the outgoing gas
with equilibrium over entering solvent: $Yout-mXin=0.003$. At the bottom,
compare incoming gas with equilibrium over rich solvent:
$Yin-mXout=0.010$. Both are positive. At the limiting bottom pinch,
$Xout=Yin/m$; substituting into the balance gives Lmin = 135 kmol/h.
The selected 202.5 kmol/h is 1.5 times this limit. It is feasible in the
linear equilibrium model, but this does not yet verify transfer rate,
wet hydraulics or real solvent capacity.
''', r'''
**Solvent-policy comparison.** At L/Lmin = 1.1, 1.5 and 2.0, the solvent
rates are 148.5, 202.5 and 270 kmol/h and the calculated requirements are
ten, five and three full ideal contacts respectively. These alternatives
illustrate why approaching the pinch saves solvent at the expense of
height, while more solvent reduces contacts but increases handling.

**Provisional choice.** I retain L/Lmin = 1.5 as a starting point:
five contacts at a rate 50% above the nominal minimum. This is a margin
relative to an equilibrium limit, not a flooding or safety margin. The
1.1 option is less attractive if equilibrium is uncertain; the 2.0 option
could be justified by a strict height constraint but needs a circulation
and cost assessment.

**What could change the choice?** Solvent price, regeneration heat,
recovery/recycle requirements, liquid pumping and distribution, wet pressure
drop, packing/tray cost and available vessel height could favour a different
policy. None is quantified by the equilibrium staircase.

**Final full-contact convention.** Stepping from the known top conditions,
the last vertical move reaches or exceeds Yin. Keeping the entire final
contact rounds the requirement upward rather than interpolating a partial
one. That convention explains a conservative integer count; it does not
ensure the same margin against uncertainty in equilibrium or efficiency.
''', r'''
**Height comparison.** Five ideal contacts at overall tray efficiency 0.60
give nine actual trays, hence 4.05 m active height. Independently, HETP
of 0.6–1.2 m gives 3–6 m active packed height. These ranges overlap,
so height alone does not establish a preferred internals type. I would
defer final selection until capacity, wet pressure drop, distribution,
fouling tendency, maintenance and transfer-performance data are available.

**Hydraulic screening numbers.** The illustrative area of 1 m² and gas
flow of 0.8 m³/s give 0.8 m/s superficial velocity. The dry Ergun model
predicts 47.927 Pa/m, or about 144–288 Pa over the 3–6 m packed height.
Distributor and other internal losses are not included.

**Would this approve an irrigated absorber?** No. The dry equivalent-particle
model does not represent liquid holdup, wetted effective area, packing
shape, countercurrent loading or flooding. Obtain packing-specific wet
pressure-drop and capacity curves at the actual gas/liquid properties and
loads. The supplied cross-sectional area is an assumed screening input,
not a hydraulically selected column diameter.

**Why not multiply packing height by tray inefficiency too?** HETP already
converts ideal stages to packed height. Overall tray efficiency is a
different equipment model for actual tray count. Applying both would mix
two alternative conversions without a physical basis.
''', r'''
**Requested uncertainty cases.** At m = 1.2, 1.5 and 1.8, the minimum
solvent rates are 108, 135 and 162 kmol/h. At fixed L = 202.5 kmol/h,
all are feasible, but the full-contact counts are three, five and six.
At the adverse slope the nominal 50% solvent excess over minimum shrinks
to 25%. Feasibility alone therefore does not demonstrate adequate height.

**Does the nominal height have enough margin?** A design based strictly
on five contacts does not cover the six-contact adverse case at unchanged
performance assumptions. Trays would increase from nine to ten actual
trays (4.05 to 4.50 m active height). At the same HETP, packed height
would rise by 20%, giving 3.6–7.2 m across the stated HETP range. Do
not interpret the nominal upper value of 6 m as automatically sufficient
when both equilibrium and HETP may be adverse.

**Decision.** Before fixing a new vessel, obtain better equilibrium data
and carry the six-contact case in the preliminary height allowance.
Alternatively, increasing solvent to 243 kmol/h at m = 1.8 preserves
the nominal absorption factor and restores five contacts in this model.
That option needs wet-hydraulic and solvent-cost checks before adoption.

**Vendor evidence needed.** Request wet loading/flooding curves, recommended
capacity margins, liquid distributor operating limits, holdup and packing-
specific transfer data. Dry Ergun contains none of these relationships.
The conditional response should therefore address both equilibrium margin
and actual equipment performance, rather than simply increasing a dry
pressure-drop allowance.
''']
}


COMPARISON_CODE = {
    'lab_03_distillation': '''
    # Supporting comparison for the written default-case answers.
    print("Reference comparison: same base feed and product compositions")
    for comparison_R in [2.5, 3.0, 4.0]:
        comparison_N = distillation_steps(.45,.95,.05,comparison_R,2.4)[0]
        comparison_D = 100*(.45-.05)/(.95-.05)
        print(f"R={comparison_R:.1f}: {comparison_N} full ideal contacts; V={(comparison_R+1)*comparison_D:.3f} kmol/h")
    ''',
    'lab_04_absorption': '''
    # Supporting comparison for the written default-case answers.
    print("Reference comparison at m=1.5 and Lmin=135 kmol/h")
    for comparison_multiple in [1.1,1.5,2.0]:
        comparison_L = comparison_multiple*135
        comparison_N = absorption_steps(100,comparison_L,.03,.003,0,1.5)[0]
        print(f"L/Lmin={comparison_multiple:.1f}: L={comparison_L:.1f} kmol/h; {comparison_N} full contacts")
    assert absorption_steps(100,243,.03,.003,0,1.8)[0] == 5
    print("Adverse m=1.8, increased L=243 kmol/h: 5 full contacts")
    '''
}
