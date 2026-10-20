"""Build and execute separate instructor notebooks without editing student files.

Usage: python build_solutions.py [--no-execute]
Requires nbclient and a working Python 3 Jupyter kernel for execution.
"""
from pathlib import Path
import argparse
import copy
import os
import textwrap
import nbformat
from nbclient import NotebookClient
from solution_content import SOLUTIONS

ROOT = Path(__file__).parent.resolve()


def markdown(source):
    return nbformat.v4.new_markdown_cell(textwrap.dedent(source).strip())


def code(source):
    return nbformat.v4.new_code_cell(textwrap.dedent(source).strip())


def build(execute=True):
    for folder, answers in SOLUTIONS.items():
        student = ROOT / folder / 'lab.ipynb'
        notebook = copy.deepcopy(nbformat.read(student, as_version=4))
        cells = []
        task = 0
        for cell in notebook.cells:
            if cell.cell_type == 'code' and '# TODO:' in cell.source:
                cell = code(answers['tasks'][task][0])
            elif cell.cell_type == 'markdown' and cell.source.startswith('**Your interpretation:**'):
                cell = markdown('**Solution and interpretation**\n\n' + answers['tasks'][task][1])
                task += 1
            cells.append(cell)
            if cell.cell_type == 'markdown' and cell.source.startswith('**Try a small change:**'):
                cells.extend([markdown('### Solution to the small change\n\n' + answers['warmup'][0]),
                              code(answers['warmup'][1])])
            if cell.cell_type == 'markdown' and cell.source.startswith('## 6.'):
                cells.append(markdown('### Example engineering recommendation\n\n' + answers['recommendation']))
                cells.append(markdown('**Review note:** This is an instructor model answer. '
                                      'The checks below document a self-review; no student peer '
                                      'discussion or real equipment validation is claimed.'))
            if cell.cell_type == 'markdown' and cell.source.startswith('## Optional extension'):
                cells.extend([markdown('### Extension solution\n\n' + answers['extension'][0]),
                              code(answers['extension'][1])])
        if task != 4:
            raise ValueError(f'{folder}: expected four task placeholders, found {task}')
        cells.insert(1, markdown('**Instructor solution — completed reference notebook.**\n\n'
                                + answers['prediction'] + '\n\n'
                                'All exercises, including the small-change example and optional '
                                'extension, are answered below. Use the matching `helpers.py` '
                                'from this folder. Stage counts follow the student notebook conventions.'))
        # Explicit inline backend ensures plots are stored in notebook outputs.
        first_code = next(i for i, c in enumerate(cells) if c.cell_type == 'code')
        cells.insert(first_code, code('%matplotlib inline'))
        notebook.cells = cells
        notebook.cells[0].source += '\n\n**Completed solution**'
        notebook.metadata['solution_source'] = 'build_solutions.py and solution_content.py'
        nbformat.validate(notebook)
        if execute:
            client = NotebookClient(notebook, timeout=120, kernel_name='python3',
                                    resources={'metadata': {'path': str(ROOT / folder)}})
            client.execute()
            for cell in notebook.cells:
                if cell.cell_type == 'code':
                    if cell.execution_count is None:
                        raise AssertionError('Unexecuted solution cell')
                    if any(o.output_type == 'error' for o in cell.outputs):
                        raise AssertionError('Solution contains an error output')
        destination = ROOT / folder / 'lab_solution.ipynb'
        nbformat.write(notebook, destination)
        print(f'{destination.relative_to(ROOT)}: {"executed with outputs" if execute else "built without execution"}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-execute', action='store_true')
    parser.add_argument('--runtime-dir', type=Path,
                        help='Optional writable directory for Jupyter/IPython execution state')
    args = parser.parse_args()
    if args.runtime_dir:
        for variable, child in [('JUPYTER_DATA_DIR','data'), ('JUPYTER_CONFIG_DIR','config'),
                                ('JUPYTER_RUNTIME_DIR','runtime'), ('IPYTHONDIR','ipython')]:
            directory = args.runtime_dir.resolve()/child
            directory.mkdir(parents=True, exist_ok=True)
            os.environ[variable] = str(directory)
    build(execute=not args.no_execute)
