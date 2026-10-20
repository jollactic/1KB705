# Computational labs — Kemisk apparatteknik (1KB705)

Four draft Jupyter labs, each scoped for approximately **six hours** of student work.
Written in English for pairs, with a runnable example, calculations students must
implement, sensitivity analysis, and an engineering recommendation. No prior
experience with numerical root finding or stage stepping is assumed; allow an
introductory Python session if students have never used arrays and plotting.

| Folder | Design problem | Principal syllabus alignment | Student implementation |
| --- | --- | --- | --- |
| `lab_01_flow` | Water-transfer line and pump | Flowing fluids, pressure losses, pumps | Bernoulli balance and bisection |
| `lab_02_heat` | Heat recovery and fouling | Heat exchangers, energy balances | Effectiveness–NTU and feasibility checks |
| `lab_03_distillation` | Binary separation | Material balances, graphical/numerical stages, efficiency | McCabe–Thiele staircase and tray height |
| `lab_04_absorption` | Solvent rate and column size | Absorption, stages, column height, porous beds | Absorber staircase and hydraulic screening |

Each folder contains `lab.ipynb` and an independent `helpers.py`. There are no
cross-lab imports, API keys, remote data requirements, or repository-specific URLs.

Each notebook starts with a labelled system diagram and a small worked example.
Students first change one parameter, predict the result, and explain what they
observe; they then extend the example to the main design problem. Distillation
and absorption include plots of the first two equilibrium steps. Suggested routes
break the larger tasks into balance, calculation, iteration and interpretation.
The diagrams are embedded in the notebooks, so no image downloads are required.

## Run locally

From the repository root:

```sh
python -m venv .venv
# Activate the virtual environment using your platform's usual command.
python -m pip install -r requirements.txt
jupyter notebook
```

Open a notebook inside its lab folder so that its matching `helpers.py` is on the
Python import path. Use a separate kernel for each lab: all four helper modules
share the name `helpers`, which Python caches within a running kernel.

## Run in Colab

Upload `lab.ipynb` and the matching `helpers.py` from one folder. The notebook's
first code cell also supports downloading the helper from a raw GitHub URL once
you publish the repository. Set `HELPER_URL` to the actual owner, repository,
commit and lab path. No GitHub account or URL is assumed by this draft.
Colab normally supplies NumPy and Matplotlib. The notebooks use no SciPy features.

## Teaching and assessment

The six-hour estimate includes setup (30 min), model development (75 min),
numerical work (90 min), design comparison (75 min), sensitivity and a break
(45 min), and reporting (45 min). Pilot these timings with a small student group;
they are estimates, not measured completion times. Extensions are optional.

Suggested assessment: physical model and assumptions 25%; numerical correctness
and balance checks 30%; sensitivity and engineering judgement 25%; clear,
reproducible reporting 20%. Students should submit a completed notebook and its
300–500 word recommendation. Grade reasoning and checks, not matching a single
rounded stage count. `INSTRUCTOR_NOTES.md` contains benchmark results; remove it
from a student distribution if you want to withhold those values.

These computational exercises cover selected outcomes. They do not cover all
syllabus topics: evaporation, drying, extraction/leaching, mixing, filtration,
fluidisation and sedimentation need other teaching activities. They also do not
establish that the course's compulsory physical laboratory requirements can be
replaced; that decision belongs to the course examiner.

## Source and model provenance

The requested [Uppsala syllabus](https://www.uu.se/utbildning/kursplan?query=38474)
identifies the 10-credit course and its flow, heat-transfer and separation outcomes.
That page is marked as an older version (adopted 2018); this draft deliberately
targets the linked version. Confirm the intended course version before adoption.

For instructional background and independent diagrams, see the University of
Colorado Boulder's [LearnChemE separations teaching materials](https://learncheme.com/screencasts/separations-mass-transfer/)
and MIT's [Transport Processes laboratory materials](https://www.ocw.mit.edu/courses/10-302-transport-processes-fall-2004/pages/labs/).
The notebooks and synthetic cases here are newly authored; external materials
are reading links, not copied exercises or datasets. All model equations and
stage-count conventions are stated in the notebooks/helper docstrings.

## Maintainer checks

```sh
python build_labs.py
python validate_labs.py
```

The builder and `teaching_materials.py` are the notebook content sources. The
latter holds the system-diagram drawing code and worked examples. Edit these and
rebuild when changing student instructions; helper modules are edited directly. Validation checks
notebook structure, executes every supplied code cell in a separate process per
lab with a headless plotting backend, and checks physical benchmarks. Student
TODO cells intentionally contain comments and are not completed solutions.
Choose a repository licence before public release.

## Completed instructor solutions

Each lab folder also has a separate **`lab_solution.ipynb`** with all exercise
cells filled, written interpretations, a model engineering recommendation and
the optional extension. The small-change exercises are answered too. The files
include executed code outputs and plots, and use the same local `helpers.py` as
their student counterpart. Student `lab.ipynb` files remain unchanged.

Solutions can be opened directly without rerunning to read the saved results.
To rerun in Colab, upload the solution notebook and its matching helper file.
The distillation extension uses clearly labelled synthetic equilibrium samples
because no real instructor dataset was provided; the absorption extension uses
an explicitly assumed transfer-unit height.

Rebuild and execute instructor solutions after updating student notebooks:

```sh
python build_solutions.py
```

This requires the `nbclient` and `ipykernel` dependencies in `requirements.txt`.
For environments with restricted access to the user profile, use
`python build_solutions.py --runtime-dir .jupyter_runtime`.
Use `--no-execute` only when intentionally generating notebooks without outputs.
The authored answers live in `solution_content.py`; the builder transfers them
into copies of the student notebooks and checks every code cell executes.
Keep solution files, `solution_content.py`, `build_solutions.py` and the instructor
notes out of a student-only distribution if answers should be withheld.
