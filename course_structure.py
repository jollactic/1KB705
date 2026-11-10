"""Course roles shared by generated student and solution notebooks."""
import nbformat

ROLES = {'preparation/lab_00_balances':'preparation','main_labs/lab_01_flow':'main','main_labs/lab_03_distillation':'main',
         'optional_labs/lab_02_heat':'optional','optional_labs/lab_04_absorption':'optional'}


def apply_course_role(notebook,folder):
    role=ROLES[folder]
    notebook.metadata['course_role']=role
    notebook.cells=[c for c in notebook.cells if not c.metadata.get('course_role_banner')]
    if role=='main':
        message='''**Main course lab.** The two main labs are **Lab 1 (flow and
pumps) and Lab 3 (distillation)**. Use Lab 00 for preparation if needed.
Complete the tasks and recommendation as part of the main lab work. Labs 2
and 4 are optional self-study and are not prerequisites for this lab.'''
    elif role=='optional':
        message='''**Optional self-study lab.** Explore this extra material independently
if you are interested. The main course labs are **Lab 1 (flow and pumps) and
Lab 3 (distillation)**. There is **no required submission or assessment** for
this optional lab. Worked examples, supplied calculations and the separate solution
notebook support self-checking. The six-hour outline is a suggested pace for the
full notebook; choose individual sections or work at your own pace, alone or
with a partner. Lab 00 can help with balance fundamentals.'''
    else:
        message='''**Preparation and practice.** Use this introductory balance workshop
before the main labs if needed. The main course labs are **Lab 1 (flow and
pumps) and Lab 3 (distillation)**. This preparation is not an additional assessed
main lab; use the completed solution to check your work.'''
    banner=nbformat.v4.new_markdown_cell(message)
    banner.metadata['course_role_banner']=True
    notebook.cells.insert(1,banner)
    for cell in notebook.cells:
        if cell.cell_type!='markdown' or cell.metadata.get('course_role_banner'):
            continue
        if role=='optional':
            substitutions={
                '**Time budget: 6 hours, including a short break and submission.** Work in pairs,':
                '**Suggested self-study pace: about 6 hours for the full notebook.** Work independently or with a partner,',
                'Submit this notebook with outputs and a short engineering recommendation (300–500 words).':
                'For your own learning, keep outputs and optionally write a short recommendation. No submission is required.',
                'You are assessed on engineering reasoning, not on writing Python.':
                'Use the solution to self-check your engineering reasoning. No assessment or new Python code is required.',
                '## 6. Engineering recommendation and submission — 45 minutes':
                '## 6. Optional reflection and self-check — suggested 45 minutes',
                'No new code is required for submission.':
                'No formal submission is required; use the solution for self-checking.',
                'before submission':'before comparing with the solution',
                'core design challenge':'self-study design challenge',
                'Core design challenge':'Self-study design challenge',
                'core comparison':'self-study comparison'}
            substitutions.update({
                'used in the assessed tasks':'used in the self-study tasks',
                'No Python programming is assessed.':'No Python programming is required.',
                'but both partners must be able to explain every figure and calculation.':
                'Use the solution to check your understanding of each figure and calculation.',
                '**Time budget (six hours):**':'**Suggested full self-study outline (six hours):**',
                '**Peer check:** Ask your partner to explain one equation, one numerical check,':
                '**Self-check (or discuss with a partner):** Explain one equation, one numerical check,',
                'core cost/constraint table':'cost/constraint comparison table'})
            for original,replacement in substitutions.items():
                cell.source=cell.source.replace(original,replacement)
        elif role=='preparation':
            cell.source=cell.source.replace('Submit your completed answer cells and a short explanation (150–250 words) of',
                'For preparation, complete the answer cells and write a short explanation (150–250 words) of')
    return notebook
