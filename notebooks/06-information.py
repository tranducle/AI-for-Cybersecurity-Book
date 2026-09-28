"""Chapter 6 notebook: information and learning (fictional data only).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

import math


def surprise(p):
    """News in bits: minus log base 2 of the chance."""
    return -math.log(p, 2)


print("1. the surprise ladder")
for p in [0.5, 0.25, 0.125]:
    print("chance", p, "gives", round(surprise(p), 4), "bits of news")

print()
print("2. entropy as the average surprise")
probs = [0.5, 0.25, 0.25]
surprises = [surprise(p) for p in probs]
weighted = [probs[i] * surprises[i] for i in range(3)]
print("surprises:", surprises)
print("weighted:", [round(w, 4) for w in weighted])
print("entropy =", round(sum(weighted), 4), "bits")

print()
print("3. log-loss: the average news of the truth")
true_class_p = [0.5, 0.5, 0.25, 0.25]
losses = [surprise(p) for p in true_class_p]
print("true-class probabilities:", true_class_p)
print("per-event losses:", [round(loss, 4) for loss in losses])
average = sum(losses) / len(losses)
print("average log-loss =", round(average, 4), "bits")

print()
print("4. the confident-wrong fine")
p_truth = 1 / 64
print("probability given the truth:", p_truth, "(1/64)")
print("fine =", round(surprise(p_truth), 4), "bits")

print()
print("5. likelihood: the same fit as a product")
likelihood = 1.0
for p in true_class_p:
    likelihood *= p
print("likelihood =", round(likelihood, 6), "(1/64)")
print("average log-loss is the news version of this product")

print()
print("6. bias and variance on three fictional rounds (true rate 0.05)")
rounds = {
    "steady and right": [0.04, 0.05, 0.06],
    "tight but wrong": [0.12, 0.13, 0.11],
    "scattered": [0.01, 0.09, 0.05],
}
for name, values in rounds.items():
    avg = sum(values) / len(values)
    spread = max(values) - min(values)
    print(name, values, " average =", round(avg, 4),
          " spread =", round(spread, 4))

print()
print("7. the regularization toy")
print("wobbly fit: training leftovers 0, invented guess at x=4: 10")
print("straight line: training leftovers small, invented guess at x=4: 4")
print("the tug prefers the straight line")

print()
print("a small loss is an observation about data, not proof of learning")
