"""Authoring source for introductory Lab 00 and its separate instructor notebook."""
from pathlib import Path
from io import BytesIO
import base64
import inspect
import nbformat

ROOT=Path(__file__).parent


def diagram(kind):
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,FancyArrowPatch
    fig,ax=plt.subplots(figsize=(10,3.2))
    ax.set(xlim=(0,10),ylim=(0,3.2)); ax.axis('off')
    def arrow(start,end):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=15,lw=2,color='steelblue'))
    ax.add_patch(Rectangle((4,1),2,1.3,fc='#edf5fc',ec='navy',lw=2))
    if kind=='mix':
        ax.text(5,1.65,'Mixer',ha='center')
        arrow((.3,2.2),(4,2.2)); arrow((.3,1.1),(4,1.1)); arrow((6,1.65),(9.7,1.65))
        ax.text(1.9,2.5,'A: 80 kg/h, 10 wt% salt',ha='center')
        ax.text(1.9,.65,'B: 20 kg/h, pure water',ha='center')
        ax.text(8,2,'C: flow and composition?',ha='center')
    elif kind=='heat':
        ax.text(5,1.65,'Water heater',ha='center')
        arrow((.3,1.65),(4,1.65)); arrow((6,1.65),(9.7,1.65)); arrow((5,.1),(5,1))
        ax.text(2,2.1,'2 kg/s at 20 °C',ha='center')
        ax.text(8,2.1,'2 kg/s at 50 °C',ha='center'); ax.text(5,.35,'Heat in',ha='right')
    else:
        ax.text(5,1.65,'Tank\nM(t)',ha='center',va='center')
        arrow((.3,1.65),(4,1.65)); arrow((6,1.65),(9.7,1.65))
        ax.text(2,2.1,'In: 2 kg/s',ha='center'); ax.text(8,2.1,'Out: 1.5 kg/s',ha='center')
        ax.text(5,.4,'Initial mass 50 kg; maximum contents 400 kg',ha='center')
    ax.add_patch(Rectangle((3.6,.85),2.8,1.6,fill=False,ec='grey',ls='--'))
    ax.text(5,2.8,'Dashed line: chosen system boundary',ha='center')
    stream=BytesIO(); fig.tight_layout(); fig.savefig(stream,format='png',dpi=140); plt.close(fig)
    return base64.b64encode(stream.getvalue()).decode('ascii')


TASKS=[
('2. Mix two streams: total and component mass — 35 minutes','mix',r'''
**Worked example.** Stream A is 80 kg/h of salt solution with salt mass fraction
0.10; stream B is 20 kg/h pure water. Salt does not react. The mixer operates
at steady state with one outlet and no loss.

1. Draw the boundary and label every stream. What do 10 wt% and kg/h mean?
2. Write the total mass balance **before** putting in numbers: $A+B=C$.
3. Write the salt balance: $Aw_A+Bw_B=Cw_C$. Derive C and wC by hand.
4. Check the supplied result and explain why the outlet fraction lies between
   the two inlet fractions. Is the outlet salt flow lower after dilution?
5. Change only the water feed to 40 kg/h. Predict the concentration first,
   then calculate. How much water is needed to reach exactly 5 wt%?

Use **mass fractions**, not molar fractions: no molecular weights are needed.
''','''water_feed = 20.0 #@param {type:"number"}''','''
A,wA = 80.,.10
B,wB = water_feed,0.
C,wC = h.mix_streams(A,wA,B,wB)
print(f'Outlet C={C:.2f} kg/h; salt fraction={wC:.5f} kg/kg ({wC*100:.2f} wt%)')
print(f'Salt in={A*wA+B*wB:.2f} kg/h; salt out={C*wC:.2f} kg/h')
print(f'Total residual={A+B-C:.3e} kg/h; salt residual={A*wA+B*wB-C*wC:.3e} kg/h')
target_salt_fraction = .05  # stated 5 wt% product target, kg salt/kg solution
water_needed=A*wA/target_salt_fraction-A
print(f'Water feed for 5 wt% target: {water_needed:.2f} kg/h')
''',r'''
**Boundary and equations.** Both inlets and the single outlet cross the mixer
boundary. Steady state means zero accumulation. Ten wt% is 10 kg salt per
100 kg solution; kg/h describes mass passing per hour, not mass stored.
The total balance gives C = 80 + 20 = **100 kg/h**. Salt enters at
80(0.10) + 20(0) = **8 kg/h**, so wC = 8/100 = **0.08**, or 8 wt%.
Both residuals are zero apart from numerical roundoff.

**Dilution does not remove salt.** The outlet carries the same 8 kg/h salt;
only its fraction decreases because more water accompanies it. With 40 kg/h
water, C = 120 kg/h and wC = 8/120 = **6.667 wt%**. This lies between
the inlet fractions, as a nonreacting mixture must. A result above 10 wt%
would signal an error under these assumptions.

**Target calculation.** At 5 wt%, C = 8/0.05 = 160 kg/h, hence pure-water
feed B = 160 − 80 = **80 kg/h**. Distinguish this total water feed from
the additional 60 kg/h needed relative to the original 20 kg/h case.
'''),
('3. Split or concentrate: choose the right balance — 35 minutes',None,r'''
Treat these as **two separate examples**, each fed with the original 100 kg/h,
8 wt% solution from the mixer.

**Splitter:** send 30% of the well-mixed stream to one branch. Write a total
balance and a salt balance. What are each branch's flow and concentration?
Does splitting alone produce one purer stream? Check the supplied results.

**Evaporator:** remove pure water as vapour, leaving a 20 wt% salt product.
Assume nonvolatile salt, no entrainment, no crystallization and steady operation.
Write $F=P+V$ and $Fw_F=Pw_P$ before calculating P and V. Why is a single
total balance insufficient? Check salt and water separately. Change target
product concentration to 10 wt%; does the direction of change make sense?

These are mass balances only. What is still missing to calculate evaporation
heat? Why should concentrating to a value below the feed fraction be rejected
for this pure-water-removal operation?
''','''product_fraction = 0.20 #@param {type:"number"}''','''
F,wF = 100.,.08  # stated original mixer outlet: kg/h, kg salt/kg solution
split_fraction = .30  # supplied branch-one mass-flow fraction
branch1,branch2 = split_fraction*F,(1-split_fraction)*F
print(f'Splitter: {branch1:.1f} and {branch2:.1f} kg/h; both {wF*100:.1f} wt% salt')
P,V=h.evaporate(F,wF,product_fraction)
print(f'Evaporator product={P:.3f} kg/h; pure-water vapour={V:.3f} kg/h')
print(f'Salt residual={F*wF-P*product_fraction:.3e} kg/h')
print(f'Water residual={F*(1-wF)-P*(1-product_fraction)-V:.3e} kg/h')
''',r'''
**Splitter.** The branch flows are **30 and 70 kg/h**, each at **8 wt%**.
Salt flows are 2.4 and 5.6 kg/h, adding to 8 kg/h. A simple splitter of
a homogeneous liquid changes the amount sent each way, not composition.

**Evaporator.** The independent salt balance fixes P = 100(0.08)/0.20 =
**40 kg/h**; the total balance then gives V = **60 kg/h**. Product salt
is 8 kg/h and product water is 32 kg/h. The incoming 92 kg/h water equals
32 in product plus 60 in vapour. Two unknown outlet flows need two independent
balances: the total equation alone admits many possible P,V pairs.

At a 10 wt% target, product rises to **80 kg/h** and evaporation falls to
**20 kg/h**. Less water removal is needed for a weaker concentration change.
A target below 8 wt% would imply negative evaporation; dilution requires water
addition rather than this operation. The helper therefore rejects it.

**No evaporation duty has been calculated.** Heat requires inlet/outlet
temperatures, phase conditions, latent heat and sensible-heat information, plus
any external loss. Multiplying the evaporated mass by liquid heat capacity
and an arbitrary temperature difference would omit phase-change energy.
'''),
('4. Heat a stream and mix temperatures — 40 minutes','heat',r'''
**Water heater.** Heat 2 kg/s water from 20 to 50 °C, with constant
cp = 4180 J/(kg K), no heat loss, no phase change and no shaft work. Neglect
kinetic and potential energy changes. Write the steady energy balance, then
use $\dot Q=\dot m c_p(T_{out}-T_{in})$. Check units before computing.
Here cp means that heating 1 kg of this liquid by 1 K requires 4180 J.
Temperature differences in °C and K are equal. This example uses kg/s;
1 kg/s equals 3600 kg/h, unlike the hourly flows in the earlier examples.

Calculate heat duty in W and kW, then energy for two hours in kWh. Explain
the difference between power and energy. What changes if flow doubles or
outlet temperature is 40 °C? Are we calculating electricity or heat transferred?

**Adiabatic mixer, separate example.** Mix 0.5 kg/s water at 80 °C with
1.5 kg/s water at 20 °C. Write the total mass balance and energy balance
using the same temperature reference and constant cp for both streams. Find
the outlet temperature. Why is the simple arithmetic mean incorrect here?
Explain why outlet temperature must lie between the inlet temperatures.
''','''heated_flow = 2.0 #@param {type:"number"}
inlet_temperature = 20.0 #@param {type:"number"}
target_temperature = 50.0 #@param {type:"number"}''','''
water_cp = 4180.0  # supplied constant specific heat capacity, J/(kg K)
duty=h.heating_duty(heated_flow,water_cp,inlet_temperature,target_temperature)
print(f'Heat supplied={duty:.1f} W = {duty/1000:.3f} kW')
print(f'Heat supplied over 2 hours={duty/1000*2:.3f} kWh')
mixed_temperature=h.mixing_temperature(.5,80.,1.5,20.)
print(f'Adiabatic mixed outlet: 2 kg/s at {mixed_temperature:.3f} °C')
reference=20.
energy_in=.5*water_cp*(80-reference)+1.5*water_cp*(20-reference)
energy_out=2*water_cp*(mixed_temperature-reference)
print(f'Mixer energy residual={energy_in-energy_out:.3e} W')
''',r'''
**Heater balance.** With the stated simplifications,
$\dot Q=\dot m(h_{out}-h_{in})=\dot m c_p\Delta T$.
Units are (kg/s)(J/(kg K))(K) = J/s = W. The 30 °C temperature difference
is also a 30 K difference: no 273.15 offset belongs in this subtraction.
The duty is **250800 W = 250.8 kW**. Over two hours, heat supplied is
**501.6 kWh**. kW measures transfer rate; kWh measures energy over time.
Doubling flow doubles duty to 501.6 kW. At 40 °C outlet with original
flow, duty is 167.2 kW. This is heat transferred to water, not automatically
electrical input: a heater efficiency or heat-source model is still needed.

**Adiabatic mixing.** Mass out is 0.5 + 1.5 = 2 kg/s. With a shared
enthalpy reference and constant equal cp, energy conservation reduces to
$T_C=(\dot m_A T_A+\dot m_B T_B)/(\dot m_A+\dot m_B)$, giving **35 °C**.
The arithmetic mean, 50 °C, would apply only to equal mass flows under these
assumptions. The colder stream has three times the mass flow, pulling the
result toward 20 °C. The result must stay between 20 and 80 °C without
external heat, phase change or heat of mixing.
'''),
('5. A filling tank: when accumulation matters — 25 minutes','tank',r'''
Take a short break within this block. Initially the tank holds 50 kg water.
Constant inflow is 2 kg/s and constant outflow is 1.5 kg/s. Maximum contents
are 400 kg. There is no level controller. Treat the tank as well-mixed; no
density change or reaction occurs.

Write $dM/dt=\dot m_{in}-\dot m_{out}$ and integrate for constant flows.
How much water is present after ten minutes? Is this steady state? When does
the tank reach capacity? Predict what happens if outflow equals inflow.
Explain why the line must not be extrapolated past overflow or emptying.
At density 1000 kg/m³, what volume corresponds to the ten-minute inventory?
The supplied plot stops at the first capacity limit, not after it.
''','''tank_outflow = 1.5 #@param {type:"number"}''','''
initial_mass,inflow,capacity=50.,2.,400.
evaluation_seconds = 10*60  # ten-minute inventory check, converted to seconds
water_density = 1000.0  # supplied volume-conversion density, kg/m³
net=inflow-tank_outflow
limit=(capacity-initial_mass)/net if net>0 else (initial_mass/(-net) if net<0 else np.inf)
print(f'Net accumulation={net:.3f} kg/s')
if evaluation_seconds <= limit:
    mass10=float(h.tank_inventory(initial_mass,inflow,tank_outflow,evaluation_seconds))
    print(f'At 10 min: inventory={mass10:.2f} kg; volume={mass10/water_density:.3f} m³')
else:
    print('A boundary limit is reached before ten minutes; constant-flow continuation is invalid.')
print(f'First boundary limit: {limit/60:.3f} min' if np.isfinite(limit) else 'No filling/emptying boundary reached at equal flows.')
times=np.linspace(0,min(900,limit),100)
inventory=h.tank_inventory(initial_mass,inflow,tank_outflow,times)
plt.plot(times/60,inventory,label='Valid constant-flow interval')
plt.axhline(capacity,color='black',linestyle=':',label='Capacity')
plt.xlabel('Time / min'); plt.ylabel('Water inventory / kg'); plt.legend(); plt.grid(); plt.show()
''',r'''
**Accumulation balance.** $dM/dt=2-1.5=0.5$ kg/s, so
$M(t)=50+0.5t$ with t in seconds. Ten minutes is 600 s, not 10 s:
inventory is **350 kg**, or **0.350 m³** at the stated density.
The nonzero accumulation means this is not steady state, despite constant
inlet and outlet flows.

**Capacity and model domain.** Setting 400 = 50 + 0.5t gives
t = **700 s = 11.667 min**. Beyond this point overflow, control or another
physical change must occur. The no-overflow balance cannot keep predicting
increasing inventory in a full tank. Likewise, a tank cannot maintain the
assumed positive outflow after emptying.

**Equal-flow case.** With outflow 2 kg/s, accumulation is zero and M stays
50 kg. That establishes constant total inventory, not necessarily constant
temperature or composition if other conditions change. One total balance
does not prove every aspect of the process is at steady state.
''')]


def build_intro(solution=False,execute=False):
    md=lambda s:nbformat.v4.new_markdown_cell(inspect.cleandoc(s))
    code=lambda s:nbformat.v4.new_code_cell(inspect.cleandoc(s))
    cells=[md('''# Lab 00 — First steps in mass and heat balances

Learn to choose a system boundary, label streams, state assumptions and write
balances before calculating. You need basic arithmetic and algebra; no prior
balance course or Python programming is assumed. All case values are synthetic.

**Workload:** about three hours of core work, including a short break. Optional
practice can extend this to four–six hours; it is an introduction rather than
another advanced design lab. Work in pairs. Show equations, substituted numbers
and units. Calculations are supplied so the focus remains on setting up balances.

Submit your completed answer cells and a short explanation (150–250 words) of
how you distinguish a mass balance, component balance and energy balance.
'''),md(r'''## 1. The balance recipe — 30 minutes

1. Draw the boundary: what equipment or volume is inside?
2. Label inputs, outputs and stored quantities. Write units beside each.
3. State assumptions: steady or changing inventory? Reaction? Heat loss?
4. Write the symbolic balance before inserting values; count unknowns.
5. Calculate and check units, conservation and physically sensible limits.

For a nonreacting system:

$$\text{accumulation rate}=\text{rate in}-\text{rate out}.$$

Total mass is conserved. For a component, include production/consumption if
there is reaction; all examples here are nonreacting. At steady state,
accumulation is zero. An energy balance also includes energy transferred as
heat or work across the boundary. The terms depend on the chosen boundary.

**Do not confuse:** kg (inventory) with kg/s (flow); mass fraction with mass
flow; kW (power) with kWh (energy). A balance residual of zero checks arithmetic
and consistency, but does not prove the assumptions match real equipment.

**Data convention:** Numbers stated in each problem are supplied inputs or
explicit assumptions; outlet properties and duties are calculated results.
The salt fractions are kg salt/kg solution. Drawings show the printed default
case; when changing a setting, update your own stream labels accordingly.

**Prediction:** If water is added to a salt solution without salt loss, will
salt mass flow, salt fraction, or both change? Write your prediction before running.
'''),md('''### Setup

Locally, open this notebook in `lab_00` with its own `helpers.py`. In Colab,
upload this notebook and that helper file using the Files panel. A separate
kernel/session prevents confusion with helpers from the other labs.
'''),code('''
from pathlib import Path
if not Path('helpers.py').exists():
    raise FileNotFoundError('Upload lab_00/helpers.py beside this notebook, then rerun.')
import numpy as np
import matplotlib.pyplot as plt
import helpers as h
''')]
    if solution:
        cells.insert(1,md('''**Completed instructor solution.** Written answers use the printed default
settings. Edited inputs change numerical outputs, not the written explanations.
Prediction: dilution lowers salt fraction while conserving salt flow.
'''))
        cells.insert(2,code('%matplotlib inline'))
    for index,(heading,kind,prompt,settings,analysis,answer) in enumerate(TASKS):
        cell=md('## '+heading+'\n\n'+prompt)
        if kind:
            cell.source+='\n\n![System boundary and streams](attachment:balance-system.png)'
            cell['attachments']={'balance-system.png':{'image/png':diagram(kind)}}
        cells.extend([cell,code('#@title SETTINGS — edit values only\n'+settings)])
        provided=code('#@title SUPPLIED CHECK — first write the equations yourself\n'+analysis)
        provided.metadata.update(jupyter={'source_hidden':True},cellView='form')
        cells.append(provided)
        response=md('**Worked answer and interpretation**\n\n'+answer if solution else
                    '**Your answer:** Write the symbolic balance, assumptions, numbers with units, '
                    'and answers to every question. A table output alone is not an answer.')
        cells.append(response)
    cells.append(md('''## 6. Explain and review — 15 minutes

Write 150–250 words answering: What is conserved? When is accumulation zero?
Why does a component balance add information? What extra information does a
heat balance need? Give one unit mistake and one physical-limit mistake to avoid.
Swap explanations with your partner and record one clarification. Restart and
run your completed notebook in order. No new Python code is required.
'''))
    if solution:
        cells.append(md('''**Example final explanation**

A balance relates what crosses a chosen boundary to what changes inside it.
Total mass is conserved, and in these nonreacting cases salt is conserved too.
In the mixer, adding water increases total outlet flow but leaves salt flow at
8 kg/h. The component balance determines concentration, information that the
total mass equation alone cannot supply. In the evaporator it distinguishes
water vapour from the salt-bearing product.

Accumulation is zero when the stored quantity does not change. Constant inlet
and outlet rates are not sufficient: the tank gains 0.5 kg each second because
its rates differ. A constant total inventory also does not establish constant
temperature or composition without their own balances.

Energy calculations require appropriate enthalpy or heat-capacity data and
assumptions about heat loss, work and phase changes. Our heater requires
250.8 kW transferred to water; converting that to electrical input needs an
additional efficiency model. Multiplying by two hours gives 501.6 kWh of heat.

I would avoid mixing kg/h with kg/s and would always convert minutes to seconds
before using SI flow rates. I would also stop a constant-flow tank prediction
at emptying or overflow, rather than accepting impossible negative inventory
or contents above capacity. Checks establish internal consistency; measurements
are still needed to validate a model of real equipment.
'''))
    cells.append(md('''## Optional practice — up to three additional hours

Use the same equations and supplied cells; no new algorithms are needed.

- Make a 6 wt% mixer product from the original 80 kg/h, 10 wt% inlet. Distinguish
  total water feed from the extra water relative to the original case.
- Set evaporator product to the feed's 8 wt%. Explain the result. Then explain
  why a requested 5 wt% product is outside this operation's assumptions.
- Heat 1 kg/s water from 15 to 55 °C and calculate heat over four hours.
- Set tank outflow to 2 and then 2.5 kg/s. Identify constant inventory or
  emptying and explain why the original ten-minute prediction can fail.
- Draw a mixer followed by an evaporator. Write balances around each unit and
  around both together. Explain why the internal connecting stream cancels.
'''))
    if solution:
        cells.append(md('''**Optional-practice answers**

- At 6 wt%, total product is 8/0.06 = 133.333 kg/h; pure-water feed is
  53.333 kg/h, or 33.333 kg/h additional to the original water feed.
- At 8 wt%, product is 100 kg/h and vapour is zero. A 5 wt% target would
  require negative vapour flow; dilution, not evaporation, is needed.
- Heating duty is 1(4180)(55−15) = 167200 W = 167.2 kW; four-hour heat
  is 668.8 kWh. This is not automatically electrical energy.
- At 2 kg/s outflow the inventory remains 50 kg. At 2.5 kg/s the tank
  empties after 50/0.5 = 100 s = 1.667 min. A ten-minute continuation is invalid.
- For the coupled original mixer/evaporator, overall mass is 80 + 20 = 40 + 60
  kg/h. Overall salt is 80(0.10) = 40(0.20) = 8 kg/h. The 100 kg/h internal
  stream is an outlet of one unit and inlet of the next, so cancels when summed.
'''))
    notebook=nbformat.v4.new_notebook(cells=cells,metadata={
        'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
        'language_info':{'name':'python'},'teaching_variant':'introductory-balances'})
    nbformat.validate(notebook)
    if execute:
        from nbclient import NotebookClient
        NotebookClient(notebook,timeout=90,kernel_name='python3',
                       resources={'metadata':{'path':str((ROOT/'lab_00').resolve())}}).execute()
    destination=ROOT/'lab_00'/('lab_solution.ipynb' if solution else 'lab.ipynb')
    nbformat.write(notebook,destination)
    print('Built '+str(destination),flush=True)
