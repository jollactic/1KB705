"""Four-hour teaching routes, applied to both student and solution notebooks."""
import re


def apply_four_hour_format(notebook,folder):
    flow=folder=='main_labs/lab_01_flow'
    distillation=folder=='main_labs/lab_02_distillation'
    optional=folder.startswith('optional_labs/')
    cells=[]
    omit=False
    for cell in notebook.cells:
        if cell.cell_type=='markdown':
            if flow and re.match(r'## [56]\.',cell.source):
                omit=True
            elif cell.source.startswith('## Optional'):
                omit=False
        if omit:
            continue
        if cell.cell_type=='markdown':
            s=cell.source
            s=s.replace('Lab 3','Lab 02').replace('Lab 1','Lab 01')
            s=s.replace('Lab 2 — Heat recovery','Heat — Heat recovery').replace('Lab 4 — Gas absorption','Absorption — Gas absorption')
            if s.startswith('# '):
                title={'main_labs/lab_01_flow':'# Lab 01 — Pipe flow and pump selection',
                       'main_labs/lab_02_distillation':'# Lab 02 — Binary distillation and ideal stages',
                       'optional_labs/heat':'# Heat — Heat recovery and fouling',
                       'optional_labs/absorption':'# Absorption — Gas absorption and column height'}.get(folder)
                if title:
                    s=title+'\n'+s.partition('\n')[2]
            if flow or distillation:
                s=s.replace('**Time budget: 6 hours, including a short break and submission.**',
                            '**Time budget: 4 hours, including a short break and submission.**')
                s=s.replace('300–500 words','100–150 words').replace('300–500 word','100–150 word')
                s=s.replace('outside the six-hour budget','outside the four-hour budget')
            if s.startswith('## Design workshop:'):
                if flow:
                    s='''## Four-hour route — run, compare, decide

Complete Parts 1–4 only. All calculations and plots are supplied; edit only
DESIGN SETTINGS. After changing an input, rerun that section and the sections
below it. Keep one feasible choice and one rejected alternative with evidence.

**Schedule:** Part 1 setup/prediction 20 min; Part 2 curves and energy 60 min;
Part 3 fixed-delivery diameter comparison 70 min; Part 4 cost, robustness and
brief decision 90 min, including a 10-minute break. Total: 240 minutes.
Parts 5 (pump arrangements) and 6 (separate report) have been removed.
End Part 4 with a 100–150 word decision in its answer cell; no separate report
is required. Optional exploration is outside the four-hour route.'''
                elif distillation:
                    s='''## Four-hour route — run, compare, decide

All calculations and plots are supplied. Focus on the base separation and the
height/capacity comparison; no algorithms or additional parameter sweeps are
required. Use Lab 00 for balance preparation if needed.

**Schedule:** Part 1 setup/prediction 30 min; Part 2 balances 40 min;
Part 3 stage construction 50 min; Part 4 constrained reflux choice 65 min,
including a 10-minute break; Part 5 tray/height interpretation 30 min;
Part 6 brief recommendation 25 min. Total: 240 minutes. The extra purity
and broad reflux sweeps are supplied reference plots, not extra assessed tasks.
Optional exploration is outside this route.'''
                elif optional:
                    s='''## Optional four-hour self-study route

Run the worked example and supplied analyses; no Python algorithms are required.
Suggested pace: setup 20 min; Part 2 balances 40 min; Part 3 checks 40 min;
Part 4 one design comparison 120 min including a 20-minute break; reflection
20 min. Total: 240 minutes. Choose one comparison policy rather than repeated
sweeps. Part 5 and the optional extension are further exploration outside this
route. There is no required submission or assessment.'''
            if flow:
                s=re.sub(r'(## 1\..*?— )30 minutes',r'\g<1>20 minutes',s)
                s=re.sub(r'(## 3\..*?— )75 minutes',r'\g<1>70 minutes',s)
                if s.startswith('## 4.') and '### End-of-lab decision' not in s:
                    s+='''

### End-of-lab decision (included in this block)

Use the last 15 minutes to write 100–150 words in this answer cell: select a
pipe/speed for the fixed delivery, give electrical energy and modelled cost,
reject one alternative, and state one assumption that could change the choice.
Include the short break in this block. No pump-arrangement task or separate
Part 6 report is required. Submit the notebook with the three completed answer cells.'''
                s=s.replace('Submit this notebook with outputs and a short engineering recommendation (300–500 words).',
                            'Submit this notebook with its three answer cells and a brief decision at the end of Part 4.')
                s=s.replace('Submit this notebook with outputs and a short engineering recommendation (100–150 words).',
                            'Submit this notebook with its three answer cells and a brief decision at the end of Part 4.')
            elif distillation:
                minutes={2:40,3:50,4:65,5:30,6:25}
                for section,duration in minutes.items():
                    s=re.sub(rf'(## {section}\..*?— )\d+ minutes',rf'\g<1>{duration} minutes',s)
                if s.startswith('## 4.'):
                    marker='![Service boundary for the design comparison]'
                    tail=s[s.index(marker):] if marker in s else ''
                    s='''## 4. Choose a constrained reflux policy — 65 minutes

Keep the base feed and product specifications fixed. Use the supplied stage,
height, vapour-capacity and cost table to select one feasible reflux policy.
Reject at least one candidate using a numerical constraint. Compare the selected
policy at 100 and 120 kmol/h feed. Explain what changes in capacity margin.
Take a 10-minute break within this block. The broad reflux and purity plots
are reference material; no separate purity study is required in the four hours.

'''+tail
                if s.startswith('## 3.'):
                    s=s.replace('Compare your reflux\nchoice with a higher one and describe the physical tradeoff.',
                                'Use the base reflux here; compare operating policies in Part 4.')
                if s.startswith('## 5.'):
                    s=s.replace('Take a 10-minute break. ','')
            elif optional:
                s=s.replace('about 6 hours','about 4 hours').replace('six-hour','four-hour')
                for section,duration in {1:20,2:40,3:40,4:120,6:20}.items():
                    s=re.sub(rf'(## {section}\..*?— )(?:suggested )?\d+ minutes',rf'\g<1>{duration} minutes',s)
                if s.startswith('## 5.'):
                    s=re.sub(r'^## 5\.[^\n]*','## Further exploration — robustness (outside the four-hour route)',s)
            cell.source=s
        cells.append(cell)
    notebook.cells=cells
    if flow or distillation or optional:
        notebook.metadata['planned_hours']=4
    return notebook
