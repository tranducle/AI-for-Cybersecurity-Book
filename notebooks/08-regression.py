"""Chapter 8 notebook: linear and logistic regression (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

import math


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def transpose(table):
    return [[row[j] for row in table] for j in range(len(table[0]))]


def squash(z):
    """The base-2 squash: a probability between 0 and 1."""
    return 1 / (1 + 2 ** (-z))


def surprise(p):
    """News in bits: minus log base 2 of the truth's probability."""
    return -math.log(p, 2)


print("1. the chapter 3 hand solve returns")
X1 = [[1, 1], [1, 2], [1, 3], [1, 4]]
y = [1, 2, 2, 3]
X1T = transpose(X1)
XTX = [[dot(X1T[i], [r[j] for r in X1]) for j in range(2)] for i in range(2)]
XTy = [dot(X1T[i], y) for i in range(2)]
print("X^T X =", XTX, " X^T y =", XTy)
b = 3 / 5
a = (8 - 10 * b) / 4
print("fit: risk =", a, "+", b, "* events")
print("the intercept sentence: risk", a, "when events are 0")
print("the slope sentence: each extra event adds", b)
print("prediction at 6 events:", a + 6 * b)

print()
print("2. the squash table (base 2)")
for z in [-1, 0, 1, 2, 3]:
    print("z =", z, " ->  p =", round(squash(z), 3))

print()
print("3. the logistic run on the train emails: z = -3 + 1 * odd_chars")
train = [(1, "benign"), (2, "benign"), (4, "phishing"),
         (5, "phishing"), (5, "phishing"), (8, "phishing")]
probs = []
for count, label in train:
    z = -3 + 1 * count
    p = squash(z)
    probs.append((count, label, z, p))
    call = "phishing" if p >= 0.5 else "benign"
    print(f"  ({count}, {label}): z = {z}  p = {round(p, 3)}  call: {call}")

print()
print("4. the log-loss fine on the train batch (bits)")
bits = []
for count, label, z, p in probs:
    p_truth = p if label == "phishing" else 1 - p
    s = surprise(p_truth)
    bits.append(s)
    print(f"  ({count}, {label}): p_truth = {round(p_truth, 3)}"
          f"  surprise = {round(s, 3)} bits")
print("sum =", round(sum(bits), 3),
      " average log-loss =", round(sum(bits) / len(bits), 4), "bits")

print()
print("5. validate and test: the walks repeat, the graze returns")
validate = [(1, "benign"), (3, "benign"), (7, "phishing")]
test = [(2, "benign"), (6, "phishing"), (9, "phishing")]
for name, batch in [("validate", validate), ("test", test)]:
    vb = []
    for count, label in batch:
        p = squash(-3 + 1 * count)
        call = "phishing" if p >= 0.5 else "benign"
        p_truth = p if label == "phishing" else 1 - p
        vb.append(surprise(p_truth))
        print(f"  {name} ({count}, {label}): p = {round(p, 3)}"
              f"  call: {call}  surprise = {round(surprise(p_truth), 3)}")
    print(f"  {name} average log-loss =",
          round(sum(vb) / len(vb), 4), "bits")

print()
print("a fitted sentence is an observation about this data, not a cause")
