# Design workshops — Kemisk apparatteknik (1KB705)

The **main course labs are Lab 01 (flow and pumps) and Lab 02 (distillation)**.
Use Lab 00 for preparation. Heat recovery and absorption are
**optional self-study extras** for interested students, with no required submission
or assessment. They are not prerequisites for the main labs.

Recommended route: **Lab 00 (as needed) → Lab 01 → Lab 02**. Explore heat
or absorption independently if interested; each includes worked examples, a helper
file and a complete solution for self-checking. The main labs are numbered 01 and 02; optional folders
are grouped by their role. Use the updated paths below for notebooks and Colab.

```text
preparation/
  lab_00_balances/
main_labs/
  lab_01_flow/
  lab_02_distillation/
optional_labs/
  heat/
  absorption/
```

Each lab folder contains its student notebook, solution notebook and `helpers.py`.

Each also has a separate **tutor guide** with step-by-step explanations of the
worked examples and solution questions, numerical checkpoints, common errors,
and suggested prompts for helping students:

- [Lab 00 tutor guide](preparation/lab_00_balances/TUTOR_GUIDE.md)
- [Lab 01 tutor guide](main_labs/lab_01_flow/TUTOR_GUIDE.md)
- [Lab 02 tutor guide](main_labs/lab_02_distillation/TUTOR_GUIDE.md)
- [Heat tutor guide](optional_labs/heat/TUTOR_GUIDE.md)
- [Absorption tutor guide](optional_labs/absorption/TUTOR_GUIDE.md)

These guides contain answers and are intended for tutors. Exclude
`TUTOR_GUIDE.md` files from a student-only distribution if answers are withheld.

Start with **`preparation/lab_00_balances`**, an introductory workshop on choosing system boundaries
and writing elementary total-mass, component and heat balances. It includes
mixing, splitting, water evaporation (mass balance only), stream heating,
adiabatic temperature mixing and tank accumulation. Students write equations
and units before running supplied checks. No programming or prior balance
course is assumed. Plan about three hours of core work, with optional practice
up to four hours. A separate completed `lab_solution.ipynb` is included.

The two main labs are each scoped for approximately **four hours** of student
work: about 8 hours total, excluding preparation. The optional labs each offer
a four-hour self-study route plus further exploration, which may be explored selectively at your own pace.
This **`jolla-design-support`** branch provides a version with less coding and
more engineering design. The original programming-oriented version remains on
`jolla`. Students run supplied numerical routines, change clearly marked
**DESIGN SETTINGS**, compare alternatives, and write their recommendations.
No Python algorithms, loops or plotting code need to be written or assessed.

| Folder | Design problem | Course role | Student decisions |
| --- | --- | --- | --- |
| [preparation/lab_00_balances](preparation/lab_00_balances/lab.ipynb) | First mass and heat balances | Preparation | Write equations, check assumptions and physical limits |
| [main_labs/lab_01_flow](main_labs/lab_01_flow/lab.ipynb) | Water-transfer line and pump | **Main lab** | Select diameter/speed at fixed delivery and compare lifecycle cost |
| [main_labs/lab_02_distillation](main_labs/lab_02_distillation/lab.ipynb) | Binary separation | **Main lab** | Choose a constrained reflux policy and tray-height assumptions |
| [optional_labs/heat](optional_labs/heat/lab.ipynb) | Heat recovery and fouling | Optional self-study | Choose fouling allowance, area and operating flow |
| [optional_labs/absorption](optional_labs/absorption/lab.ipynb) | Solvent rate and column size | Optional self-study | Choose solvent policy, compare internals and robustness |

Each folder contains `lab.ipynb` and an independent `helpers.py`. There are no
cross-lab imports, API keys, remote data requirements, or repository-specific URLs.

Each notebook starts with a labelled system diagram and a small worked example.
Worked examples and main cases specify their inputs, units and assumptions
separately. Given values, chosen settings and calculated results are distinguished.
`lab_inputs.py` maintains the main-case reference tables; example data and named
constants live in `teaching_materials.py` (Lab 00 uses `balances_intro.py`).
Students first change one parameter, predict the result, and explain what they
observe; they then use the supplied analyses for the main design problem.
Implementation cells are collapsed where the notebook viewer supports it, with
separate editable design settings. Students record requirements, numerical
evidence, a decision and what could change it. They keep at least one rejected
design and explain why it fails or is less attractive.
The diagrams are embedded in the notebooks, so no image downloads are required.

Lab 01 additionally plots synthetic head, pump efficiency, shaft input and electrical
input with BEP and an assumed operating band. Its core compares diameters at
exactly 3 L/s using speed control, then compares illustrative pipe-plus-electricity
costs. Parts 5 (pump arrangements) and 6 (separate report) have been removed;
Part 4 ends with a brief decision in the notebook. Pump curves, operating limits and installed costs
are teaching assumptions, not equipment specifications. Shaft energy and electrical
energy are distinguished; motor and drive losses are included.

distillation and the optional workshops use the same design-workshop approach, with added service-boundary
diagrams, explicit feasibility constraints, illustrative costs and a core changed-
duty or robustness challenge:

- **Heat recovery:** compare exchanger area plus electric trim heating at equal
  delivered water flow/temperature; test clean and more-fouled conditions. The
  selected area is used in the subsequent operating-flow envelope.
- **Distillation:** compare six reflux policies under active-height and vapour-
  capacity limits, with an explicitly assumed latent-heat utility model; repeat
  at increased feed. Screen feasibility before comparing illustrative costs.
- **Absorption:** choose solvent circulation and packed height at adverse
  equilibrium and HETP, enforcing the same removal and a six-metre active-height
  limit; distinguish minimum height from minimum modelled service cost.

These tasks share each workshop's four-hour route; they do not require new
student algorithms. All price/limit/utility assumptions are stated in the lab.

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

Assessment and submission guidance below applies to **Labs 01 and 02 only**.
Lab 00 is preparation/practice. the optional heat and absorption labs are optional, unassessed self-study;
their questions, recommendations and solutions are learning aids, not submission
requirements. No optional-lab result is needed to complete the main route.

Main Lab 01 uses 20/60/70/90 minutes for Parts 1–4, including a short
break and a 100–150 word decision in Part 4; there is no separate report.
Main Lab 02 uses 30/40/50/65/30/25 minutes for Parts 1–6, including a break
and a 100–150 word recommendation. The broad purity sweep is reference material.
Each totals four hours. Optional workshops have a four-hour suggested route;
their robustness section and extensions are further exploration. Pilot these
timings with students; they are workload estimates, not measured completion times.

Suggested assessment: balances, units and model understanding 25%; design choices
and tradeoffs 35%; robustness and limitations 25%; clear, reproducible reporting
15%. Students should submit a completed notebook and its
100–150 word decision (in Part 4 for flow, Part 6 for distillation). Grade reasoning and checks, not matching a single
rounded stage count. No marks are assigned for writing Python. `INSTRUCTOR_NOTES.md` contains benchmark results; remove it
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

`four_hour_format.py` maintains the four-hour routes, removes flow Parts 5 and 6,
and keeps student and solution scopes aligned. The optional robustness sections
remain available as further exploration outside their four-hour routes.

```sh
python build_labs.py
python validate_labs.py
python validate_design_labs.py
```

`flow_workshop.py` is the current Lab 01 content source; its numerical routines
and plotting functions live in `main_labs/lab_01_flow/helpers.py`. It overrides the older
flow template retained in the common builder. `flow_solution.py` holds its current
question-by-question instructor answers. Use `python build_labs.py --lab main_labs/lab_01_flow`
and `python build_solutions.py --lab main_labs/lab_01_flow` for a targeted rebuild.

`balances_intro.py` holds Lab 00's instructions, diagrams and model answers;
its independent numerical checks are in `preparation/lab_00_balances/helpers.py`. Build with
`python build_labs.py --lab preparation/lab_00_balances` and
`python build_solutions.py --lab preparation/lab_00_balances`. The usual `--runtime-dir` option
is also available for executing its solution in a restricted environment.
The introductory authoring module contains answers; student distributions need
only its notebook and matching helper file.

`workshop_extensions.py` supplies the core comparison prompts, diagrams and
analysis cells for distillation and the optional workshops; their numerical design comparisons live in each
lab's own `helpers.py`. `workshop_solutions.py` adds the matching discussions
and updated recommendation openings. Use `--lab` with the corresponding folder
to rebuild only one lab and its solution.

`build_labs.py` and `teaching_materials.py` hold the common cases, diagrams and
worked examples. `design_materials.py` replaces implementation exercises with
design questions and settings; `design_calculations.py` supplies the analysis
code. Edit these sources and rebuild when changing student instructions; helper
modules are edited directly. Validation checks
notebook structure, executes every supplied code cell in a separate process per
lab with a headless plotting backend, and checks physical benchmarks. Design
scenario checks also exercise changed settings, including infeasible throughput
requirements. Numerical calculations are complete in student notebooks; written
decisions and recommendations remain open.
Choose a repository licence before public release.

## Completed instructor solutions

Each lab folder also has a separate **`lab_solution.ipynb`** with all exercise
cells filled, written interpretations, a model engineering recommendation and
the optional extension. The small-change exercises are answered too. The files
include executed code outputs and plots, and use the same local `helpers.py` as
their student counterpart. Rebuilding solutions leaves student `lab.ipynb` files unchanged.

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
Lab 01's current worked answers live in `flow_solution.py`. The original worked
answers for the other labs live in `solution_content.py`. Question-by-question
design discussions and additional reference comparisons live in
`solution_discussion.py`; they explicitly address the questions in each design
section, using the default settings. The builder transfers these answers
into copies of the student notebooks and checks every code cell executes.
Keep solution files, `flow_solution.py`, `solution_content.py`, `solution_discussion.py`, `build_solutions.py` and the instructor
notes out of a student-only distribution if answers should be withheld.
Also withhold `workshop_solutions.py` from a student-only distribution.
