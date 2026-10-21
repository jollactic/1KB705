"""Lab 1: supplied pump performance and fixed-duty design workshop content."""
import nbformat

THEORY = r'''## Model and assumptions

The system transfers water between large open tanks. Flow is steady and
incompressible; tank-surface velocities are negligible. Pipe length is 120 m,
water density 998 kg/m³ and viscosity 0.001 Pa s; roughness is 0.000045 m.
The base elevation rise is 12 m. The combined dimensionless coefficient for
**bends and valves has been determined to be $\sum K=8$**, based on pipe velocity.

$$
v=\frac{4Q}{\pi D^2},\qquad Re=\frac{\rho vD}{\mu},\qquad
H_s=\Delta z+\left(f_D\frac{L}{D}+8\right)\frac{v^2}{2g}.
$$

Use the Darcy friction factor: $64/Re$ for laminar flow and the Haaland
approximation for turbulent flow. The helper rejects transition flow.

**Synthetic pump curves, not manufacturer data.** Real pump curves are normally
established through testing. Here the reference-speed curves are assumed:

$$
H_{ref}(q)=40-1.5\times10^6q^2,\qquad
P_{shaft,ref}(q)=900+40000q.
$$

Flow $q$ is in m³/s, head in m and shaft power in W. The coefficient 40000
has units W s/m³. These illustrative curves form a consistent pair for water
of the specified density; they are not a universal pump law. Efficiency is
**derived from the two curves**, not assumed constant:

$$
\eta_p=\frac{\rho gQH_p}{P_{shaft}}.
$$

For speed ratio $s=N/N_0$, use approximate affinity scaling with $q=Q/s$:

$$
H_p(Q,s)=s^2H_{ref}(Q/s),\qquad
P_{shaft}(Q,s)=s^3P_{shaft,ref}(Q/s).
$$

The BEP is the maximum-efficiency point on these synthetic curves. For this
exercise only, assume a permitted speed ratio of **0.6–1.1** and a recommended
flow band of **0.65–1.35 times the BEP flow at the actual speed**, per pump.
These are teaching screening limits, not manufacturer-approved operating limits.
The plotted shutoff point has nonzero shaft input and zero hydraulic output;
it is not an acceptable continuous operating condition.

**Electrical energy includes motor and drive losses.** Assume motor efficiency
0.90 and drive efficiency 0.96. With total shaft power summed over running pumps:

$$
P_{electric}=\frac{\sum P_{shaft}}{\eta_m\eta_d},\qquad
E_{year}=\frac{P_{electric}}{1000}t_{hours},\qquad
e_V=\frac{P_{electric}}{3.6\times10^6Q}.
$$

The last quantity is kWh/m³. Constant motor/drive efficiencies are simplifications.
We omit cavitation/NPSH, motor and pressure ratings, transients and interconnecting
pipe losses. In pairs, pumps are identical, run at the same speed and share
flow equally in parallel; heads add in series. Passing the screening limits
does not approve procurement.

Background: [KSB characteristic curves](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/characteristic-curve-1117926)
and [affinity laws](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/pump-affinity-laws-1117584).
'''

STARTER = '''
rho, mu, g = 998.0, .001, 9.81
length, rise, roughness, K = 120., 12., 4.5e-5, 8.
diameter = .065
base_flow = h.free_operating_point(diameter)
base_performance = h.performance(base_flow)
print(f"Reference BEP flow: {h.BEP_FLOW*1000:.3f} L/s")
print(f"Uncontrolled base flow: {base_flow*1000:.4f} L/s")
h.plot_performance(operating_flow=base_flow)
plt.show()
'''

TASKS = [
('2. Read the performance curves and check the energy balance — 60 minutes',r'''
Read the three aligned performance plots: blue head, green efficiency, red shaft
input and dashed electrical input. The shaded band is an assumed per-pump
operating range. Identify the BEP and determine whether the uncontrolled base
point lies within it. A hydraulic intersection can exist outside this band.

Hand-check velocity and fitting head loss at 3 L/s. Then explain hydraulic,
shaft and electrical power at the uncontrolled operating point. Check the
efficiency identity and convert power to annual energy at 4000 h/year.
Why is zero-flow shaft power nonzero? Why must we not extrapolate to negative
head? Identify which numbers are measured data and which are assumed here.
''','', '''
trial_q = .003
v = 4*trial_q/(np.pi*diameter**2)
fitting_loss = 8*v*v/(2*g)
point = base_performance
print(f"At 3 L/s: v={v:.5f} m/s; fitting loss={fitting_loss:.5f} m")
print(f"Uncontrolled flow={base_flow*1000:.5f} L/s; head={point['head']:.5f} m")
print(f"Pump efficiency={point['efficiency']*100:.3f}%; in assumed band={bool(point['recommended'])}")
print(f"Hydraulic={point['hydraulic']:.2f} W; shaft={point['shaft']:.2f} W; electrical={point['electrical']:.2f} W")
print(f"Annual electrical energy={point['electrical']/1000*4000:.2f} kWh")
assert np.isclose(point['hydraulic'], point['efficiency']*point['shaft'])
assert point['electrical'] > point['shaft'] >= point['hydraulic']
print(f"Shutoff shaft input={h.performance(0)['shaft']:.1f} W (not an allowed duty)")
q_plot = np.linspace(.001,h.RUNOUT_FLOW,180)
plt.figure(figsize=(8,4))
plt.plot(q_plot*1000,h.pump_head(q_plot),label='Full-speed pump')
plt.plot(q_plot*1000,h.system_head(q_plot,diameter,120,12,roughness,8),label='Base system')
plt.scatter([base_flow*1000],[point['head']],color='black',label='Hydraulic intersection')
plt.xlabel('Total flow / L s$^{-1}$'); plt.ylabel('Head / m'); plt.legend(); plt.grid(); plt.show()
'''),
('3. Compare pipe diameters at the same delivery — 75 minutes',r'''
The base requirement is **exactly 3 L/s**, delivered for 4000 h/year. A variable-
speed drive adjusts speed to meet that flow without throttling. Run the supplied
table for 50, 65 and 80 mm internal diameters. For each, check required speed,
efficiency, electrical power, kWh/m³ and the assumed operating limits.

Select a diameter and report why it passes or fails. Does lower friction always
mean higher pump efficiency? Compare electricity at equal annual volume, not
uncontrolled flows. Inspect the selected-speed diagram and identify its BEP
relative to the actual operating point. Speed and each pump's flow must be
checked together. Do not change pipe roughness or fitting K between candidates.
''', '''required_flow_Lps = 3.0 #@param {type:"number"}
operating_hours = 4000 #@param {type:"number"}
selected_diameter = 0.050 #@param [0.05, 0.065, 0.08] {type:"raw"}''', '''
required_flow = required_flow_Lps/1000
diameters = [.050,.065,.080]
designs = [h.design_at_flow(required_flow,D,hours=operating_hours) for D in diameters]
print('D/mm  speed   eta/%   electric/W  kWh/m³   annual/kWh  speed OK  band OK')
for D,row in zip(diameters,designs):
    print(f"{D*1000:4.0f}  {row['speed']:.4f}  {row['efficiency']*100:6.2f}  {row['electrical']:9.2f}  {row['specific_kwh']:.6f} {row['annual_kwh']:10.2f}  {row['speed_ok']}  {row['range_ok']}")
chosen = h.design_at_flow(required_flow,selected_diameter,hours=operating_hours)
print(f"Chosen diameter: {selected_diameter*1000:.0f} mm; feasible under supplied limits={chosen['feasible']}")
print(f"Annual delivered volume: {required_flow*3600*operating_hours:.1f} m³")
assert all(np.isclose(h.arrangement_head(required_flow,row['speed']),row['head']) for row in designs)
h.plot_performance(chosen['speed'],required_flow); plt.show()
'''),
('4. Choose an energy or lifecycle design — 90 minutes',r'''
Use these **illustrative installed pipe costs** for the complete 120 m line:
50 mm €6000, 65 mm €8500, 80 mm €12000. They are supplied teaching inputs,
not quotations. Pump and drive purchase costs are common to these three single-
pump options and omitted from this incremental comparison. Use electricity
€0.20/kWh, ten years, and no discounting, maintenance or residual value.

Compare installed pipe cost plus electricity over that horizon. Select a
feasible diameter on total cost, and compare it with the least-electricity
candidate. Does the answer change at electricity €0.10 or €0.40/kWh?
Calculate the payback of a larger pipe where electricity savings are positive;
if savings are negative, report no energy payback. Explain why this simplified
cost model is not a procurement estimate.

For your selected diameter, inspect the supplied roughness sweep at fixed flow.
Is the required speed and pump operating band still acceptable? State the
remaining electrical-power and cost assumptions that matter to your choice.
''', '''electricity_price = 0.20 #@param {type:"number"}
years = 10 #@param {type:"number"}''', '''
pipe_costs = np.array([6000.,8500.,12000.])
annual_energy = np.array([row['annual_kwh'] for row in designs])
totals = pipe_costs+electricity_price*years*annual_energy
feasible_mask = np.array([row['feasible'] for row in designs])
print('D/mm  pipe/€  electricity/€  total/€  eligible')
for D,cost,energy,total,ok in zip(diameters,pipe_costs,annual_energy,totals,feasible_mask):
    print(f'{D*1000:4.0f}  {cost:7.0f} {electricity_price*years*energy:13.2f} {total:9.2f} {ok}')
if np.any(feasible_mask):
    best_index = int(np.argmin(np.where(feasible_mask,totals,np.inf)))
    energy_index = int(np.argmin(np.where(feasible_mask,annual_energy,np.inf)))
    print(f'Least cost: {diameters[best_index]*1000:.0f} mm; least electricity: {diameters[energy_index]*1000:.0f} mm')
else:
    best_index = None
    print('No feasible candidate at this duty; do not select on cost alone.')
for price in [.10,.20,.40]:
    costs = pipe_costs+price*years*annual_energy
    if np.any(feasible_mask):
        idx = int(np.argmin(np.where(feasible_mask,costs,np.inf)))
        print(f'At €{price:.2f}/kWh: least-cost feasible pipe {diameters[idx]*1000:.0f} mm')
for small,large in [(0,1),(1,2),(0,2)]:
    savings = electricity_price*(annual_energy[small]-annual_energy[large])
    if savings > 0:
        print(f'{diameters[small]*1000:.0f}→{diameters[large]*1000:.0f} mm: simple payback {(pipe_costs[large]-pipe_costs[small])/savings:.2f} years')
    else:
        print('No positive electricity savings; no energy payback')
fig,axes = plt.subplots(1,2,figsize=(11,4))
axes[0].bar(np.array(diameters)*1000,totals,width=7)
axes[0].set(xlabel='Internal diameter / mm',ylabel='Illustrative horizon cost / €')
roughness_values = np.linspace(1e-6,2e-4,30)
rough_results = [h.design_at_flow(required_flow,selected_diameter,roughness=e,hours=operating_hours) for e in roughness_values]
axes[1].plot(roughness_values*1e6,[row['electrical'] for row in rough_results])
axes[1].set(xlabel='Roughness / µm',ylabel='Electrical input at fixed delivery / W')
plt.tight_layout(); plt.show()
print('Selected pipe feasible throughout roughness sweep:',all(row['feasible'] for row in rough_results))
'''),
('5. Choose single, series or parallel pumps — 60 minutes',r'''
This is a **core design challenge**. Take a 10-minute break within this block.
Keep the 80 mm line and the same pump type. Compare three arrangements at
exactly the required delivery using speed control: one pump, two identical pumps
in series, and two identical pumps in parallel. Count both running motors.

**Duty A:** 6 L/s against a 12 m elevation rise. **Duty B:** 3 L/s against
a 55 m rise. These are two separate changed requirements, not simultaneous duties.
Use the supplied diagrams and tables to decide which arrangements satisfy speed
and per-pump operating-band limits. Explain why heads add in series and flows
add in parallel, and why neither arrangement guarantees an acceptable point.
Report total electrical input and energy per volume for feasible candidates.
Do not compare arrangements by each pump's power alone.

Would two parallel pumps double uncontrolled flow in the original line? Use the
printed equal-speed intersection comparison. List at least three missing checks
before specifying an actual paired installation: suction/NPSH, casing pressure,
motor ratings, connecting pipe losses, valves, control or transients.
''','', '''
arrangement_results = {}
h.plot_arrangements(); plt.show()
for name,flow,target_rise in [('A',.006,12.),('B',.003,55.)]:
    print()
    print(f'Duty {name}: {flow*1000:.1f} L/s, static rise {target_rise:.1f} m')
    for arrangement in ['single','series','parallel']:
        row = h.design_at_flow(flow,.080,target_rise,arrangement,hours=operating_hours)
        arrangement_results[(name,arrangement)] = row
        print(f"{arrangement:8s}: speed={row['speed']:.4f}, each Q={row['pump_flow']*1000:.2f} L/s, eta={row['efficiency']*100:.2f}%, total electric={row['electrical']:.2f} W, eV={row['specific_kwh']:.6f} kWh/m³, feasible={row['feasible']} (speed={row['speed_ok']}, band={row['range_ok']})")
fig,axes = plt.subplots(1,2,figsize=(12,4))
for axis,(name,flow,target_rise) in zip(axes,[('A',.006,12.),('B',.003,55.)]):
    q = np.linspace(.001,.011,250)
    axis.plot(q*1000,h.system_head(q,.080,120,target_rise,roughness,8),color='black',label='System')
    for arrangement in ['single','series','parallel']:
        head = h.arrangement_head(q,1.,arrangement)
        axis.plot(q[head>=0]*1000,head[head>=0],label=arrangement+' at speed 1')
    axis.axvline(flow*1000,color='grey',linestyle=':',label='Required flow')
    axis.set(xlabel='Total flow / L s$^{-1}$',ylabel='Head / m',ylim=(0,90),title=f'Duty {name}')
    axis.legend(fontsize=8); axis.grid()
plt.tight_layout(); plt.show()
single_free = h.free_operating_point(.065)
parallel_free = h.free_operating_point(.065,arrangement='parallel')
print(f'Original 65 mm line, speed 1: single={single_free*1000:.4f} L/s; parallel={parallel_free*1000:.4f} L/s; twice single={single_free*2000:.4f} L/s')
assert single_free < parallel_free < 2*single_free
''')]


def adapt_flow_notebook(notebook,md,code):
    prefix = []
    for cell in notebook.cells:
        if cell.cell_type=='markdown' and cell.source.startswith('## 2.'):
            break
        if cell.cell_type=='markdown' and cell.source.startswith('## Model and assumptions'):
            cell = md(THEORY)
        if cell.cell_type=='code' and 'rho, mu, g = 998.0' in cell.source:
            cell = code(STARTER)
        if cell.cell_type=='markdown' and cell.source.startswith('## Design workshop:'):
            cell.source = '''## Design workshop: run → compare → decide

All calculations and plots are supplied. Edit only **DESIGN SETTINGS**, then
rerun that section and the sections below it. Write engineering decisions using
numbers and units. No algorithm writing is required. This edition compares
electrical energy at equal delivery, includes illustrative pipe costs, and
treats series/parallel pumps as a core task.

Six-hour budget: setup 30 min; curve/energy review 60 min; fixed-duty diameter
comparison 75 min; costs and robustness 90 min; pump arrangements including a
break 60 min; final recommendation 45 min. The small worked example belongs
within the curve/energy review. Paired-pump curves are idealized screening tools.
'''
        prefix.append(cell)
    for index,(title,prompt,settings,analysis) in enumerate(TASKS):
        prefix.append(md('## '+title+'\n\n'+prompt))
        if settings:
            setting_cell = code('#@title DESIGN SETTINGS\n'+settings)
            setting_cell.metadata['design_settings'] = index
            prefix.append(setting_cell)
        supplied = code('#@title SUPPLIED ANALYSIS — run without edits\n'+analysis)
        supplied.metadata.update(design_analysis=index,jupyter={'source_hidden':True},cellView='form')
        prefix.append(supplied)
        answer = md('**Your design decision:** State the requirement, numerical evidence, selection or rejection, '
                    'and what new evidence could change it. Answer every question in this section.')
        answer.metadata['design_answer'] = index
        prefix.append(answer)
    prefix += [md('''## 6. Engineering recommendation — 45 minutes

Write 300–500 words covering your base-duty pipe/speed choice, electrical energy,
cost criterion, one rejected alternative and robustness. Recommend arrangements
for both changed duties and identify missing procurement checks. Include evidence
from the supplied plots. A feasible screen is not a verified equipment design.
Restart and run all cells in order before submitting. Ask your partner to explain
one energy conversion and one rejected design; record any resulting revision.
'''),md('''## Optional extension

What changes if the plant has a fixed-speed drive and controls delivery by
throttling? Explain where excess head is dissipated and how the fair electrical-
energy comparison would need to change. No extra code is required.''')]
    notebook.cells = prefix
    notebook.metadata['flow_model'] = 'variable-efficiency-fixed-duty-v2'
    return notebook
