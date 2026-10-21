"""Reference answers for Lab 1's variable-efficiency, fixed-duty edition."""
FLOW_DISCUSSIONS = [r'''
**Hand check and system boundary.** At 3 L/s in the 65 mm pipe,
$v=0.003/[\pi(0.065)^2/4]=0.90408$ m/s. With the determined total K = 8,
fitting head loss is $8v^2/(2g)=0.33327$ m. The 12 m elevation rise is
stored gravitational energy, whereas pipe and fitting losses are dissipation.
Both free surfaces are open to air, so their pressures cancel in Bernoulli.

**Reading the curves.** The synthetic reference BEP is about 2.862 L/s.
The assumed reference-speed operating band is approximately 1.860–3.864 L/s.
The uncontrolled hydraulic intersection is 4.03456 L/s at 15.5835 m, outside
that band despite satisfying the head balance. Existence of an intersection
does not establish an acceptable equipment duty.

**Energy accounting.** At that intersection the water receives 615.55 W,
the pump shaft requires 1061.38 W, and electrical input is 1228.45 W after
motor and drive efficiencies of 0.90 and 0.96. Their identity is
$615.55=0.57995(1061.38)$ W. Running 4000 h uses about **4913.81 kWh of
electricity**. This replaces the old constant-70%-efficiency shaft-energy
estimate; the former 3517 kWh figure is not the electrical result in this edition.

**Shutoff and domain.** At zero flow the synthetic shaft input is 900 W,
but hydraulic output and efficiency are zero: the input is not useful delivery.
Shutoff is not an allowed continuous duty here. Negative head beyond the
curve's runout would be extrapolation outside the model, so performance
calculations reject it. None of the supplied performance curves or operating
limits is measured manufacturer data; those would be needed for a real selection.
''', r'''
**Fair comparison.** Each pipe delivers exactly 3 L/s and 43200 m³/year.
Speed is adjusted to match system head rather than leaving each candidate
at a different uncontrolled throughput. The required speeds for 50, 65 and
80 mm are approximately 0.9055, 0.8299 and 0.8103. All three pass the
assumed speed and per-pump BEP-band checks at the default duty.

**Energy and efficiency.** The respective pump efficiencies are 73.94%,
69.11% and 67.22%; electrical inputs are 887.37, 691.02 and 645.32 W.
Annual electricity use is 3549.47, 2764.07 and 2581.29 kWh, or
0.082164, 0.063983 and 0.059752 kWh/m³. The 80 mm pipe minimizes
electricity among the three candidates at this fixed duty.

**Why is efficiency lower in the larger pipe?** Lower loss allows lower speed.
At unchanged delivery, that changes Q/s and moves the pump relative to the
scaled BEP. At the 50 mm candidate's speed, the BEP is about 2.59 L/s;
the actual 3 L/s point is to its right but within the assumed band. Lower
friction therefore does not automatically imply higher pump efficiency.
Here electrical demand still falls because the reduction in required hydraulic
head outweighs the efficiency reduction.

**Provisional selection.** I keep the default 50 mm candidate for the subsequent
cost comparison, while recording that 80 mm is the energy-only preference.
This is not an energy optimum at 50 mm: it is an explicit distinction between
capacity feasibility, minimum electricity and the economic criterion considered next.
''', r'''
**Cost criterion.** Over ten undiscounted years at €0.20/kWh, installed pipe
plus electricity totals are about €13098.94 for 50 mm, €14028.14 for
65 mm and €17162.57 for 80 mm. All are screened feasible, so the **50 mm
pipe is the least-cost choice** under these inputs. The 80 mm pipe remains
the least-electricity choice. Those are different objectives.

**Price sensitivity and payback.** At €0.10/kWh, 50 mm still wins; at
€0.40/kWh, 65 mm wins. At the default price the 50-to-65 mm upgrade saves
about 785.40 kWh/year, or €157.08/year, against €2500 additional pipe
cost: simple payback is about **15.92 years**, longer than the ten-year horizon.
The 65-to-80 mm upgrade pays back in about 95.74 years; the direct
50-to-80 mm upgrade in about 30.99 years. These are undiscounted paybacks,
not investment returns. Infeasible candidates must be excluded regardless of cost.

**Robustness.** The selected default 50 mm pipe stays within the assumed
speed and operating band throughout the supplied roughness sweep at fixed
3 L/s. Increasing roughness requires more head and a revised speed;
the flow is held by control rather than allowed to drift. Check both limits
after every such adjustment, not simply the increase in electrical power.

**Limits of the cost result.** Pipe costs and electricity price are illustrative.
Common pump/drive purchase cost is excluded only for this same-pump comparison.
Real installation quotes, finance/discounting, maintenance, availability,
motor/drive efficiency maps, ageing and validated pump data could change the
choice. These totals are a teaching lifecycle comparison, not procurement estimates.
''', r'''
**Duty A: 6 L/s, 12 m rise.** Two parallel pumps are the only feasible
arrangement among the supplied choices. Each carries 3 L/s at speed ratio
0.8413 and about 70.07% pump efficiency. Both motors together require
**1436.91 W electrical**, or **0.066523 kWh/m³**. The single and series
options require speeds above 1.1 and also miss the assumed per-pump band.
Their printed powers are extrapolated screening calculations at rejected speeds,
not permissible operating recommendations.

**Duty B: 3 L/s, 55 m rise.** Two series pumps are the only screened-feasible
arrangement. Each carries the full 3 L/s, shares the required total head equally,
and runs at speed ratio 1.0171 with efficiency about 76.45%. Total electrical
input is **2479.49 W**, or **0.229583 kWh/m³**. A single pump requires
speed 1.3159, and the parallel pair requires 1.2159; both exceed the stated limit.

**Connection laws and energy.** Series pumps carry the same stream sequentially,
so their energy additions per unit weight add. Parallel pumps connect between
common suction and discharge headers, so head is shared and branch flows add.
The identical-pump assumption gives equal sharing here. In both arrangements,
sum both shaft inputs and both motor/drive losses. A useful total check is
$\rho gQH_{system}=\sum P_{hydraulic,pump}$.

**Why not twice the free flow?** At speed 1 in the original 65 mm line, one
pump gives 4.0346 L/s and two parallel pumps give 6.9196 L/s, less than
8.0691 L/s. Larger total flow raises system losses, so the new intersection
does not simply double. These uncontrolled points illustrate intersection
geometry; they are not approvals of the per-pump operating ranges.

**Before specifying a pair.** Check NPSH at each suction, casing and discharge
pressure ratings (especially the second series pump), individual motor ratings,
header and valve losses, reverse flow/check valves, controls and transients.
The illustrative pipe-cost comparison cannot rank these paired installations:
their extra pump, motor, control and connection costs were not supplied.
''']

FLOW_ANSWERS = {
    'prediction': 'I expect larger pipes to reduce hydraulic losses, but the least-electricity '
                  'choice need not minimize total cost. Higher flow and higher static head '
                  'will test different pump arrangements.',
    'tasks': [('',text) for text in FLOW_DISCUSSIONS],
    'warmup': ('The smaller pipe increases velocity and both loss contributions. '
               'The total K = 8 remains the same supplied case value.', '''
        for D,q in [(.065,.003),(.050,.003),(.050,.004)]:
            v = 4*q/(np.pi*D**2)
            print(f"D={D*1000:.0f} mm, Q={q*1000:.1f} L/s: v={v:.3f} m/s, fittings={8*v*v/(2*9.81):.3f} m, total head={h.system_head(q,D,120,12,4.5e-5,8):.3f} m")
        '''),
    'recommendation': '''For the base duty of exactly 3 L/s, I recommend carrying
the 50 mm line and a single variable-speed pump at speed ratio about 0.9055
forward for further review. It meets the assumed speed and per-pump flow-band
limits and minimizes the supplied ten-year pipe-plus-electricity cost. This
recommendation is specific to the illustrative prices and constant operating duty.

At fixed delivery, the 50 mm option requires about 887.37 W electrical and
3549.47 kWh/year for 4000 operating hours. The 65 and 80 mm alternatives use
2764.07 and 2581.29 kWh/year, so increasing diameter does save electricity.
However, installed pipe plus ten-year energy costs are about €13099, €14028
and €17163 at €0.20/kWh. The larger pipes do not recover their additional
cost within this horizon. At €0.40/kWh the 65 mm option becomes preferable,
so the energy-price assumption is material.

The comparison uses equal annual delivery of 43200 m³, rather than rewarding
low-power candidates that pump less water. Efficiency is derived from the
synthetic head and shaft-power curves, and electrical input includes separate
motor and drive losses. The original full-speed 65 mm hydraulic intersection
is outside the assumed recommended band; satisfying the head balance alone
is therefore insufficient. The selected 50 mm fixed-duty candidate remains
screened feasible over the stated roughness range.

For the changed high-flow duty, 6 L/s against 12 m elevation, I recommend
the parallel pair for further assessment: it is the only screened-feasible
arrangement and uses about 1.437 kW electrical in total. For the high-head
duty, 3 L/s against 55 m rise, the series pair is the only screened-feasible
choice, using about 2.479 kW. These are distinct duties, not additional
operating points that the base single-pump system is assumed to meet.

Before purchase, obtain tested pump performance and NPSH data, actual operating
limits, motor ratings, suction conditions and pressure ratings. Include connecting
pipe losses and suitable paired-pump controls. Obtain actual installation costs
and evaluate maintenance, discounting and variable load profiles. The synthetic
curves, assumed band and simplified cost model support an internally consistent
design exercise; they do not establish a verified installation or an economic
optimum across all commercially available equipment.''',
    'extension': ('''With a fixed-speed pump, a throttling valve adds resistance
until the system curve intersects the pump curve at the desired flow. The valve
dissipates excess head. At 3 L/s the full-speed pump supplies 26.5 m; a
lower-loss pipe does not by itself change that pump's head or shaft input at
the same flow. It mainly changes the valve loss needed. Speed control can
instead reduce supplied head and power, which is why the core lab specifies
it. Compare actual power curves and controls at equal delivery rather than
assuming the same savings apply to both control methods.''','''
        flow = .003
        full_speed = h.performance(flow)
        for D in [.05,.065,.08]:
            required_head = h.system_head(flow,D,120,12,4.5e-5,8)
            valve_loss = float(full_speed['head']-required_head)
            print(f"D={D*1000:.0f} mm: extra valve head={valve_loss:.3f} m; fixed-speed electrical input={full_speed['electrical']:.2f} W")
        ''')
}
