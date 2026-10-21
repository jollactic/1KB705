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
        ('smaller pipe and higher duty', {0:'diameter = .050', 1:'required_flow_Lps = 4.5',
                                        2:'selected_diameter = .080\nselected_speed = 1.1'},
         'assert diameter == .050\nassert chosen_D == .080 and chosen_speed == 1.1\nassert chosen_result[0]*1000 >= required_flow_Lps'),
        ('no feasible candidate', {1:'required_flow_Lps = 6.0',
                                   2:'selected_diameter = .050\nselected_speed = .8'},
         'assert not feasible_designs\nassert not robust\nassert chosen_result[0]*1000 < required_flow_Lps')],
    'lab_02_heat': [
        ('no fouling allowance', {2:'design_R = 0.0'},
         'assert np.isclose(fouled_sized_area,area)\nassert np.isclose(enlarged_design[1],55)'),
        ('larger allowance and narrower flow range', {2:'design_R = .001',
                                                     3:'cold_flow_low = .8\ncold_flow_high = 1.2'},
         'assert fouled_sized_area > area\nassert np.isclose(enlarged_design[1],55)')],
    'lab_03_distillation': [
        ('low reflux with less efficient trays', {1:'R = 1.6', 3:'selected_tray_efficiency = .50'},
         'assert N_ideal > 11\nassert selected_trays == int(np.ceil((N_ideal-1)/.50))'),
        ('higher reflux and different purity policy', {1:'R = 3.5',
            2:'purity_targets = [.92,.96]\npurity_reflux_multiple = 1.8',
            3:'selected_tray_efficiency = .80'},
         'assert N_ideal < 11\nassert len(purity_results) == 2\nassert selected_trays == int(np.ceil((N_ideal-1)/.80))')],
    'lab_04_absorption': [
        ('low solvent rate loses uncertainty margin', {1:'solvent_multiple = 1.1'},
         'assert np.isnan(robustness[-1][2])\nassert np.isclose(Ls,1.1*Lmin)'),
        ('larger solvent rate and alternative internals', {1:'solvent_multiple = 2.5',
            2:'absorber_tray_efficiency = .75\nhetp_low = .8\nhetp_high = 1.4'},
         'assert N_abs < 5\nassert np.isclose(packed_heights.min(),N_abs*.8)\nassert Ls > infeasible_min')]
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
    print('All eight changed-setting scenarios passed.')


if __name__ == '__main__':
    main()
