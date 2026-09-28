"""Chapter 12 notebook: neural networks and deep learning (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

import math


def relu(z):
    """The keep-the-positive bend."""
    return max(0.0, z)


def squash(z):
    """The base-2 squash into a probability."""
    return 1 / (1 + 2 ** (-z))


print("1. the ReLU ladder")
for z in [-2, 0, 3, 8.5]:
    print(f"  ReLU({z}) = {relu(z)}")

print()
print("2. one neuron: weighted sum, bias, bend, squash")
z = 2 * 3 + 1 * 2 + 0.5
print("z = 2*3 + 1*2 + 0.5 =", z)
print("ReLU(z) =", relu(z))
print("squash(8.5) =", round(squash(8.5), 4), "(about 0.997)")

print()
print("3. the tiny network forward pass (2-2-1)")
x1, x2 = 1, 2
h1 = relu(0.5 * x1 + (-0.2) * x2 + 0.1)
h2 = relu((-1) * x1 + 0.8 * x2 + 0)
print("h1 = ReLU(0.5*1 - 0.2*2 + 0.1) =", round(h1, 6))
print("h2 = ReLU(-1*1 + 0.8*2 + 0) =", round(h2, 6))
z_out = 1.5 * h1 + 1.0 * h2 - 0.4
print("z = 1.5*h1 + 1.0*h2 - 0.4 =", round(z_out, 6))
print("squash(z) =", round(squash(z_out), 4), "(about 0.586)")

print()
print("4. the sliding filter [1, 0, 1] over the byte window")
window = [9, 0, 9, 1]
filt = [1, 0, 1]
scores = []
for pos in range(len(window) - len(filt) + 1):
    s = sum(window[pos + k] * filt[k] for k in range(len(filt)))
    scores.append(s)
    print(f"  position {pos + 1}: "
          + " + ".join(f"{window[pos + k]}*{filt[k]}"
                       for k in range(len(filt))) + f" = {s}")
print("score map:", scores, "(the 9-0-9 pattern lives at position 1)")
spike = [sum(window[p + k] * [0, 1, 0][k] for k in range(3))
         for p in range(2)]
print("spike filter [0,1,0] map:", spike)

print()
print("5. the attention spotlight (weights sum to 1)")
inputs = ["login failed", "new country", "night hour"]
weights = [0.1, 0.8, 0.1]
print("weights:", weights, " sum:", round(sum(weights), 3))
for name, w in zip(inputs, weights):
    print(f"  {name}: {w}")
print("the weighted reading leans on:", inputs[weights.index(max(weights))])

print()
print("stacked arithmetic, not understanding; judge on new batches")
