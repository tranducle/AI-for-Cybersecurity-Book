# Reproducibility

## Requirements

Any modern Python 3 works; Python 3.9 or newer is a safe baseline.
The notebooks use only the Python standard library (`math` and built-in
types). There are no third-party dependencies, so no `pip install` step
is needed. See `requirements.txt`.

## Running a notebook

From the repository root:

    python3 notebooks/01-reading-math.py
    python3 notebooks/02-vectors.py
    python3 notebooks/03-matrices.py
    python3 notebooks/04-optimization.py
    python3 notebooks/05-chance.py
    python3 notebooks/06-information.py
    python3 notebooks/07-ml-intro.py
    python3 notebooks/08-regression.py
    python3 notebooks/09-trees.py
    python3 notebooks/10-neighbors.py
    python3 notebooks/11-anomaly.py

Each notebook can also be run from inside `notebooks/` with
`python3 01-reading-math.py`; no file reads or writes are involved.

## Expected output

All output prints to stdout. Each notebook prints numbered sections
with the intermediate arithmetic of its chapter, ending with the final
quantity the chapter derives (an accuracy, a distance, an entropy, a
fitted line, a tree split, and so on).

The notebooks are deterministic: they contain no randomness, no seeds,
no network access, and no file access. Running a notebook twice gives
identical output. If the numbers on your screen disagree with the book,
re-check your hand arithmetic; the notebook is the slower, more patient
calculator of the two.
