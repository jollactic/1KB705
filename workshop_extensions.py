"""Core design comparisons for Labs 2–4; supplied analysis, no student coding."""

def design_diagram(folder):
    """Embedded block diagram of the added design-service boundary."""
    from io import BytesIO
    import base64
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,FancyArrowPatch
    fig,ax = plt.subplots(figsize=(12,3.4))
    ax.set(xlim=(0,12),ylim=(0,3.4)); ax.axis('off')
    labels = {
        'lab_02_heat':['Cold feed\n1 kg/s, 15 °C','Heat recovery\nArea A, fouled U','Electric trim heater\nPositive duty deficit','Required service\n1 kg/s, 55 °C'],
        'lab_03_distillation':['Feed\nF, zF = 0.45','Distillation column\nActive height ≤ 8 m','Products\nxD = 0.95, xB = 0.05'],
        'lab_04_absorption':['Gas feed\nGs = 100, Yin = 0.03','Absorber\nActive packing ≤ 6 m','Cleaned gas\nYout = 0.003']
    }[folder]
    positions = [0.1,3.1,6.1,9.1] if len(labels)==4 else [.1,4.6,9.1]
    for pos,label in zip(positions,labels):
        ax.add_patch(Rectangle((pos,1.3),2.7,1.1,fc='#edf5fc',ec='#204060',lw=1.7))
        ax.text(pos+1.35,1.85,label,ha='center',va='center',fontsize=10)
    def arrow(start,end,color='steelblue'):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle='->',mutation_scale=13,lw=2,color=color))
    for left,right in zip(positions[:-1],positions[1:]):
        arrow((left+2.7,1.85),(right,1.85))
    center = positions[1]+1.35
    upper = {'lab_02_heat':'Hot process stream supplies recovered heat',
             'lab_03_distillation':'Condenser and reflux: V ≤ 190 kmol/h',
             'lab_04_absorption':'Lean solvent L; nominal/adverse equilibrium'}[folder]
    lower = {'lab_02_heat':'Electrical trim input; compare area + backup electricity cost',
             'lab_03_distillation':'Reboiler heat input: compare utility cost and capacity',
             'lab_04_absorption':'Rich solvent to service/regeneration: compare circulation cost'}[folder]
    ax.text(6,3,upper,ha='center',fontsize=11)
    arrow((center,2.85),(center,2.4),'darkorange')
    ax.text(6,.25,lower,ha='center',fontsize=11)
    lower_center = positions[2]+1.35 if folder=='lab_02_heat' else center
    arrow((lower_center,.6),(lower_center,1.3),'darkorange')
    if folder=='lab_04_absorption':
        # Rich solvent leaves the design boundary rather than supplying heat.
        ax.patches[-1].remove()
        arrow((center,1.3),(center,.6),'darkorange')
    fig.tight_layout()
    stream=BytesIO(); fig.savefig(stream,format='png',dpi=140); plt.close(fig)
    return base64.b64encode(stream.getvalue()).decode('ascii')

SETTINGS = {
 'lab_02_heat': '''\ntrim_electricity_price = 0.10 #@param {type:"number"}
cost_horizon = 10 #@param {type:"number"}''',
 'lab_03_distillation': '''\ncomparison_feed = 100.0 #@param {type:"number"}
comparison_heat_price = 0.03 #@param {type:"number"}''',
 'lab_04_absorption': '''\nrobust_slope = 1.8 #@param {type:"number"}
design_hetp = 1.2 #@param {type:"number"}
solvent_service_price = 60.0 #@param {type:"number"}'''
}

PROMPTS = {
 'lab_02_heat': r'''
**Core design challenge — recover heat, then supply any deficit.** The system
is now an exchanger followed by a trim heater, delivering the same **1 kg/s
at 55 °C** for 4000 h/year. Compare supplied areas 8.13059, 11.30152 and
14 m² at your chosen fouling resistance. The trim heater supplies only the
positive deficit to 167.2 kW, at assumed efficiency one. Excess recovered heat
gets no sale credit; bypass/control would be needed to hold the target.

Illustrative installed exchanger cost is **€4000 + €700 per m²**. Compare
installed cost plus ten years of trim-heater electricity at €0.10/kWh.
Heater capital, hydraulic power, maintenance, cleaning and discounting are
omitted. These are supplied teaching prices, not quotations.

Choose an area, report recovered heat, backup power, annual backup electricity
and total modelled cost. Does your choice change at zero added resistance or
at 0.001 m² K/W? Is the cheapest exchanger also the cheapest way to deliver
the required service? A larger exchanger is not automatically sufficient at
every fouling condition. Explain the control and cleaning assumptions.
''',
 'lab_03_distillation': r'''
**Core design challenge — constrained equipment and heat cost.** Keep the same
feed composition and product specifications. Compare six supplied R/Rmin policies
with overall efficiency 0.65, tray spacing 0.45 m, **maximum active height 8 m**
and **maximum vapour circulation 190 kmol/h**. These are teaching constraints;
the vapour limit stands in for a capacity specification, not a flooding calculation.

For an approximate heat-duty comparison, assume equal latent heats of
30000 kJ/kmol and negligible sensible changes: $Q_R=V\lambda/3600$ kW.
This goes beyond the earlier vapour-load proxy but remains a synthetic energy
model for the hypothetical mixture. Installed cost is €50000 + €3000 per
actual tray + €250 per (kmol/h) of vapour capacity. Add ten years of heat
at €0.03/kWh and 4000 h/year. Cooling, maintenance and discounting are omitted.

Select the least-cost **feasible** policy, identify why other candidates fail,
and compare it with minimum-stage and minimum-heat choices. Then repeat at
**120 kmol/h feed** with unchanged equipment limits. Can the original reflux
policy still meet capacity? If a lower-reflux policy passes, what extra height
does it need? A change in product throughput must be reflected in D and V.
''',
 'lab_04_absorption': r'''
**Core design challenge — a height-limited absorber under uncertainty.** Retain
the same 100 kmol/h solute-free gas feed and **90% removal**. Compare solvent
rates of 1.1, 1.5, 1.8, 2.0 and 2.5 times the nominal minimum of 135 kmol/h.
Screen each at both nominal m = 1.5 and adverse m = 1.8. Use conservative
HETP = 1.2 m and **maximum active packed height 6 m**. This is a height
constraint, not a verified wet-hydraulic capacity.

Illustrative installed packing-section cost is €20000 + €6000 per metre of
required active height. Annual solvent-service cost is €60 per (kmol/h) of
circulation at 4000 h/year. This is a supplied combined service allowance,
not solvent purchase cost or a calculated regeneration duty. Compare ten-year
undiscounted totals. Missing wet hydraulics, internals and maintenance still matter.

Choose a feasible solvent/height combination. Does the nominal five-contact
choice fit the adverse condition? Is the lowest solvent rate actually feasible?
Would minimum height also minimize this cost model? Explain how HETP uncertainty
can change the answer and what extra cost or vendor data would change your choice.
'''
}

ANALYSIS = {
 'lab_02_heat': '''
# Same-service area/backup-heating comparison.
heat_designs = h.compare_designs(design_R,trim_electricity_price,cost_horizon)
print('Area/m²  recovery/kW  trim/kW   trim/kWh/year  capital/€  horizon/€')
for row in heat_designs:
    print(f"{row['area']:7.3f} {row['recovery_kw']:11.3f} {row['trim_kw']:8.3f} {row['annual_kwh']:14.1f} {row['installed']:10.1f} {row['total']:10.1f}")
heat_best = min(heat_designs,key=lambda row:row['total'])
installed_area = heat_best['area']
print(f"Least modelled service cost at selected fouling: {heat_best['area']:.3f} m²")
for test_resistance in [0.,.0006,.001]:
    candidates = h.compare_designs(test_resistance,trim_electricity_price,cost_horizon)
    best = min(candidates,key=lambda row:row['total'])
    print(f"R_f={test_resistance:.4f}: preferred area {best['area']:.3f} m²; backup {best['trim_kw']:.3f} kW")
fig,axes = plt.subplots(1,2,figsize=(11,4))
axes[0].bar([str(round(r['area'],2)) for r in heat_designs],[r['total'] for r in heat_designs])
axes[0].set(xlabel='Installed exchanger area / m²',ylabel='Modelled horizon cost / €')
axes[1].plot(resistance*1e4,fixed_area_results[:,2]/1000,label='Original clean-sized recovery')
axes[1].axhline(167.2,color='black',linestyle=':',label='Required service duty')
axes[1].set(xlabel='Added resistance / (10$^{-4}$ m² K W$^{-1}$)',ylabel='Duty / kW')
axes[1].legend(); axes[1].grid(); plt.tight_layout(); plt.show()
''',
 'lab_03_distillation': '''
# Fixed separation, constrained height/capacity and illustrative heat cost.
column_designs = h.compare_designs(comparison_feed,heat_price=comparison_heat_price)
print('R/Rmin   stages  trays height/m  V/kmol/h  heat/kW  horizon/€  eligible')
for row in column_designs:
    print(f"{row['multiple']:6.2f} {row['stages']:7d} {row['trays']:6d} {row['height']:8.2f} {row['V']:9.2f} {row['duty_kw']:8.2f} {row['total']:10.0f} {row['feasible']}")
eligible_columns = [r for r in column_designs if r['feasible']]
column_best = min(eligible_columns,key=lambda r:r['total']) if eligible_columns else None
print('Chosen constrained policy:',column_best)
for feed_case in [100.,120.]:
    candidates = h.compare_designs(feed_case,heat_price=comparison_heat_price)
    eligible = [r for r in candidates if r['feasible']]
    if eligible:
        best = min(eligible,key=lambda r:r['total'])
        print(f"Feed {feed_case:.0f} kmol/h: choose R/Rmin={best['multiple']:.2f}; height={best['height']:.2f} m, V={best['V']:.2f} kmol/h")
    else:
        print(f'Feed {feed_case:.0f} kmol/h: no screened-feasible policy')
fig,axes = plt.subplots(1,2,figsize=(11,4))
axes[0].plot([r['V'] for r in column_designs],[r['height'] for r in column_designs],'o-')
axes[0].axhline(8,color='black',linestyle=':'); axes[0].axvline(190,color='black',linestyle=':')
axes[0].set(xlabel='Vapour circulation / kmol h$^{-1}$',ylabel='Active height / m')
axes[1].plot([r['multiple'] for r in column_designs],[r['total'] for r in column_designs],'o-')
for ok,color,marker,label in [(True,'green','o','Eligible'),(False,'crimson','x','Rejected by a limit')]:
    subset = [r for r in column_designs if r['feasible']==ok]
    axes[1].scatter([r['multiple'] for r in subset],[r['total'] for r in subset],color=color,marker=marker,s=70,label=label,zorder=3)
axes[1].legend(fontsize=8)
axes[1].set(xlabel='R/Rmin',ylabel='Modelled horizon cost / €')
for axis in axes: axis.grid()
plt.tight_layout(); plt.show()
''',
 'lab_04_absorption': '''
# Same removal; choose solvent and height against adverse equilibrium.
absorber_designs = h.compare_designs(robust_slope,design_hetp,solvent_service_price)
print('L/Lmin   L/kmol/h nominal N adverse N height/m horizon/€ eligible / reason')
for row in absorber_designs:
    print(f"{row['multiple']:6.2f} {row['solvent']:10.1f} {row['nominal']:9d} {row['worst']:9.0f} {row['height']:8.2f} {row['total']:9.0f} {row['feasible']} / {row['reason']}")
eligible_absorbers = [r for r in absorber_designs if r['feasible']]
absorber_best = min(eligible_absorbers,key=lambda r:r['total']) if eligible_absorbers else None
print('Selected robust cost candidate:',absorber_best)
fig,axes = plt.subplots(1,2,figsize=(11,4))
valid = [r for r in absorber_designs if np.isfinite(r['height'])]
axes[0].plot([r['solvent'] for r in valid],[r['height'] for r in valid],'o-')
axes[0].axhline(6,color='black',linestyle=':',label='Active-height limit'); axes[0].legend()
axes[0].set(xlabel='Solvent circulation / kmol h$^{-1}$',ylabel='Adverse-case active height / m')
axes[1].plot([r['solvent'] for r in valid],[r['total'] for r in valid],'o-')
for ok,color,marker,label in [(True,'green','o','Eligible'),(False,'crimson','x','Rejected by height')]:
    subset = [r for r in valid if r['feasible']==ok]
    axes[1].scatter([r['solvent'] for r in subset],[r['total'] for r in subset],color=color,marker=marker,s=70,label=label,zorder=3)
axes[1].legend(fontsize=8)
axes[1].set(xlabel='Solvent circulation / kmol h$^{-1}$',ylabel='Modelled horizon cost / €')
for axis in axes: axis.grid()
plt.tight_layout(); plt.show()
'''
}


def enrich_workshop(notebook,folder,md,code):
    """Extend the existing design-comparison block, not the total lab duration."""
    for cell in notebook.cells:
        if cell.cell_type=='markdown' and cell.source.startswith('## Design workshop:'):
            cell.source += '\n\nThe core comparison block also includes a same-service cost/constraint '
            cell.source += 'challenge. These activities share the existing six-hour budget; prioritize '
            cell.source += 'one checked base case and the supplied comparison tables over extra sweeps.'
        if cell.cell_type=='markdown' and cell.source.startswith('## 4.'):
            cell.source += '\n\n![Service boundary for the design comparison](attachment:design-service.png)\n\n'
            cell.source += 'Block diagram of the design boundary; see the main flowsheet for physical stream connections.\n\n' + PROMPTS[folder]
            cell['attachments'] = {'design-service.png':{'image/png':design_diagram(folder)}}
        if cell.metadata.get('design_settings') == 2:
            cell.source += SETTINGS[folder]
        if cell.metadata.get('design_analysis') == 2:
            cell.source += '\n\n' + ANALYSIS[folder]
        if folder=='lab_02_heat' and cell.metadata.get('design_analysis')==3:
            cell.source = cell.source.replace('design_U*fouled_sized_area','design_U*installed_area')
        if folder=='lab_04_absorption' and cell.cell_type=='markdown' and cell.source.startswith('## 5.'):
            cell.source += '\n\nDistinguish the original solvent-policy sensitivity from the '
            cell.source += 'robust candidate in the preceding core comparison. State whether '
            cell.source += 'you retain or revise the original policy after applying the height limit.'
        if cell.cell_type=='markdown' and cell.source.startswith('## 6.'):
            cell.source += '\n\nInclude your choice from the core cost/constraint table, a rejected '
            cell.source += 'alternative and the effect of the changed duty or adverse condition. '
            cell.source += 'Identify both the energy/circulation criterion and the cost criterion.'
    notebook.metadata['workshop_edition'] = 'constrained-design-v2'
    return notebook
