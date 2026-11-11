"""Notebook setup cells using the published helper paths on the jolla branch."""
import textwrap

BASE_URL='https://raw.githubusercontent.com/jollactic/1KB705/refs/heads/jolla'


def helper_setup(folder):
    return textwrap.dedent(f'''
    from pathlib import Path
    from urllib.request import urlretrieve

    # Published helper for this lab; an existing local helpers.py is retained.
    HELPER_URL = "{BASE_URL}/{folder}/helpers.py"
    if not Path("helpers.py").exists():
        urlretrieve(HELPER_URL, "helpers.py")

    import numpy as np
    import matplotlib.pyplot as plt
    import helpers as h
    ''').strip()
