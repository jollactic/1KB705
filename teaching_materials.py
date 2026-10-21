"""Worked examples and portable system diagrams used by build_labs.py."""
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch


def system_diagram(folder):
    """Return a PNG attachment: diagrams travel inside the notebook, including Colab."""
    fig, ax = plt.subplots(figsize=(11, 4.7))
    fig.patch.set_facecolor('#f5f8fc')
    ax.set(xlim=(0, 11), ylim=(0, 4.7), aspect='equal')
    ax.axis('off')
    blue, orange, ink = '#1676a3', '#ce6428', '#213449'

    def text(x, y, label, size=11):
        ax.text(x, y, label, ha='center', va='center', fontsize=size, color=ink)

    def arrow(points, color=blue):
        for start, end in zip(points[:-1], points[1:]):
            ax.add_patch(FancyArrowPatch(start, end, arrowstyle='->',
                                        mutation_scale=15, lw=2.4, color=color))

    def box(x, y, w, height, label):
        ax.add_patch(Rectangle((x, y), w, height, fc='white', ec=ink, lw=1.8))
        text(x+w/2, y+height/2, label)

    text(5.5, 4.4, 'Follow the streams → write balances → choose the equipment', 14)
    if folder == 'lab_01_flow':
        # Open tanks: surface elevations are the Bernoulli endpoints.
        for x, y in [(0.5, 0.7), (8.6, 2.2)]:
            ax.plot([x, x, x+1.8, x+1.8], [y+1.1, y, y, y+1.1], color=ink, lw=2)
            ax.add_patch(Rectangle((x+.04, y+.04), 1.72, .65, fc='#c5e6f3', ec='none'))
            ax.plot([x+.04, x+1.76], [y+.7, y+.7], color=blue)
        text(1.4, 2.1, 'Tank A: open to air\nSurface 1, z₁')
        text(9.5, 3.7, 'Tank B: open to air\nSurface 2, z₂')
        ax.add_patch(Circle((3.5, 1.05), .4, fc='white', ec=ink, lw=2))
        text(3.5, 1.05, 'P')
        arrow([(2.3, 1.05), (3.1, 1.05)])
        arrow([(3.9, 1.05), (6.5, 1.05), (6.5, 2.55), (8.6, 2.55)])
        text(3.5, .3, 'Pump adds head Hₚ')
        text(6.1, 3.3, 'Pipe: L, D, roughness\nBends / valves: ΣK = 8')
        text(5.3, .55, 'Flow Q →')
        text(8.6, 1.25, 'Static rise Δz = z₂ − z₁\nPump head = rise + losses')
    elif folder == 'lab_02_heat':
        box(3.5, 1.2, 4, 2.2, 'Heat-transfer wall\nArea A; coefficient U')
        arrow([(0.5, 2.9), (3.5, 2.9)], orange)
        arrow([(7.5, 2.9), (10.5, 2.9)], orange)
        arrow([(10.5, 1.7), (7.5, 1.7)], blue)
        arrow([(3.5, 1.7), (.5, 1.7)], blue)
        text(1.8, 3.5, 'Hot inlet\nṁh, Th,in')
        text(9.2, 3.5, 'Hot outlet\nTh,out')
        text(9.2, .95, 'Cold inlet\nṁc, Tc,in')
        text(1.8, .95, 'Cold outlet\nTc,out')
        text(5.5, .35, 'Opposite stream directions: heat duty Q̇ passes through the wall')
    elif folder == 'lab_03_distillation':
        box(4.2, 1.15, 2, 2.25, 'Column\nIdeal trays')
        for y in [1.5, 2, 2.5, 3]:
            ax.plot([4.35, 4.65], [y, y], color=ink)
            ax.plot([5.75, 6.05], [y, y], color=ink)
        arrow([(.5, 2.3), (4.2, 2.3)])
        text(2, 2.9, 'Feed F, zF\nSaturated liquid: q = 1')
        box(7.1, 3.05, 1.7, .65, 'Condenser')
        arrow([(5.2, 3.4), (5.2, 3.85), (7.95, 3.85), (7.95, 3.7)], orange)
        arrow([(8.8, 3.35), (10.5, 3.35)])
        text(9.7, 2.9, 'Distillate D, xD')
        arrow([(7.1, 3.35), (6.5, 3.35), (6.5, 2.9), (6.2, 2.9)])
        text(6.95, 2.5, 'Reflux L = RD', 10)
        box(4.25, .1, 1.9, .65, 'Reboiler')
        arrow([(4.6, 1.15), (4.6, .75)])
        arrow([(5.8, .75), (5.8, 1.15)], orange)
        arrow([(6.15, .4), (9.1, .4)])
        text(8.2, .85, 'Bottoms B, xB')
        text(2.1, .5, 'Heat input → vapour', 10)
    else:
        box(4.3, 1, 2.1, 2.5, 'Absorber\nGas ↑  Liquid ↓\nTrays OR packing')
        arrow([(.6, 1.15), (4.3, 1.15)], orange)
        text(2.1, .55, 'Gas in: Gs, Yin')
        arrow([(6.4, 3.3), (10.4, 3.3)], orange)
        text(8.7, 3.85, 'Cleaned gas: Gs, Yout')
        arrow([(1.1, 3.3), (4.3, 3.3)])
        text(2.1, 3.85, 'Lean solvent: Ls, Xin')
        arrow([(6.4, 1.15), (10.4, 1.15)])
        text(8.7, .55, 'Rich solvent: Ls, Xout')
        text(8.6, 2.15, 'Solute transfers\nfrom gas to liquid')
        text(2.1, 2.15, 'Gs and Ls are\nsolute-free flow rates')
    stream = BytesIO()
    fig.savefig(stream, format='png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    return base64.b64encode(stream.getvalue()).decode('ascii')


EXAMPLES = {
    'lab_01_flow': ('''### Worked example: one pipe and one trial flow
Follow the diagram from Tank A through the pump and pipe to Tank B. The pump
must supply both the elevation rise and the losses. Start by testing **one** flow;
it is not yet the operating point. The code below prints each part separately.

**Supplied worked-example data (synthetic):**

| Quantity | Value | Meaning / units |
| --- | --- | --- |
| Trial flow | 3 L/s = 0.003 m³/s | Trial value, not a prescribed pump operating point |
| Internal pipe diameter | 0.065 m | Pipe flow area is πD²/4 |
| Pipe length / elevation rise | 120 m / 12 m | Distinct contributions to the energy balance |
| Water density / dynamic viscosity | 998 kg/m³ / 0.001 Pa s | Constant assumed water properties |
| Absolute roughness | 0.000045 m | Assumed pipe-wall roughness |
| Gravitational acceleration | 9.81 m/s² | Constant used to convert velocity to head |
| Total bend/valve coefficient | 8, dimensionless | Supplied combined K, based on pipe velocity |
| Reference pump curve | H0 = 40 m, a = 1.5 × 10⁶ s²/m⁵ | H = H0 − aQ² at speed ratio 1; synthetic |

For this case, the combined dimensionless loss coefficient for the bends and
valves has been determined to be **ΣK = 8**, based on the pipe velocity.
Thus `ex_fitting_loss = 8.0 * ex_v**2 / (2 * 9.81)` is their total head loss
in metres of fluid; 8 is a supplied coefficient, not a count of fittings.
At 3 L/s you should find a velocity near 0.904 m/s and a system head near 14.0 m.
The pump supplies 26.5 m, so the actual intersection should lie at a higher flow.
''', '''
    ex_Q = 3.0 / 1000  # convert L/s to m³/s before using SI equations
    ex_D, ex_L, ex_rise = 0.065, 120.0, 12.0
    ex_rho = 998.0  # assumed water density, kg/m³
    ex_mu = 0.001  # assumed dynamic viscosity, Pa s
    ex_roughness = 4.5e-5  # assumed absolute pipe roughness, m
    ex_g = 9.81  # gravitational acceleration, m/s²
    ex_K = 8.0  # supplied total bend/valve loss coefficient, dimensionless
    ex_H0, ex_a = 40.0, 1.5e6  # synthetic reference head curve: m, s²/m⁵
    ex_v = ex_Q / (np.pi * ex_D**2 / 4)
    ex_Re = ex_rho * ex_v * ex_D / ex_mu
    ex_f = float(h.friction_factor(ex_Re, ex_roughness / ex_D))
    ex_pipe_loss = ex_f * ex_L / ex_D * ex_v**2 / (2 * ex_g)
    ex_fitting_loss = ex_K * ex_v**2 / (2 * ex_g)  # head loss in m
    ex_required = ex_rise + ex_pipe_loss + ex_fitting_loss
    ex_available = float(h.pump_head(ex_Q, ex_H0, ex_a, speed_ratio=1.0))
    print(f"Velocity = {ex_v:.3f} m/s; Re = {ex_Re:.0f}; Darcy f = {ex_f:.4f}")
    print(f"Rise = {ex_rise:.2f} m; pipe loss = {ex_pipe_loss:.2f} m; fittings = {ex_fitting_loss:.2f} m")
    print(f"Required = {ex_required:.2f} m; pump = {ex_available:.2f} m")
    print(f"Head surplus = {ex_available-ex_required:.2f} m")
    ''', 'Copy the cell and change only ex_D to 0.050 m. Predict the direction of the loss change first. Then change the trial flow to 4 L/s. Which term changes most?'),
    'lab_02_heat': ('''### Worked example: heat a small cold-water stream
Trace the orange stream left to right and the blue stream right to left.
Use an easier target first: heat 0.5 kg/s of water from 15 to 35 °C using
1.0 kg/s of hot water entering at 70 °C. Both **specific heat capacities**
are assumed constant at 4180 J/(kg K). The heat-capacity rates C = mass flow × cp
are different: 4180 W/K hot and 2090 W/K cold.

**Assume an overall heat-transfer coefficient U = 650 W/(m² K)** for this
clean, ideal countercurrent exchanger. It represents the combined fluid-film
and wall resistance on the stated area basis; it is a supplied teaching
assumption, not calculated from the terminal temperatures or measured equipment.
There is no additional fouling, heat loss or phase change in this example.

| Supplied example input | Value / units | Status |
| --- | --- | --- |
| Hot / cold mass flow | 1.0 / 0.5 kg/s | Given example conditions |
| Both specific heat capacities | 4180 J/(kg K) | Constant assumed liquid properties |
| Hot inlet / cold inlet | 70 / 15 °C | Given inlet conditions |
| Cold outlet | 35 °C | Required target |
| Overall coefficient U | 650 W/(m² K) | Assumed clean exchanger performance |
| LMTD correction factor | 1, dimensionless | Ideal countercurrent geometry |

Duty, hot outlet, LMTD and area are **calculated outputs**. Temperature differences
have the same numerical value in K and °C. This smaller worked case is separate
from the main design case below; do not mix their stream data.
First calculate the duty, then use that same duty to calculate the hot outlet.
Only then calculate area. Expected results: 41.8 kW, 60 °C, and about 1.62 m².
''', '''
    ex_mh, ex_mc = 1.0, 0.5  # given hot/cold mass flows, kg/s
    ex_cp = 4180.0  # assumed specific heat capacity of both liquids, J/(kg K)
    ex_U = 650.0  # assumed clean overall heat-transfer coefficient, W/(m² K)
    ex_Ch, ex_Cc = ex_mh * ex_cp, ex_mc * ex_cp  # capacity rates, W/K
    ex_Thi, ex_Tci, ex_Tco = 70.0, 15.0, 35.0
    ex_duty = ex_Cc * (ex_Tco - ex_Tci)
    ex_Tho = ex_Thi - ex_duty / ex_Ch
    ex_dt1, ex_dt2 = ex_Thi - ex_Tco, ex_Tho - ex_Tci
    ex_lmtd = h.lmtd(ex_dt1, ex_dt2)
    ex_area = ex_duty / (ex_U * ex_lmtd)
    print(f"Duty = {ex_duty/1000:.1f} kW; hot outlet = {ex_Tho:.1f} °C")
    print(f"Terminal differences = {ex_dt1:.1f}, {ex_dt2:.1f} K; LMTD = {ex_lmtd:.2f} K")
    print(f"Required area = {ex_area:.2f} m²")
    print("Energy-balance residual / W:", ex_Ch*(ex_Thi-ex_Tho)-ex_duty)
    ''', 'Copy the cell and raise the cold outlet target to 45 °C. Predict whether area rises or falls. Then try 75 °C: inspect both terminal differences and explain why this target fails before asking the helper to evaluate LMTD.'),
    'lab_03_distillation': ('''### Worked example: balances and the first two steps
The feed enters between the two column sections. A total condenser returns part
of the condensed overhead as reflux; the rest leaves as distillate. For a simple
case take F = 100 kmol/h, zF = 0.5, xD = 0.9, xB = 0.1 and R = 3.
All compositions are mole fractions of the more volatile component, not mass
fractions. R = L/D is the dimensionless reflux ratio. Use **constant relative
volatility α = 2.4**, a supplied dimensionless teaching assumption for a
hypothetical mixture, with saturated-liquid feed q = 1, constant molar overflow,
a total condenser and an equilibrium partial reboiler.

| Supplied example input | Value / units | Status |
| --- | --- | --- |
| Feed F | 100 kmol/h | Given molar feed rate |
| Feed composition zF | 0.50 mol/mol | Given feed mole fraction |
| Distillate / bottoms xD, xB | 0.90 / 0.10 mol/mol | Product targets |
| Reflux ratio R | 3, dimensionless | Chosen operating condition |
| Relative volatility α | 2.4, dimensionless | Assumed equilibrium model parameter |
| Feed thermal condition q | 1, dimensionless | Saturated-liquid assumption |

Two plotted contacts are a demonstration length, not a supplied column size.
The balances give D = B = 50 kmol/h. Start at y = xD, move to equilibrium
to find x, then use the rectifying operating line to obtain the next y.
This example stops after two steps; it is not a complete stage counter.
''', '''
    ex_F, ex_zF, ex_xD, ex_xB, ex_R = 100.0, 0.5, 0.9, 0.1, 3.0
    ex_alpha = 2.4  # supplied constant relative volatility, dimensionless
    ex_D = ex_F * (ex_zF-ex_xB)/(ex_xD-ex_xB)
    ex_B = ex_F - ex_D
    print(f"Distillate = {ex_D:.1f}; bottoms = {ex_B:.1f} kmol/h")
    ex_rect, ex_strip = h.operating_lines(ex_zF, ex_xD, ex_xB, ex_R)
    ex_y = ex_xD
    ex_points = [(ex_xD, ex_y)]
    for ex_n in range(1, 3):
        ex_x = float(h.inverse_equilibrium(ex_y, ex_alpha))
        ex_points.append((ex_x, ex_y))  # horizontal: equilibrium
        ex_y = float(ex_rect(ex_x))  # both example steps are above the feed
        ex_points.append((ex_x, ex_y))  # vertical: operating line
        print(f"Step {ex_n}: liquid x = {ex_x:.4f}; next vapour y = {ex_y:.4f}")
    ex_grid = np.linspace(0, 1, 200)
    plt.figure(figsize=(6, 5))
    plt.plot(ex_grid, h.equilibrium(ex_grid, ex_alpha), label="Equilibrium")
    plt.plot(ex_grid, ex_grid, color="grey", label="Diagonal")
    plt.plot(ex_grid[ex_grid>=ex_zF], ex_rect(ex_grid[ex_grid>=ex_zF]), label="Rectifying")
    ex_steps = np.array(ex_points)
    plt.plot(ex_steps[:, 0], ex_steps[:, 1], "o-", label="First two stages")
    plt.xlabel("Liquid mole fraction x"); plt.ylabel("Vapour mole fraction y")
    plt.legend(); plt.grid(); plt.show()
    ''', 'Change R to 5 and compare the first two steps. Before extending the loop, add an if/else that selects the stripping line when x < zF. Explain why always using the rectifying line would fail below the feed.'),
    'lab_04_absorption': ('''### Worked example: follow a solute through two contacts
Gas enters the bottom and solvent enters the top. Count contacts from the top,
where the clean-gas target and fresh-solvent composition are known.
For a small example use Gs = 100 kmol/h, Ls = 300 kmol/h, m = 1.5,
Xin = 0 and Yout = 0.002. The first equilibrium liquid ratio is 0.001333;
the next gas ratio is 0.006. Repeat the same two operations for contact two.

| Supplied example input | Value / units | Meaning / status |
| --- | --- | --- |
| Gs | 100 kmol/h | Given solute-free gas-carrier flow |
| Ls | 300 kmol/h | Chosen solute-free solvent flow |
| Equilibrium slope m | 1.5, dimensionless | Assumed linear model Y* = mX; synthetic |
| Lean solvent Xin | 0 mol solute/mol solvent | Fresh solvent assumption |
| Clean gas Yout | 0.002 mol solute/mol carrier | Required outlet mole ratio |

X = x/(1−x) and Y = y/(1−y) are **mole ratios**, not mole fractions.
Assume isothermal, nonreacting absorption with constant solute-free flow rates.
The first two contacts are calculated demonstrations, not a specified total
column height or number of contacts. The later Yin = 0.03 is the inlet target
for the small-change exercise, not an extra condition used in these first two steps.
''', '''
    ex_G, ex_L, ex_m = 100.0, 300.0, 1.5
    ex_Xin, ex_Yout = 0.0, 0.002
    ex_y = ex_Yout
    ex_points = [(ex_Xin, ex_y)]
    for ex_n in range(1, 3):
        ex_x = ex_y / ex_m  # horizontal move to equilibrium
        ex_points.append((ex_x, ex_y))
        ex_y = ex_Yout + ex_L/ex_G * (ex_x-ex_Xin)  # vertical to operating line
        ex_points.append((ex_x, ex_y))
        print(f"Contact {ex_n}: X = {ex_x:.6f}; next Y = {ex_y:.6f}")
    ex_grid = np.linspace(0, 0.006, 100)
    plt.figure(figsize=(6, 5))
    plt.plot(ex_grid, ex_m*ex_grid, label="Equilibrium")
    plt.plot(ex_grid, ex_Yout+ex_L/ex_G*(ex_grid-ex_Xin), label="Operating line")
    ex_steps = np.array(ex_points)
    plt.plot(ex_steps[:, 0], ex_steps[:, 1], "o-", label="First two contacts")
    plt.xlabel("Liquid mole ratio X"); plt.ylabel("Gas mole ratio Y")
    plt.legend(); plt.grid(); plt.show()
    ''', 'Change Ls from 300 to 400 kmol/h. Does each step cover more or less of the required gas-composition change? Extend the loop until it reaches Yin = 0.03, checking first that solvent flow exceeds its minimum.')
}


GUIDANCE = [
    '''**Suggested route:** (1) List known values and units. (2) Write the balance on
    paper. (3) Translate one equation at a time into named Python variables.
    (4) Print intermediate results and compare with a hand calculation.
    Start from the worked-example cell above rather than an empty page.''',
    '''**Suggested route:** Adapt the short example into a reusable function.
    Keep the base-case parameters outside the loop. Print the first three iterations
    before running a full search. Add the stopping rule, then a maximum iteration
    count and a clear error for infeasible inputs. Compare one validated result
    with the helper before making a parameter sweep.''',
    '''**Suggested route:** Copy your validated base-case calculation. Change one
    parameter at a time in a short for-loop, store results in a list, then plot.
    Label infeasible designs explicitly. First compare two cases by hand so you
    know what trend to expect.''',
    '''**Suggested route:** State what stays fixed in this experiment. Use at least
    five parameter values, include the base case, and report the change relative
    to it. Explain the physical reason for the trend before choosing a design.'''
]
