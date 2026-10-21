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
For this case, the combined dimensionless loss coefficient for the bends and
valves has been determined to be **ΣK = 8**, based on the pipe velocity.
Thus `ex_fitting_loss = 8.0 * ex_v**2 / (2 * 9.81)` is their total head loss
in metres of fluid; 8 is a supplied coefficient, not a count of fittings.
At 3 L/s you should find a velocity near 0.904 m/s and a system head near 14.0 m.
The pump supplies 26.5 m, so the actual intersection should lie at a higher flow.
''', '''
    ex_Q = 3.0 / 1000  # convert L/s to m³/s before using SI equations
    ex_D, ex_L, ex_rise = 0.065, 120.0, 12.0
    ex_v = ex_Q / (np.pi * ex_D**2 / 4)
    ex_Re = 998.0 * ex_v * ex_D / 0.001
    ex_f = float(h.friction_factor(ex_Re, 4.5e-5 / ex_D))
    ex_pipe_loss = ex_f * ex_L / ex_D * ex_v**2 / (2 * 9.81)
    ex_fitting_loss = 8.0 * ex_v**2 / (2 * 9.81)  # determined total ΣK = 8; head loss in m
    ex_required = ex_rise + ex_pipe_loss + ex_fitting_loss
    ex_available = float(h.pump_head(ex_Q))
    print(f"Velocity = {ex_v:.3f} m/s; Re = {ex_Re:.0f}; Darcy f = {ex_f:.4f}")
    print(f"Rise = {ex_rise:.2f} m; pipe loss = {ex_pipe_loss:.2f} m; fittings = {ex_fitting_loss:.2f} m")
    print(f"Required = {ex_required:.2f} m; pump = {ex_available:.2f} m")
    print(f"Head surplus = {ex_available-ex_required:.2f} m")
    ''', 'Copy the cell and change only ex_D to 0.050 m. Predict the direction of the loss change first. Then change the trial flow to 4 L/s. Which term changes most?'),
    'lab_02_heat': ('''### Worked example: heat a small cold-water stream
Trace the orange stream left to right and the blue stream right to left.
Use an easier target first: heat 0.5 kg/s of water from 15 to 35 °C using
1.0 kg/s of hot water entering at 70 °C. Both heat capacities are 4180 J/(kg K).
First calculate the duty, then use that same duty to calculate the hot outlet.
Only then calculate area. Expected results: 41.8 kW, 60 °C, and about 1.62 m².
''', '''
    ex_Ch, ex_Cc = 1.0 * 4180, 0.5 * 4180  # W/K
    ex_Thi, ex_Tci, ex_Tco = 70.0, 15.0, 35.0
    ex_duty = ex_Cc * (ex_Tco - ex_Tci)
    ex_Tho = ex_Thi - ex_duty / ex_Ch
    ex_dt1, ex_dt2 = ex_Thi - ex_Tco, ex_Tho - ex_Tci
    ex_lmtd = h.lmtd(ex_dt1, ex_dt2)
    ex_area = ex_duty / (650.0 * ex_lmtd)
    print(f"Duty = {ex_duty/1000:.1f} kW; hot outlet = {ex_Tho:.1f} °C")
    print(f"Terminal differences = {ex_dt1:.1f}, {ex_dt2:.1f} K; LMTD = {ex_lmtd:.2f} K")
    print(f"Required area = {ex_area:.2f} m²")
    print("Energy-balance residual / W:", ex_Ch*(ex_Thi-ex_Tho)-ex_duty)
    ''', 'Copy the cell and raise the cold outlet target to 45 °C. Predict whether area rises or falls. Then try 75 °C: inspect both terminal differences and explain why this target fails before asking the helper to evaluate LMTD.'),
    'lab_03_distillation': ('''### Worked example: balances and the first two steps
The feed enters between the two column sections. A total condenser returns part
of the condensed overhead as reflux; the rest leaves as distillate. For a simple
case take F = 100 kmol/h, zF = 0.5, xD = 0.9, xB = 0.1 and R = 3.
The balances give D = B = 50 kmol/h. Start at y = xD, move to equilibrium
to find x, then use the rectifying operating line to obtain the next y.
This example stops after two steps; it is not a complete stage counter.
''', '''
    ex_F, ex_zF, ex_xD, ex_xB, ex_R = 100.0, 0.5, 0.9, 0.1, 3.0
    ex_D = ex_F * (ex_zF-ex_xB)/(ex_xD-ex_xB)
    ex_B = ex_F - ex_D
    print(f"Distillate = {ex_D:.1f}; bottoms = {ex_B:.1f} kmol/h")
    ex_rect, ex_strip = h.operating_lines(ex_zF, ex_xD, ex_xB, ex_R)
    ex_y = ex_xD
    ex_points = [(ex_xD, ex_y)]
    for ex_n in range(1, 3):
        ex_x = float(h.inverse_equilibrium(ex_y, 2.4))
        ex_points.append((ex_x, ex_y))  # horizontal: equilibrium
        ex_y = float(ex_rect(ex_x))  # both example steps are above the feed
        ex_points.append((ex_x, ex_y))  # vertical: operating line
        print(f"Step {ex_n}: liquid x = {ex_x:.4f}; next vapour y = {ex_y:.4f}")
    ex_grid = np.linspace(0, 1, 200)
    plt.figure(figsize=(6, 5))
    plt.plot(ex_grid, h.equilibrium(ex_grid), label="Equilibrium")
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
