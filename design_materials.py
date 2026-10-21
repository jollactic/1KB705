"""Design-focused prompts, editable settings and supplied numerical analyses."""
import textwrap
import ast
from design_calculations import CALCULATIONS


GUIDE = '''**How to work:** Run the supplied analysis cell, read its table and plot,
then answer the decision questions in words. If this section has a settings cell,
change only those values and rerun this section and all following sections.
No numerical routines or plotting code need to be written. A failed constraint
is a result to discuss, not something to hide. Keep units with every reported value.'''


DESIGN_TASKS = {
    'lab_01_flow': [
        ('2. Understand the energy requirement — 75 minutes',
         '''Use the supplied contribution calculation at 3 L/s. On the system diagram,
identify where the pump adds energy and where energy is dissipated. Check one
velocity or loss term with a calculator and explain pressure versus head.
Which part of the required head could a larger pipe reduce? Which part remains
even at negligible flow? Predict the effect of a smaller pipe before changing
the diameter in the settings cell. Record a prediction and the observed result.''',
         'diameter = 0.065  # m; try 0.050, then restore the base case'),
        ('3. Decide whether the base pump meets the duty — 90 minutes',
         '''Run the supplied operating-point search. Mark the operating point on
the curves and decide whether the base system meets the required throughput.
Report flow, head, annual energy and energy per cubic metre. What does the
head-residual check tell you, and what does it leave uncertain? If the requirement
changes from 3 to 4.5 L/s, would this base pump/pipe combination still qualify?
No bisection code is required: explain the physical meaning of the intersection.''',
         'required_flow_Lps = 3.0  # L/s; try 4.5\noperating_hours = 4000  # hours/year'),
        ('4. Select a pipe and pump speed — 75 minutes',
         '''Use the supplied nine-candidate table to shortlist feasible designs.
Choose a pipe diameter and speed in the settings cell, then compare your choice
with the feasible candidate using least electricity per delivered volume.
Report throughput margin and specific energy. Explain whether you would accept
a larger pipe without its purchase price, and whether a low-power design that
fails the flow requirement should remain on the shortlist. State your selection
criterion explicitly; more than one defended recommendation is possible.''',
         '''selected_diameter = 0.080  # m: choose 0.050, 0.065 or 0.080
selected_speed = 1.0  # choose 0.8, 1.0 or 1.1'''),
        ('5. Check robustness before recommending — 45 minutes',
         '''Take a 10-minute break. Run the supplied roughness and efficiency
sweeps for your selected design. Is it feasible at the worst roughness?
Which uncertainty changes specific energy most over these stated ranges?
Explain why efficiency changes power without moving the operating point in
this particular model. Name the pump and suction data you would request before
procurement. Revise your selection if its margin is inadequate.''',
         '''roughness_low = 1e-6  # m
roughness_high = 2e-4  # m
efficiency_low = 0.55
efficiency_high = 0.80''')],
    'lab_02_heat': [
        ('2. Check that the temperature target is feasible — 75 minutes',
         '''Run the supplied balance and temperature schematic. Check one duty
calculation with a calculator. Locate both terminal driving forces on the system
diagram. Is the target duty below the thermodynamic maximum? Explain why the
cold outlet may exceed the hot outlet without reversing local heat flow. Identify
the stream data you would measure to check this design in an operating plant.''', ''),
        ('3. Review the thermal design checks — 90 minutes',
         '''Run the supplied effectiveness–NTU verification. Compare its outlet
temperatures with the LMTD design. Explain the zero-transfer and large-area
limits in physical terms. Do the agreement and limiting-case checks establish
that the real exchanger will work? Identify at least two assumptions that still
need confirmation. Choose whether this design is ready for thermal review,
hydraulic review or purchase, and justify that decision.''', ''),
        ('4. Choose a fouling allowance and installed area — 75 minutes',
         '''Choose an added fouling resistance in the settings cell. Read the
fixed-area performance curves and compare a clean-sized unit with an enlarged
unit designed to meet the target at your chosen resistance. Report the added
area percentage. Would you specify the larger area or accept a lower outlet
temperature between cleanings? State the process requirement supporting your
choice. What happens when the enlarged exchanger is clean, and what control
action would be needed?''',
         'design_R = 0.0006  # m² K/W; choose between 0 and 0.001'),
        ('5. Define an operating envelope — 45 minutes',
         '''Take a 10-minute break. Use the supplied cold-flow sweep at fixed
chosen area and fouling allowance. Identify which tested flows meet the 55 °C
target, and select an operating flow or range. Explain the difference between
maximizing heat recovery and maximizing outlet temperature. What further
pressure-drop and pumping calculations must accompany your thermal decision?
State why the constant-U sweep is provisional.''',
         '''cold_flow_low = 0.5  # kg/s
cold_flow_high = 1.8  # kg/s''')],
    'lab_03_distillation': [
        ('2. Establish the separation duty and reflux limit — 75 minutes',
         '''Run the supplied material balance and pinch construction. Check one
component balance with a calculator. Identify feed, reflux, distillate and
bottoms on the system diagram. Explain why the minimum reflux is a limit rather
than a usable finite-column design. Record the product flows and the minimum
reflux needed before considering equipment choices.''', ''),
        ('3. Choose a feasible reflux and inspect the column — 90 minutes',
         '''Choose a reflux ratio above the printed minimum. The supplied routine
draws the first three contacts and the complete staircase; do not write a stage
counter. Explain the horizontal and vertical moves using one printed pair of
coordinates. Locate the operating-line switch at the feed. Report ideal stages
and state whether the condenser and reboiler are included. Compare your reflux
choice with a higher one and describe the physical tradeoff.''',
         'R = 2.5  # reflux ratio; must exceed Rmin (about 1.352 for the base case)'),
        ('4. Compare purity and operating policies — 75 minutes',
         '''Run the supplied reflux and purity comparisons. Select a preliminary
reflux policy and explain where extra reflux gives little stage reduction.
Does demanding 0.98 distillate purity appear worthwhile if the process only
requires 0.95? Use stage count, product flow and vapour load in your answer.
Explain why neither a minimum stage count nor a minimum vapour flow alone
identifies an economic optimum. List the cost and energy data needed to decide.''',
         '''reflux_ratio_low = 1.1  # R/Rmin; keep above 1
reflux_ratio_high = 3.0
purity_targets = [0.90, 0.95, 0.98]  # mole fractions, above feed composition
purity_reflux_multiple = 1.5  # compare each target at this R/Rmin'''),
        ('5. Translate ideal contacts into equipment — 45 minutes',
         '''Take a 10-minute break. Compare the supplied overall-efficiency cases.
Select an efficiency assumption for a preliminary tray-height estimate and
state what evidence would justify it. Explain the difference between overall
and Murphree efficiency. Distinguish active height from vessel height, including
at least three allowances absent from the model. Would efficiency uncertainty
change your preferred reflux policy?''',
         '''efficiency_cases = [0.50, 0.65, 0.80]
selected_tray_efficiency = 0.65
tray_spacing = 0.45  # m''')],
    'lab_04_absorption': [
        ('2. Check removal duty and solvent feasibility — 75 minutes',
         '''Run the supplied solute balance and pinch construction. Check the
removed solute flow with a calculator. Explain why mole ratios are used with
solute-free flow rates. Identify both end driving forces on the diagram and
decide whether the selected solvent rate is feasible. Report removal, rich
solvent composition and minimum solvent rate.''', ''),
        ('3. Choose a solvent rate — 90 minutes',
         '''Choose a solvent rate as a multiple of the minimum and run the
supplied staircase and solvent sweep. No recurrence or loop needs to be written.
Compare your choice with a lower and a higher rate. Recommend a provisional
solvent policy using contact count, solvent handling and margin above the pinch.
State which missing regeneration or operating-cost information could change
your decision. Explain how the final full-contact convention affects the count.''',
         'solvent_multiple = 1.5  # Ls/Lmin; keep above 1'),
        ('4. Compare internals and screen hydraulics — 75 minutes',
         '''Compare tray and packing active heights using the supplied results.
Choose a provisional internals option or explain why selection must wait.
Report the range of packed height and the dry-bed pressure-drop estimate.
Would you use that dry estimate to approve an irrigated absorber? Identify
the missing physical effects and data. Do not apply tray efficiency to a
packing height already based on HETP.''',
         '''absorber_tray_efficiency = 0.60
absorber_tray_spacing = 0.45  # m
hetp_low = 0.6  # m
hetp_high = 1.2  # m'''),
        ('5. Check the recommendation against equilibrium uncertainty — 45 minutes',
         '''Take a 10-minute break. Run the ±20% equilibrium-slope cases at your
fixed selected solvent flow. Determine whether each is feasible before reading
its stage count. Does your nominal height have adequate margin? Decide whether
to increase solvent flow, allow more height or obtain better equilibrium data.
List vendor data needed for wet pressure drop, liquid distribution and flooding
margin; explain why the dry Ergun result cannot supply them.''', '')]
}


def supplied_code(folder, index):
    """Adapt the verified reference calculations to explicit student design settings."""
    source = textwrap.dedent(CALCULATIONS[folder][index]).strip()
    if folder == 'lab_01_flow':
        if index == 1:
            source = 'system = h.system_head(Q,diameter,length,rise,roughness,K,rho,mu)\n' + source
            source = source.replace('assert base_q >= .003',
                                    'print("Meets flow requirement:", base_q*1000 >= required_flow_Lps)')
            source = source.replace('base_power/1000*4000', 'base_power/1000*operating_hours')
        if index == 2:
            source = source.replace('>=3 L/s', 'meets duty')
            source = source.replace('flow >= .003', 'flow*1000 >= required_flow_Lps')
            source = source.replace('row[2] >= .003', 'row[2]*1000 >= required_flow_Lps')
            source = source.replace('selected = min(feasible_designs, key=lambda row: row[5])\nchosen_D, chosen_speed = selected[:2]\nprint(f"Lowest specific-energy feasible candidate: D={chosen_D:.3f} m, speed={chosen_speed:.1f}")',
                                    '''if feasible_designs:
    best = min(feasible_designs, key=lambda row: row[5])
    print(f"Lowest specific-energy feasible candidate: D={best[0]:.3f} m, speed={best[1]:.1f}")
else:
    print("None of the candidates meets the requested duty")
chosen_D, chosen_speed = selected_diameter, selected_speed
chosen_result = operating_point(chosen_D, chosen_speed)
print(f"Your selection: {chosen_result[0]*1000:.4f} L/s; margin={chosen_result[0]*1000-required_flow_Lps:.4f} L/s")
print(f"Your selection: {chosen_result[3]:.6f} kWh/m³; feasible={chosen_result[0]*1000 >= required_flow_Lps}")''')
            source = source.replace('axes[0].axhline(3,', 'axes[0].axhline(required_flow_Lps,')
        if index == 3:
            source = source.replace('np.linspace(1e-6, 2e-4, 25)', 'np.linspace(roughness_low, roughness_high, 25)')
            source = source.replace('np.linspace(.55, .80, 25)', 'np.linspace(efficiency_low, efficiency_high, 25)')
            source = source.replace("axes[0].axhline(3,", "axes[0].axhline(required_flow_Lps,")
            source = source.replace('eps=2e-4)[0] >= .003', 'eps=roughness_high)[0]*1000 >= required_flow_Lps')
            source = source.replace('robust_choice = min(robust, key=lambda row: row[5])\nprint(f"Robust to stated roughness range: D={robust_choice[0]:.3f} m, speed={robust_choice[1]:.1f}")',
                                    '''if robust:
    robust_choice = min(robust, key=lambda row: row[5])
    print(f"Robust to stated roughness range: D={robust_choice[0]:.3f} m, speed={robust_choice[1]:.1f}")
else:
    print("No candidate meets the requirement at maximum roughness")''')
    elif folder == 'lab_02_heat':
        if index == 2:
            source = source.replace('design_R = .0006\n', '')
            source = source.replace('assert np.isclose(enlarged_design[1],55)', 'assert np.isclose(enlarged_design[1],Tco_target)')
            source += '\nprint(f"Area increase: {(fouled_sized_area/area-1)*100:.1f}%")'
        if index == 3:
            source = source.replace('np.linspace(.5,1.8,60)', 'np.linspace(cold_flow_low,cold_flow_high,60)')
            source += '''
meets_target = flow_results[:,1] >= Tco_target-1e-8
if np.any(meets_target):
    qualifying = cold_flows[meets_target]
    print(f"Tested flows meeting target: {qualifying.min():.3f}–{qualifying.max():.3f} kg/s")
else:
    print("No tested flow meets the outlet-temperature target")
'''
    elif folder == 'lab_03_distillation':
        if index == 1:
            source = 'rect, strip = h.operating_lines(zF,xD,xB,R)\n' + source
        if index == 2:
            source = source.replace('np.linspace(1.1,3.0,60)', 'np.linspace(reflux_ratio_low,reflux_ratio_high,60)')
            source = source.replace('for candidate_xD in [.90,.95,.98]:', 'for candidate_xD in purity_targets:')
            source = source.replace('candidate_R = 1.5*candidate_min', 'candidate_R = purity_reflux_multiple*candidate_min')
        if index == 3:
            source = source.replace('for overall in [.50,.65,.80]:', 'for overall in efficiency_cases:')
            source = source.replace('active_height = .45*actual', 'active_height = tray_spacing*actual')
            source = source.replace('assert N_ideal == 11 and tray_results[1][1] == 16',
                                    '''selected_trays = int(np.ceil(ideal_trays/selected_tray_efficiency))
print(f"Selected assumption: {selected_trays} trays; active height={selected_trays*tray_spacing:.3f} m")''')
    elif folder == 'lab_04_absorption':
        if index == 1:
            source = 'Ls = solvent_multiple*Lmin\nXout = Xin+Gs/Ls*(Yin-Yout)\n' + source
        if index == 2:
            source = source.replace('np.ceil(N_abs/.60)', 'np.ceil(N_abs/absorber_tray_efficiency)')
            source = source.replace('installed_trays*.45', 'installed_trays*absorber_tray_spacing')
            source = source.replace('np.linspace(.6,1.2,25)', 'np.linspace(hetp_low,hetp_high,25)')
        if index == 3:
            source = source.replace('assert Ls<=infeasible_min\nprint(f\'Illustrative infeasible check: m={infeasible_m}, Lmin={infeasible_min:.2f} > Ls={Ls:.2f}\')',
                                    'print(f"Extra case: m={infeasible_m}, Lmin={infeasible_min:.2f}, feasible={Ls>infeasible_min}")')
    return source


def apply_design_version(notebook, folder, md, code):
    """Replace implementation tasks with supplied analysis and open design decisions."""
    result = []
    index = 0
    for cell in notebook.cells:
        if cell.cell_type == 'markdown' and any(cell.source.startswith(f'## {n}.') for n in range(2,6)):
            heading, prompt, settings = DESIGN_TASKS[folder][index]
            cell = md(f'## {heading}\n\n{prompt}\n\n{GUIDE}')
            result.append(cell)
            if settings:
                lines = ['#@title DESIGN SETTINGS — edit values or use the Colab form']
                for line in settings.splitlines():
                    assignment, _, explanation = line.partition('#')
                    if explanation.strip():
                        lines.append('# ' + explanation.strip())
                    value = ast.literal_eval(assignment.split('=',1)[1].strip())
                    form_type = 'raw' if isinstance(value,list) else 'number'
                    lines.append(assignment.rstrip() + ' #@param {type:"' + form_type + '"}')
                setting_cell = code('\n'.join(lines))
                setting_cell.metadata['design_settings'] = index
                result.append(setting_cell)
            continue
        if cell.cell_type == 'code' and '# TODO:' in cell.source:
            cell = code('#@title SUPPLIED ANALYSIS — run as provided; no edits needed\n' + supplied_code(folder,index))
            cell.metadata['design_analysis'] = index
            cell.metadata['jupyter'] = {'source_hidden': True}
            cell.metadata['tags'] = ['supplied-analysis', 'hide-input']
            cell.metadata['source_hidden'] = True
            cell.metadata['cellView'] = 'form'  # Colab: display output while hiding the implementation
        elif cell.cell_type == 'markdown' and cell.source.startswith('**Your interpretation:**'):
            cell = md('''**Your design decision — complete in words:**

1. **Prediction / requirement:** …
2. **Evidence:** Report at least two numbers from the table or plot, with units.
3. **Decision and tradeoff:** …
4. **What could change the decision?** State an assumption or missing measurement.

You are assessed on engineering reasoning, not on writing Python.''')
            cell.metadata['design_answer'] = index
            index += 1
        result.append(cell)
    if index != 4:
        raise ValueError('Expected four design sections')
    result.insert(1, md('''## Design workshop: run → compare → decide

All numerical methods, loops, tables and plots are supplied. You only change
values in cells marked **DESIGN SETTINGS** and write your engineering decisions.
In Colab, these settings also have parameter forms. The small worked examples
may be rerun after changing the named example values; their equations are supplied.
Run each analysis as provided; its implementation is collapsed where supported
and can be expanded if you are curious. No Python programming is assessed.

Work through the notebook in order. After changing an upstream setting, rerun
that section and every section below it so results stay consistent. Restore the
printed base values to reproduce the reference case. Keep at least one rejected
design and explain why you rejected it. Each analysis table is evidence for a
decision, not a complete answer on its own.

**Time budget (six hours):** setup and system prediction 30 min; balances and
feasibility 75 min; operating policy and checks 90 min; alternative designs
75 min; robustness and break 45 min; recommendation 45 min. The supplied
worked example belongs within the feasibility block, not an extra activity.
'''))
    for cell in result:
        if cell.cell_type != 'markdown':
            continue
        cell.source = cell.source.replace('Prerequisites: material and energy balances, algebra, basic Python arrays and plots.',
                                          'Prerequisites: material and energy balances, algebra, and reading tables and plots. No Python programming is required.')
        if cell.source.startswith('## 6.'):
            cell.source += '''

**Design-review checklist:** Does your selected design meet every stated
requirement? Include its operating margin, one rejected alternative and a
numerical reason for rejection. Distinguish a model verification check from
evidence that real equipment will perform as predicted. Identify the next
measurement or vendor datum needed. No new code is required for submission.'''
        if cell.source.startswith('**Try a small change:**'):
            cell.source = cell.source.replace('Before extending the loop, add an if/else that selects the stripping line when x < zF.',
                                              'The supplied main-case analysis switches to the stripping line when x < zF; identify where this happens.')
            cell.source = cell.source.replace('Extend the loop until it reaches Yin = 0.03, checking first that solvent flow exceeds its minimum.',
                                              'The supplied main-case analysis counts all required contacts; explain why checking minimum solvent flow comes first.')
        if cell.source.startswith('## Optional extension'):
            cell.source = '''## Optional design-review extension

No coding is required. ''' + {
                'lab_01_flow': 'Would two identical parallel pumps double the delivered flow? Sketch the combined pump curve against the rising system curve and explain your answer.',
                'lab_02_heat': 'Would a low cold outlet necessarily prove fouling? Propose measurements that distinguish heat loss to the room from reduced UA.',
                'lab_03_distillation': 'What would you check before replacing the constant-volatility curve with measured equilibrium data? Explain the implications of interpolation uncertainty or an azeotrope.',
                'lab_04_absorption': 'Could equilibrium data alone establish packing height? Compare an HETP specification with a transfer-unit model and list the additional vendor data needed.'
            }[folder]
    notebook.cells = result
    notebook.metadata['teaching_variant'] = 'design-support'
    return notebook
