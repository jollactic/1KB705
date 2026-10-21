"""Answers for the added constrained-design core challenges in Labs 2–4."""

EXTRA_DISCUSSION = {
 'lab_02_heat': r'''
**Core challenge: compare the same delivered service.** At the default fouling
resistance, the 8.13059 m² unit recovers 142.159 kW and needs 25.041 kW
of trim heating to supply the required 167.2 kW service. At 4000 h/year,
that is about 100164 kWh/year of backup electricity. The 11.30152 m² unit
recovers essentially the full target duty and needs no meaningful trim heat;
the microscopic printed deficit is rounding of the supplied area. The 14 m²
unit can recover about 183.136 kW, more than the required service, and needs
control/bypass rather than a fictitious negative heater demand.

**Choice and rejection.** At €0.10/kWh over ten years, the respective
exchanger-plus-backup totals are approximately €109856, €11911 and €13800.
I choose 11.30152 m² for the stated default fouling condition. The cheapest
exchanger to install, 8.13059 m², is far from the cheapest way to provide
the same delivered service once its heat deficit is supplied electrically.
The 14 m² option adds cost without a credited benefit under this duty.

**Changed condition.** With zero added resistance, the smallest exchanger
already supplies the target and is cheapest. At resistance 0.001 m² K/W,
14 m² becomes the preferred supplied candidate. Thus the fouling allowance
and cleaning policy can change the equipment choice. This model omits backup
heater purchase cost, exchanger pumping power, cleaning costs and discounting;
its ranking is conditional on those omissions and the stated control assumptions.
''',
 'lab_03_distillation': r'''
**Core challenge: choose only among eligible policies.** At the default feed,
R/Rmin = 1.1 and 1.5 fail the 8 m active-height limit: they need 12.15
and 8.55 m respectively. Ratio 3.0 has the fewest stages but requires
224.72 kmol/h vapour, exceeding the 190 kmol/h limit. Ratios 1.8, 2.0
and 2.2 pass both supplied limits. Of these, **1.8** is least-cost in the
given model: R = 2.43377, 11 full ideal stages, 16 trays, 7.2 m active
height, V = 152.612 kmol/h and approximate reboiler duty 1271.77 kW.
Installed cost plus ten-year heat is about €1662271. Ratio 2.0 retains
the same integer tray count while increasing heat input, so it offers no
benefit in this particular comparison. Ratio 2.2 saves trays but costs more overall.

**Changed feed.** At 120 kmol/h, product flows and vapour circulation rise
by 20% at a fixed reflux ratio. The 1.8 policy still passes with the same
ideal stage count and 7.2 m active height, but V rises to 183.134 kmol/h;
capacity margin falls to 6.866 kmol/h. Ratio 2.0 now exceeds capacity at
197.557 kmol/h. The chosen policy need not change, but its operating margin
does. Lowering to 1.5 would reduce circulation but violate the height limit.

**Interpretation.** Minimum heat and minimum stage count are not independent
selection rules: both constraints must be met. The heat estimate assumes equal
latent heats and negligible sensible changes; it is not a measured-mixture
enthalpy calculation. The supplied V limit is not a flooding correlation.
Vendor hydraulics, real enthalpies, cooling duty, equipment costs and utility
prices are required before treating the chosen candidate as an actual column design.
''',
 'lab_04_absorption': r'''
**Core challenge: the nominal candidate does not pass the robust height screen.**
At L = 148.5 kmol/h, the adverse minimum is 162 kmol/h, so the lowest
circulation policy is infeasible even with unlimited height. At 202.5 kmol/h,
absorption remains possible, but six adverse-case contacts require 7.2 m
at HETP = 1.2 m and exceed the 6 m active-height limit.

**Selected design.** At **243 kmol/h**, or 1.8 times nominal Lmin, the
model gives four nominal and five adverse-case contacts. Conservative packed
height is 6.0 m and the illustrative ten-year total is **€201800**. It is
the least-cost eligible candidate in the supplied table. At 270 kmol/h,
height falls to 4.8 m but total cost rises to €210800. At 337.5 kmol/h,
height is only 3.6 m, but total cost is €244100. Minimum height therefore
does not minimize this cost model: additional solvent service can outweigh
the installed-height saving.

**Margin and evidence.** The selected 6 m height exactly meets the assumed
limit; it has no additional allowance for worse HETP, equilibrium or distribution.
If the actual HETP exceeds 1.2 m, this selection may fail, and a higher solvent
rate or revised geometry may be needed. Obtain packing-specific transfer data
and wet capacity/pressure-drop curves before accepting it. The annual service
allowance is an assumed circulation-cost model, not a prediction of regeneration
heat or a wet hydraulic assessment. The nominal five-contact baseline is useful
for comparison but is not the final robust candidate under these new constraints.
'''
}

RECOMMENDATION_OPENINGS = {
 'lab_02_heat': '''For the default fouling allowance, I recommend carrying forward
an exchanger of about 11.30152 m², delivering 1 kg/s water at 55 °C with
negligible normal trim heating at that condition. The supplied comparison gives
about €11911 over ten years for exchanger installation plus backup electricity,
compared with about €109856 for the clean-sized unit with continuous trim heat.
This is a same-service comparison, not simply a comparison of recovered kilowatts.
At a larger fouling allowance of 0.001 m² K/W, I would review the 14 m²
candidate instead. The following thermal checks refer to the default case.''',
 'lab_03_distillation': '''For the added height/capacity challenge, I recommend
R/Rmin = 1.8, or R = 2.43377, among the six supplied policies. It meets
the 8 m active-height and 190 kmol/h vapour limits with 16 trays, 7.2 m
active height and 152.612 kmol/h vapour at the 100 kmol/h feed. It is the
least-cost feasible policy in the illustrative ten-year heat/capital comparison.
At 120 kmol/h feed it still passes, but vapour margin falls to 6.866 kmol/h.
This constrained recommendation refines the earlier R = 2.5 baseline, whose
balance and stage checks remain useful reference calculations below.''',
 'lab_04_absorption': '''For the added robust-height challenge, I recommend
243 kmol/h solvent, or 1.8 times the nominal minimum, as the preferred
candidate for review. It needs four nominal and five adverse-case contacts,
giving 6 m active packed height at HETP = 1.2 m and an illustrative
ten-year total of €201800. This exactly meets the height limit and needs
vendor validation; it is not a margin beyond that limit. The original
202.5 kmol/h baseline fails the adverse height screen. The following nominal
balance and tray/packing comparisons describe that original baseline, not a
claim that its height satisfies the new robust requirement.'''
}
