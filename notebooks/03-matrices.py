"""Chapter 3 notebook: matrices as machines (fictional data only).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

import math


def dot(a, b):
    """Matching pieces multiply, then add: the chapter-2 dot product."""
    return sum(x * y for x, y in zip(a, b))


def transpose(table):
    """Rows become columns: the table turned sideways."""
    return [[row[j] for row in table] for j in range(len(table[0]))]


print("1. the matrix machine")
M = [[2, 1], [1, 3]]
v = [3, 2]
out = [dot(row, v) for row in M]
print("M =", M)
print("v =", v)
print("row 1 dot v = 2*3 + 1*2 =", 2 * 3 + 1 * 2)
print("row 2 dot v = 1*3 + 3*2 =", 1 * 3 + 3 * 2)
print("M times v =", out, "(expect [8, 9])")

print()
print("2. the transpose lines pieces up")
X = [[40, 1], [120, 3], [150, 10], [80, 2]]  # four fictional emails: words, links
XT = transpose(X)
print("emails X (words, links) =", X)
print("transposed: words row =", XT[0])
print("transposed: links row =", XT[1])

print()
print("3. a tiny linear system: x + y = 5, 2x - y = 4")
x = 9 / 3          # adding the two equations gives 3x = 9
y = 5 - x          # put x back into the first equation
print("x =", x)
print("y =", y)
print("solution =", (x, y))

print()
print("4. least squares by hand: four days, events and risk")
X1 = [[1, 1], [1, 2], [1, 3], [1, 4]]  # the ones column is the standing start
y = [1, 2, 2, 3]                       # the analyst's fictional risk scores
X1T = transpose(X1)
XTX = [[dot(X1T[i], [X1[k][j] for k in range(len(X1))]) for j in range(2)] for i in range(2)]
XTy = [dot(X1T[i], y) for i in range(2)]
print("X^T X =", XTX, "(expect [[4, 10], [10, 30]])")
print("X^T y =", XTy, "(expect [8, 23])")
print("system to solve: 4a + 10b = 8 and 10a + 30b = 23")
b = 3 / 5          # multiply the first equation by 2.5 and subtract: 5b = 3
a = (8 - 10 * b) / 4
print("a =", a, " b =", b)
print("best-fit line: risk =", round(a, 2), "+", round(b, 2), "* events")
events = [1, 2, 3, 4]
pred = [a + b * e for e in events]
print("predictions:", [round(p, 2) for p in pred])
resid = [y[k] - pred[k] for k in range(4)]
print("leftovers:", [round(r, 2) for r in resid])
print("sum of squared leftovers:", round(sum(r * r for r in resid), 2))

print()
print("5. PCA as compression: where does the cloud spread?")
pts = [(0.4, 1.0), (1.2, 0.7), (2.0, 1.5), (2.6, 3.0),
       (3.3, 2.6), (4.1, 3.6), (4.8, 5.2), (5.6, 5.0)]


def variance(values):
    m = sum(values) / len(values)
    return sum((val - m) ** 2 for val in values) / len(values)


diag = [(x + y) / math.sqrt(2) for x, y in pts]
perp = [(x - y) / math.sqrt(2) for x, y in pts]
print("spread along the diagonal (most-spread direction):", round(variance(diag), 3))
print("spread along the perpendicular (least-spread):", round(variance(perp), 3))
print("keep the diagonal: compression keeps most of the spread")
print()
print("a fit is an observation, not a verdict")
