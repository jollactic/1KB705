"""Execute supplied cells and verify independent physical/numerical benchmarks."""
from pathlib import Path
import importlib.util
import math
import os
import subprocess
import sys
import nbformat
import numpy as np

ROOT = Path(__file__).parent.resolve()


def load(folder):
    spec = importlib.util.spec_from_file_location(folder, ROOT/folder/'helpers.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def close(actual, expected, **kwargs):
    assert np.isclose(actual, expected, **kwargs), (actual, expected)


def rejects(function, *args):
    try:
        function(*args)
    except ValueError:
        return
    raise AssertionError(f'{function.__name__} accepted invalid input')


def main():
    for folder in sorted(ROOT.glob('lab_*')):
        if not folder.is_dir():
            continue
        notebook = nbformat.read(folder/'lab.ipynb', as_version=4)
        nbformat.validate(notebook)
        supplied_code = '\n\n'.join(c.source for c in notebook.cells if c.cell_type == 'code')
        environment = dict(os.environ, MPLBACKEND='Agg', PYTHONIOENCODING='utf-8')
        result = subprocess.run([sys.executable, '-c', supplied_code], cwd=folder,
                                env=environment, capture_output=True, text=True,
                                encoding='utf-8', timeout=60)
        if result.returncode:
            raise AssertionError(f'{folder.name}: {result.stderr}')
        print(f'{folder.name}: valid notebook; supplied code executes')

    intro = load('lab_00')
    total,fraction = intro.mix_streams(80,.1,20)
    close(total,100); close(total*fraction,8)
    product,vapour = intro.evaporate(100,.08,.2)
    close(product+vapour,100); close(product*.2,8)
    close(intro.heating_duty(2,4180,20,50),250800)
    close(intro.mixing_temperature(.5,80,1.5,20),35)
    close(intro.tank_inventory(50,2,1.5,600),350)
    rejects(intro.evaporate,100,.08,.05)
    rejects(intro.tank_inventory,50,2,2.5,600)
    print('Lab 00: basic balances, conservation and model-domain checks passed')

    flow = load('lab_01_flow')
    close(flow.friction_factor(1000, 0), 0.064)
    rejects(flow.friction_factor, 3000, 0)
    # Independent implicit Colebrook solution, compare approximate Haaland within 2%.
    re, rr, f = 100000., 0.001, 0.02
    for _ in range(100):
        f = (-2*math.log10(rr/3.7+2.51/(re*math.sqrt(f))))**-2
    close(flow.friction_factor(re, rr), f, rtol=0.02)
    def residual(q):
        return flow.pump_head(q)-flow.system_head(q, .065, 120, 12, 4.5e-5, 8)
    lo, hi = .001, .005
    assert residual(lo)*residual(hi) < 0
    for _ in range(60):
        mid = (lo+hi)/2
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    q = (lo+hi)/2
    assert abs(residual(q)) < 1e-8
    head = float(flow.pump_head(q))
    point = flow.performance(q)
    close(point['hydraulic'],998*9.81*q*head)
    close(point['electrical']*.90*.96,point['shaft'])
    assert not point['recommended']
    assert flow.performance(0)['shaft'] > 0 and flow.performance(0)['efficiency'] == 0
    grid = np.linspace(0,flow.RUNOUT_FLOW,1000)
    eta = flow.performance(grid)['efficiency']
    assert np.all((eta >= 0) & (eta <= 1))
    # Affinity scaling at corresponding points must preserve efficiency and scale power cubically.
    rated, slower = flow.performance(.003), flow.performance(.003*.8,.8)
    close(slower['head'],rated['head']*.8**2)
    close(slower['shaft'],rated['shaft']*.8**3)
    close(slower['efficiency'],rated['efficiency'])
    for arrangement in ['single','series','parallel']:
        row = flow.design_at_flow(.003,.065,arrangement=arrangement)
        close(flow.arrangement_head(.003,row['speed'],arrangement),row['head'])
        close(row['shaft']*row['efficiency'],998*9.81*.003*row['head'])
        close(row['annual_kwh'],row['specific_kwh']*.003*3600*4000)
    assert flow.design_at_flow(.006,.08,arrangement='parallel')['feasible']
    assert not flow.design_at_flow(.006,.08)['feasible']
    assert flow.design_at_flow(.003,.08,rise=55,arrangement='series')['feasible']
    assert not flow.design_at_flow(.003,.08,rise=55)['feasible']
    rejects(flow.performance,flow.RUNOUT_FLOW*1.01)
    print(f'Flow uncontrolled base: Q={1000*q:.6f} L/s, H={head:.6f} m, electrical={point["electrical"]:.6f} W')

    heat = load('lab_02_heat')
    close(heat.lmtd(20, 20), 20)
    rejects(heat.lmtd, -1, 20)
    close(heat.countercurrent_effectiveness(2, 1), 2/3)
    close(heat.countercurrent_effectiveness(0, .5), 0)
    close(heat.countercurrent_effectiveness(100, .5), 1)
    duty, ch, cc = 4180*40, 1.2*3800, 4180
    tho = 85-duty/ch
    area = duty/(650*heat.lmtd(30, tho-15))
    ho, co, recovered = heat.outlets(650*area, ch, cc, 85, 15)
    close(co, 55); close(ho, tho); close(recovered, duty)
    close(ch*(85-ho), cc*(co-15))
    fouled = heat.outlets(area/(1/650+.0006), ch, cc, 85, 15)
    assert fouled[1] < co
    print(f'Heat base: duty={duty/1000:.3f} kW, Tho={tho:.6f} C, A={area:.6f} m²; fouled Tco={fouled[1]:.6f} C')
    heat_candidates = heat.compare_designs()
    assert np.isclose(min(heat_candidates,key=lambda r:r['total'])['area'],11.30152)
    for row in heat_candidates:
        assert row['recovery_kw']+row['trim_kw'] >= 167.2-1e-8
        close(row['annual_kwh'],row['trim_kw']*4000)
    assert np.isclose(min(heat.compare_designs(0),key=lambda r:r['total'])['area'],8.13059)

    dist = load('lab_03_distillation')
    x = np.linspace(0, 1, 50)
    assert np.allclose(dist.inverse_equilibrium(dist.equilibrium(x)), x)
    rmin = dist.minimum_reflux(.45, .95)
    rejects(dist.stage_count, .45, .95, .05, rmin)
    stages, points = dist.stage_count(.45, .95, .05, 2.5)
    assert points[-1, 0] <= .05
    assert dist.stage_count(.45, .95, .05, 4)[0] <= stages
    # At near-total reflux the integer counter agrees with the Fenske minimum.
    fenske = math.log((.95/.05)*(.95/.05))/math.log(2.4)
    assert dist.stage_count(.45, .95, .05, 1e9)[0] == math.ceil(fenske)
    D = 100*(.45-.05)/(.95-.05)
    close(D*.95+(100-D)*.05, 45)
    print(f'Distillation base: D={D:.6f} kmol/h, Rmin={rmin:.6f}, ideal stages={stages}')
    column_candidates = dist.compare_designs()
    feasible_columns = [r for r in column_candidates if r['feasible']]
    close(min(feasible_columns,key=lambda r:r['total'])['multiple'],1.8)
    for row in column_candidates:
        close(row['duty_kw'],row['V']*30000/3600)
        assert row['feasible'] == (row['height']<=8 and row['V']<=190)
    assert [r['multiple'] for r in dist.compare_designs(120) if r['feasible']]==[1.8]

    absorb = load('lab_04_absorption')
    lmin = 100*(.03-.003)/(.03/1.5)
    solvent = 1.5*lmin
    count, points = absorb.stage_count(100, solvent, .03, .003)
    # Independent closed-form recurrence for fresh solvent: Y_(N+1)/Yout = sum A^k.
    A = solvent/(100*1.5)
    required = math.ceil(math.log(1+(.03/.003)*(A-1), A)-1)
    assert count == required
    assert points[-1, 1] >= .03
    rejects(absorb.stage_count, 100, lmin, .03, .003)
    close(absorb.ergun_gradient(0, .7, .025), 0)
    gradient = absorb.ergun_gradient(.8, .7, .025)
    print(f'Absorption base: Lmin={lmin:.6f}, L={solvent:.6f} kmol/h, ideal stages={count}, dry gradient={gradient:.6f} Pa/m')
    absorber_candidates = absorb.compare_designs()
    feasible_absorbers = [r for r in absorber_candidates if r['feasible']]
    close(min(feasible_absorbers,key=lambda r:r['total'])['solvent'],243)
    assert not absorber_candidates[0]['feasible'] and np.isnan(absorber_candidates[0]['total'])
    assert not absorber_candidates[1]['feasible']  # nominal choice violates adverse height
    assert not any(r['feasible'] for r in absorb.compare_designs(hetp=3))
    print('All benchmark, design-service and invalid-input checks passed.')


if __name__ == '__main__':
    main()
