"""Check editable design scenarios and conservation checks in supplied analyses."""
from pathlib import Path
import os
import subprocess
import sys
import nbformat

ROOT = Path(__file__).parent.resolve()

# Each tuple changes an actual editable section; later cells must use the change.
SCENARIOS = {
    'lab_01_flow': [
        ('higher electricity price changes diameter choice',
         {1:'selected_diameter = .065',2:'electricity_price = .40'},
         'assert chosen["flow"] == .003\nassert diameters[best_index] == .065\nassert chosen["feasible"]'),
        ('higher fixed duty has no feasible single-pump candidate',
         {1:'required_flow_Lps = 6.0'},
         'assert not feasible_mask.any()\nassert best_index is None\nassert arrangement_results[("A","parallel")]["feasible"]')],
    'lab_02_heat': [
        ('no fouling allowance', {2:'design_R = 0.0'},
         'assert np.isclose(fouled_sized_area,area)\nassert np.isclose(enlarged_design[1],55)'),
        ('larger allowance and narrower flow range', {2:'design_R = .001',
                                                     3:'cold_flow_low = .8\ncold_flow_high = 1.2'},
         'assert fouled_sized_area > area\nassert np.isclose(enlarged_design[1],55)'),
        ('free backup electricity favours lower capital', {2:'trim_electricity_price = 0.0'},
         'assert np.isclose(heat_best["area"],8.13059)\nassert heat_best["trim_kw"]>0')],
    'lab_03_distillation': [
        ('low reflux with less efficient trays', {1:'R = 1.6', 3:'selected_tray_efficiency = .50'},
         'assert N_ideal > 11\nassert selected_trays == int(np.ceil((N_ideal-1)/.50))'),
        ('higher reflux and different purity policy', {1:'R = 3.5',
            2:'purity_targets = [.92,.96]\npurity_reflux_multiple = 1.8',
            3:'selected_tray_efficiency = .80'},
         'assert N_ideal < 11\nassert len(purity_results) == 2\nassert selected_trays == int(np.ceil((N_ideal-1)/.80))'),
        ('increased feed constrains reflux policy', {2:'comparison_feed = 120.0'},
         'assert column_best["multiple"]==1.8\nassert column_best["V"]<=190\nassert len(eligible_columns)==1')],
    'lab_04_absorption': [
        ('low solvent rate loses uncertainty margin', {1:'solvent_multiple = 1.1'},
         'assert np.isnan(robustness[-1][2])\nassert np.isclose(Ls,1.1*Lmin)'),
        ('larger solvent rate and alternative internals', {1:'solvent_multiple = 2.5',
            2:'absorber_tray_efficiency = .75\nhetp_low = .8\nhetp_high = 1.4'},
         'assert N_abs < 5\nassert np.isclose(packed_heights.min(),N_abs*.8)\nassert Ls > infeasible_min'),
        ('adverse packing performance leaves no eligible design', {2:'design_hetp = 3.0'},
         'assert absorber_best is None\nassert not eligible_absorbers')]
}


def main():
    for folder, scenarios in SCENARIOS.items():
        notebook = nbformat.read(ROOT/folder/'lab.ipynb',as_version=4)
        assert notebook.metadata['teaching_variant'] == 'design-support'
        analyses = [c for c in notebook.cells if 'design_analysis' in c.metadata]
        decisions = [c for c in notebook.cells if 'design_answer' in c.metadata]
        assert len(analyses) == len(decisions) == 4
        assert all('# TODO:' not in c.source for c in notebook.cells)
        for name, overrides, checks in scenarios:
            sources = []
            for cell in notebook.cells:
                if cell.cell_type != 'code':
                    continue
                source = cell.source
                section = cell.metadata.get('design_settings')
                if section in overrides:
                    source += '\n' + overrides[section]
                sources.append(source)
            result = subprocess.run([sys.executable,'-c','\n\n'.join(sources+[checks])],
                                    cwd=ROOT/folder, capture_output=True, text=True,
                                    encoding='utf-8', timeout=90,
                                    env=dict(os.environ,MPLBACKEND='Agg',PYTHONIOENCODING='utf-8'))
            if result.returncode:
                raise AssertionError(f'{folder}: {name}\n{result.stdout}\n{result.stderr}')
            print(f'{folder}: {name} — passed',flush=True)
    print(f'All {sum(len(cases) for cases in SCENARIOS.values())} changed-setting scenarios passed.')


if __name__ == '__main__':
    main()
