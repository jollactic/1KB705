"""Rebuild the authored student notebooks (requires nbformat)."""
from pathlib import Path
import inspect
import textwrap
import nbformat as nbf
from teaching_materials import system_diagram, EXAMPLES, GUIDANCE
from design_materials import apply_design_version
from lab_inputs import MAIN_INPUTS

ROOT = Path(__file__).parent
SELECTED_LAB = None
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lab',help='Build only this lab folder')
    SELECTED_LAB = parser.parse_args().lab

def write_lab(folder, title, intro, theory, starter, tasks, extension):
    if SELECTED_LAB and folder != SELECTED_LAB:
        return
    theory = inspect.cleandoc(theory) + '\n\n' + MAIN_INPUTS[folder]
    path = ROOT / folder
    path.mkdir(exist_ok=True)
    # cleandoc handles a heading on the opening line followed by indented text.
    md = lambda s: nbf.v4.new_markdown_cell(inspect.cleandoc(s))
    code = lambda s: nbf.v4.new_code_cell(textwrap.dedent(s).strip())
    cells = [md(f'# {title}\n\n{intro}'), md('''
    **Time budget: 6 hours, including a short break and submission.** Work in pairs,
    but both partners must be able to explain every figure and calculation.
    Prerequisites: material and energy balances, algebra, basic Python arrays and plots.
    Use SI units unless explicitly stated. All case data are synthetic teaching values,
    not measurements or validated equipment specifications.

    Submit this notebook with outputs and a short engineering recommendation (300–500 words).
    Include assumptions, a labelled flowsheet, equations, units, balance checks,
    at least one sensitivity plot, and a discussion of model limitations.
    Optional extensions are outside the six-hour budget.
    '''), md('''
    ## 1. Setup and prediction — 30 minutes
    Before computing, sketch the apparatus and predict which parameter most strongly
    affects its size or energy demand. Explain your reasoning in two sentences.

    Locally, place `helpers.py` beside this notebook and install the root requirements.
    In Colab, upload both files using the Files panel. Alternatively, after the repository
    is published, set `HELPER_URL` below to the raw GitHub URL of this lab's `helpers.py`.
    Use a commit SHA in the URL for reproducible teaching. Only download code from a
    repository you trust. Each lab needs only its own helper file.
    '''), code('''
    from pathlib import Path
    from urllib.request import urlretrieve

    HELPER_URL = ""  # e.g. https://raw.githubusercontent.com/OWNER/REPO/COMMIT/lab_01_flow/helpers.py
    if not Path("helpers.py").exists():
        if not HELPER_URL:
            raise FileNotFoundError("Upload this lab's helpers.py or set HELPER_URL, then rerun.")
        urlretrieve(HELPER_URL, "helpers.py")

    import numpy as np
    import matplotlib.pyplot as plt
    import helpers as h
    '''), md(theory), code(starter)]
    diagram = md('''## See the whole system

![Connected equipment and labelled streams](attachment:system.png)

Schematic only: equipment sizes, heights and pipe lengths are not to scale.
Trace each stream with your finger. Identify what enters, what leaves, and where
energy is added or removed. Match the labels to the variables in the model below.
''')
    diagram['attachments'] = {'system.png': {'image/png': system_diagram(folder)}}
    # Keep setup first; then system view, theory, a small worked case and the main case.
    cells.insert(-2, diagram)
    explanation, example_code, modification = EXAMPLES[folder]
    cells[-1:-1] = [md(explanation), code(example_code),
                   md('**Try a small change:** ' + modification + '\n\n'
                      'Spend about 20 minutes on this example within the model-development '
                      'time below. Predict → run → explain. Then move to the main case.'),
                   md('### Main design case\n\nThe next cell defines the larger case used in the assessed tasks. '
                      'Example variables use `ex_` so you can rerun them without changing this case.')]
    for index, (title_, prompt, hint) in enumerate(tasks):
        cells += [md(f'## {title_}\n\n{prompt}\n\n{GUIDANCE[index]}'), code(hint), md('**Your interpretation:** Replace this text with your reasoning, units, and evidence.')]
    cells += [md('''
    ## 6. Engineering recommendation and submission — 45 minutes
    Choose a design and support it with numbers. State what would need measuring before
    using it in practice. Check your balances and inspect every axis label and unit.
    Restart the kernel and run all completed cells in order before submission.

    **Peer check:** Ask your partner to explain one equation, one numerical check,
    and one reason the model could fail. Record any revision this discussion prompted.
    '''), md('## Optional extension\n\n' + extension)]
    nb = nbf.v4.new_notebook(cells=cells, metadata={'kernelspec': {'display_name':'Python 3','language':'python','name':'python3'}, 'language_info':{'name':'python','version':'3.9'}})
    nb = apply_design_version(nb, folder, md, code)
    if folder == 'lab_01_flow':
        from flow_workshop import adapt_flow_notebook
        nb = adapt_flow_notebook(nb, md, code)
    else:
        from workshop_extensions import enrich_workshop
        nb = enrich_workshop(nb, folder, md, code)
    nbf.write(nb, path / 'lab.ipynb')

write_lab('lab_01_flow', 'Lab 1 — Pipe flow and pump selection',
    'Design a water-transfer line between two open tanks. Select a pipe and pump operating speed, then defend the energy implications.',
    r'''## Model and assumptions

    Steady, incompressible, isothermal flow; large open tanks; negligible tank velocities.
    $v=4Q/(\pi D^2)$, $Re=\rho vD/\mu$.
    Use the **Darcy** friction factor (four times the Fanning factor):
    $H_s=\Delta z+(fL/D+\sum K)v^2/(2g)$.
    For this teaching case, the **combined dimensionless loss coefficient for
    the bends and valves has been determined to be $\sum K=8$**, referenced to
    the mean velocity in the connecting pipe. This is a supplied case value,
    not the number of fittings. Their total head loss is
    $h_{\mathrm{fittings}}=(\sum K)v^2/(2g)=8v^2/(2g)$, in metres of fluid.
    It is added to the straight-pipe friction loss and the static elevation rise.
    Laminar: $f=64/Re$. For turbulent flow the helper uses the explicit Haaland
    approximation. The transition region 2300–4000 is deliberately rejected: flag
    those cases instead of silently applying a correlation.
    The illustrative pump curve is $H_p=s^2H_0-aQ^2$, with speed ratio $s$.
    The supplied equation represents an illustrative pump characteristic. Real
    pump characteristics are normally obtained from manufacturer test data; a
    fitted equation can then be used for numerical calculations. Here, $H_0=40$
    m and $a=1.5\times10^6$ s²/m⁵ are synthetic teaching values, not a fit to
    measurements from a particular pump. Use $Q$ in m³/s. The speed ratio is
    $s=N/N_0$; the speed dependence follows approximate pump affinity scaling.
    Hydraulic power is $\rho gQH$ and shaft power is hydraulic power divided by efficiency.
    This curve is a teaching model; it does not establish NPSH margin or a safe pump envelope.
    ''', '''
    rho, mu, g = 998.0, 1.0e-3, 9.81
    length, rise, roughness, K = 120.0, 12.0, 4.5e-5, 8.0
    # K is the determined total for bends and valves (dimensionless), not their count.
    diameter = 0.065
    H0, a, efficiency = 40.0, 1.5e6, 0.70  # a has units s²/m⁵
    Q = np.linspace(0.001, 0.007, 150)  # m³/s
    system = h.system_head(Q, diameter, length, rise, roughness, K, rho, mu)
    plt.plot(Q * 1000, system, label="System")
    plt.plot(Q * 1000, h.pump_head(Q, H0, a), label="Pump")
    plt.xlabel("Flow / L s$^{-1}$"); plt.ylabel("Head / m"); plt.legend(); plt.grid()
    ''', [
    ('2. Build and check the model — 75 minutes', 'Derive the system-head expression from Bernoulli. Calculate velocity, Reynolds number, friction factor, pipe loss and fitting loss at 3 L/s. Verify the helper against your hand calculation. Explain the difference between pressure and head. Check the zero-flow limit without calling the friction correlation at Re = 0.', '# TODO: calculate and print each contribution, with units.'),
    ('3. Find the operating point — 90 minutes', 'Find the pump/system intersection using bisection on a sign-changing bracket. Implement the bisection yourself and stop when the head mismatch is below 0.001 m. Check that a root exists before iteration. Compute shaft power and annual energy for 4000 operating hours. Does the flow exceed the required 3 L/s?', '# TODO: implement residual(Q), bracket it, then bisect.'),
    ('4. Compare designs — 75 minutes', 'Repeat for diameters 0.050, 0.065 and 0.080 m and speed ratios 0.8, 1.0 and 1.1. Tabulate operating flow and shaft power. Reject designs below 3 L/s. Compare energy per cubic metre as well as total power; explain why comparing power alone can mislead when throughput differs.', '# TODO: loop over designs; plot flow and specific energy.'),
    ('5. Uncertainty and break — 45 minutes', 'Take a 10-minute break. For your chosen design vary roughness from 1e-6 to 2e-4 m and efficiency from 0.55 to 0.80. Identify which assumption changes the recommendation most. Describe what additional data a real pump selection needs.', '# TODO: sensitivity study and limiting-case checks.')],
    'Add a second pump in parallel by combining flows at equal head. Compare its operating point with twice the single-pump flow.')

write_lab('lab_02_heat', 'Lab 2 — Heat recovery with a countercurrent exchanger',
    'Recover heat from a warm process stream to preheat water. Size an exchanger and predict how fouling changes its performance.',
    r'''## Model and assumptions

    Steady operation, no heat loss or phase change, constant heat capacities and overall
    heat-transfer coefficient; ideal countercurrent flow, so the LMTD correction factor is 1.
    For the main case, assume the clean overall coefficient is
    $U_{clean}=650$ W/(m² K), based on heat-transfer area. It is a supplied
    teaching value, not inferred from the inlet temperatures. Added fouling
    resistance is introduced explicitly in the design comparison.
    $C_h=\dot m_hc_{p,h}$, $C_c=\dot m_cc_{p,c}$, and
    $\dot Q=C_h(T_{h,in}-T_{h,out})=C_c(T_{c,out}-T_{c,in})$.
    $\Delta T_1=T_{h,in}-T_{c,out}$, $\Delta T_2=T_{h,out}-T_{c,in}$.
    $\Delta T_{lm}=(\Delta T_1-\Delta T_2)/\ln(\Delta T_1/\Delta T_2)$ and
    $A=\dot Q/(U\Delta T_{lm})$. Both terminal differences must be positive.
    For a fixed area use effectiveness–NTU to predict new outlets, rather than keeping
    the design duty fixed. Resistances below refer to the same heat-transfer area.
    ''', '''
    mh, mc = 1.2, 1.0  # kg/s
    cph, cpc = 3800.0, 4180.0  # J/(kg K)
    Thi, Tci, Tco_target = 85.0, 15.0, 55.0  # °C; differences are K
    Ch, Cc = mh*cph, mc*cpc
    U_clean = 650.0  # W/(m² K), assumed
    duty = Cc * (Tco_target - Tci)
    Tho = Thi - duty / Ch
    delta_lm = h.lmtd(Thi-Tco_target, Tho-Tci)
    area = duty / (U_clean * delta_lm)
    print(f"Duty: {duty/1000:.1f} kW; hot outlet: {Tho:.2f} °C; area: {area:.2f} m²")
    ''', [
    ('2. Balance and feasibility — 75 minutes', 'Draw a flowsheet and derive the two energy balances. Independently reproduce the starter values. Compute the thermodynamic maximum duty and effectiveness. Plot the two terminal temperature pairs against normalized position (connect them only as a schematic). Explain why a cold outlet above the hot outlet can be possible in countercurrent operation.', '# TODO: balance residual, maximum duty and schematic.'),
    ('3. Size and verify — 90 minutes', 'Implement the countercurrent effectiveness–NTU equation yourself using the formula in h.countercurrent_effectiveness.__doc__. Recover both outlet temperatures from the calculated area. Compare against the LMTD design. Test equal capacity rates and very small/large NTU. Discuss why the equal-capacity limit needs special treatment.', '# TODO: independent effectiveness calculation and outlet prediction.'),
    ('4. Fouling and design choice — 75 minutes', 'For added fouling resistance 0 to 0.001 m² K/W, use 1/U_f = 1/U_clean + R_f. Keep the installed area fixed and predict outlet temperatures. Plot recovered duty and cold outlet against resistance. Find the area required to meet 55 °C at R_f = 0.0006 m² K/W. Compare a clean-sized and a fouling-sized exchanger.', '# TODO: use h.outlets for fixed-area predictions.'),
    ('5. Sensitivity and break — 45 minutes', 'Take a 10-minute break. Vary cold mass flow from 0.5 to 1.8 kg/s at fixed installed area and assumed U. Discuss the tradeoff between outlet temperature and recovered heat. Explain why holding U constant may be questionable and which hydraulic calculation is missing.', '# TODO: parameter sweep and engineering interpretation.')],
    'Introduce a heat-loss term and determine what additional measurements would be needed to distinguish fouling from heat loss.')

write_lab('lab_03_distillation', 'Lab 3 — Binary distillation and ideal stages',
    'Design a teaching-model binary distillation column, using graphical stepping and a numerical stage counter. Explore the cost of demanding higher purity.',
    r'''## Model and assumptions

    Binary mixture, constant relative volatility $\alpha=2.4$, constant molar overflow,
    saturated-liquid feed ($q=1$), total condenser and equilibrium partial reboiler.
    These assumptions define a hypothetical mixture; they are not property data for a real pair.
    $y^*(x)=\alpha x/[1+(\alpha-1)x]$.
    Overall/component balances give $D=F(z_F-x_B)/(x_D-x_B)$ and $B=F-D$.
    Rectifying line: $y=Rx/(R+1)+x_D/(R+1)$. For $q=1$ the feed line is vertical
    at $x=z_F$. The stripping line joins the rectifying/feed intersection to $(x_B,x_B)$.
    Starting at $(x_D,x_D)$, step horizontally to equilibrium and vertically to the
    appropriate operating line. Use the rectifying line for $x\ge z_F$.
    Count the final equilibrium step reaching $x\le x_B$ as one full stage (conservative
    integer convention). This includes a partial reboiler and excludes the total condenser.
    ''', '''
    F, zF, xD, xB, alpha = 100.0, 0.45, 0.95, 0.05, 2.4  # F in kmol/h
    R = 2.5
    x = np.linspace(0, 1, 400)
    rect, strip = h.operating_lines(zF, xD, xB, R)
    plt.plot(x, h.equilibrium(x, alpha), label="Equilibrium")
    plt.plot(x, x, color="grey", label="Diagonal")
    plt.plot(x[x>=zF], rect(x[x>=zF]), label="Rectifying")
    plt.plot(x[x<=zF], strip(x[x<=zF]), label="Stripping")
    plt.axvline(zF, linestyle=":", color="grey")
    plt.xlabel("Liquid mole fraction x"); plt.ylabel("Vapour mole fraction y")
    plt.legend(); plt.grid()
    ''', [
    ('2. Material balances and minimum reflux — 75 minutes', 'Calculate D and B and verify both balances. For a saturated-liquid feed, use the equilibrium point at zF and the distillate point to find the pinched rectifying-line slope and hence R_min. Show the construction on your plot. Explain why R = R_min cannot deliver a finite stage count in this model.', '# TODO: derive slope_min and R_min; print balance residuals.'),
    ('3. Graphical and numerical stages — 90 minutes', 'Draw the first three horizontal/vertical steps manually on the diagram. Implement a numerical stage counter using h.inverse_equilibrium. Store and plot every step. Stop when x <= xB, reject non-progressing steps, and impose a maximum of 300 steps. Compare your result with h.stage_count and document the feed-stage switch and reboiler convention.', '# TODO: write your own stepping loop and overlay the staircase.'),
    ('4. Reflux and purity tradeoffs — 75 minutes', 'Sweep R/R_min = 1.1 to 3.0. Plot full ideal stages and a vapour-load proxy V=(R+1)D. At R/R_min=1.5 compare xD = 0.90, 0.95 and 0.98, recalculating balances and R_min each time. Explain why vapour flow is only an energy proxy and cannot establish a monetary optimum.', '# TODO: stage and vapour-load sweep; handle infeasible cases explicitly.'),
    ('5. Real trays and break — 45 minutes', 'Take a 10-minute break. For the base case, convert ideal trays to installed trays using overall tray efficiency E_o = 0.50, 0.65 and 0.80: ceil((N_ideal-1)/E_o). The reboiler is excluded from the tray conversion. Estimate active height using 0.45 m spacing times installed tray count. Explain the difference between overall and Murphree efficiency and the omitted height allowances.', '# TODO: table of installed trays and active heights.')],
    'Replace constant relative volatility with instructor-supplied equilibrium data; interpolate monotonically and compare stage counts.')

write_lab('lab_04_absorption', 'Lab 4 — Gas absorption and column height',
    'Remove a dilute solute from a gas using a countercurrent solvent. Connect material balances, ideal stages, efficiency and a hydraulic screening calculation.',
    r'''## Model and assumptions

    Isothermal, dilute, nonreacting absorption with constant solute-free gas and solvent
    flow rates $G_s,L_s$ (kmol/h). Use mole ratios $Y=y/(1-y)$ and $X=x/(1-x)$.
    Assume the hypothetical equilibrium relation $Y^*=mX$, with $m=1.5$.
    The operating line is $Y=Y_{out}+(L_s/G_s)(X-X_{in})$.
    Balance: $L_s(X_{out}-X_{in})=G_s(Y_{in}-Y_{out})$.
    For this linear case, $L_{min}/G_s=(Y_{in}-Y_{out})/(Y_{in}/m-X_{in})$.
    Starting at $Y_1=Y_{out}$, equilibrium gives $X_n=Y_n/m$ and the balance gives
    $Y_{n+1}=Y_{out}+(L_s/G_s)(X_n-X_{in})$. Stop once $Y_{n+1}\ge Y_{in}$.
    Count the last stage in full. Ideal stages describe equilibrium contacts, not packing height.
    For trays use an assumed overall efficiency; for packing use an independently supplied
    HETP. Neither can be inferred from equilibrium data alone.
    ''', '''
    Gs, Yin, Yout, Xin, m = 100.0, 0.03, 0.003, 0.0, 1.5
    Lmin = Gs*(Yin-Yout)/(Yin/m-Xin)
    Ls = 1.5*Lmin
    Xout = Xin + Gs/Ls*(Yin-Yout)
    print(f"Minimum solvent: {Lmin:.2f} kmol/h; selected: {Ls:.2f} kmol/h")
    X = np.linspace(0, Yin/m*1.1, 200)
    plt.plot(X, m*X, label="Equilibrium")
    plt.plot(X, Yout+Ls/Gs*(X-Xin), label="Operating line")
    plt.xlabel("Liquid mole ratio X"); plt.ylabel("Gas mole ratio Y")
    plt.legend(); plt.grid()
    ''', [
    ('2. Balance and feasibility — 75 minutes', 'Convert inlet and outlet gas ratios to mole fractions. Calculate solvent outlet composition and solute removal in kmol/h. Verify the solute balance. Derive L_min from the bottom pinch and explain why the selected flow must exceed it. Check the driving force at both column ends.', '# TODO: balance, mole fractions and pinch construction.'),
    ('3. Count ideal stages — 90 minutes', 'Implement the recurrence above and plot the staircase: start at (Xin,Yout), step horizontally to equilibrium, then vertically to the operating line. Include a non-progress check and 300-stage cap. Compare with h.stage_count. Sweep L/L_min from 1.05 to 2.5 and show how solvent demand trades against stage count.', '# TODO: independent stage counter, staircase and solvent sweep.'),
    ('4. Height and hydraulic screening — 75 minutes', 'At the base case compare a tray column with overall efficiency 0.60 and tray spacing 0.45 m against packing with assumed HETP 0.6–1.2 m. Report active heights separately. For packing, use area 1.0 m², gas volumetric flow 0.8 m³/s, void fraction 0.70, equivalent particle diameter 0.025 m, gas density 1.2 kg/m³ and viscosity 1.8e-5 Pa s. Evaluate h.ergun_gradient and multiply by packed height. Discuss the credibility of treating this irrigated packing as a dry bed.', '# TODO: height ranges and dry-bed pressure-drop estimates.'),
    ('5. Robustness and break — 45 minutes', 'Take a 10-minute break. Change m by ±20% at fixed selected solvent flow. Recompute the minimum solvent requirement before counting stages; label infeasible cases. Explain why the dry Ergun estimate cannot predict flooding, liquid holdup or actual wet pressure drop. List the vendor/experimental data needed to proceed.', '# TODO: equilibrium sensitivity and feasibility table.')],
    'Compare the stage model with a continuous transfer-unit model. State which additional mass-transfer coefficients and interfacial-area data are needed.')

if __name__ == '__main__':
    if SELECTED_LAB in (None,'lab_00'):
        from balances_intro import build_intro
        build_intro()
    print('Built student notebooks' + (f': {SELECTED_LAB}' if SELECTED_LAB else ': all five') + '.')
