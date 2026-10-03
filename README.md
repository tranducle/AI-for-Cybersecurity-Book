# AI for Cybersecurity Book, Companion Notebooks

This repository holds the companion notebooks for the book
**Applying Machine Learning and AI to Cybersecurity Problems: A Visual,
Zero-Background Guide to Models, Data, and Real Security Problems**
by Tran Duc Le.

Each notebook is a small Python script that works through the arithmetic
of one chapter. The notebooks are checkers: you do the calculations by
hand while reading the chapter, then run the script to confirm each
intermediate step. They are meant to be read beside the book, not as a
standalone course.

## Notebooks and chapters

| Notebook | Chapter |
|---|---|
| `notebooks/01-reading-math.py` | 1. Reading Mathematics Again |
| `notebooks/02-vectors.py` | 2. Vectors |
| `notebooks/03-matrices.py` | 3. Matrices as Machines |
| `notebooks/04-optimization.py` | 4. Change and Optimization |
| `notebooks/05-chance.py` | 5. Chance and Evidence |
| `notebooks/06-information.py` | 6. Information and Learning |
| `notebooks/07-ml-intro.py` | 7. What Machine Learning Actually Is |
| `notebooks/08-regression.py` | 8. Linear and Logistic Regression |
| `notebooks/09-trees.py` | 9. Trees, Forests, and Boosting |
| `notebooks/10-neighbors.py` | 10. Nearest Neighbors and Clustering |
| `notebooks/11-anomaly.py` | 11. Anomaly Detection |
| `notebooks/12-neural.py` | 12. Neural Networks and Deep Learning |
| `notebooks/13-llm.py` | 13. Language Models and LLMs |
| `notebooks/14-process.py` | 14. The Whole Process at Once |
| `notebooks/15-problem-framing.py` | 15. Problem Framing and Data Acquisition: Stage 1 in Depth |
| `notebooks/16-data-validation.py` | 16. Data Validation, Cleaning, and Labels: Stage 2 in Depth |

## How to run

You need Python 3 and nothing else. The notebooks use only the standard
library, so there is nothing to install:

    python3 notebooks/03-matrices.py

Run them in any order, although they follow the chapter sequence of the
book. See `REPRODUCIBILITY.md` for details on expected output and
`DATA.md` for a note on the data.

## A note on the data

Every dataset in these notebooks is fictional. The counts, scores,
emails, and measurements were invented for teaching the arithmetic
behind each method. Nothing in the notebooks is real telemetry, real
traffic, or data from any real system.
