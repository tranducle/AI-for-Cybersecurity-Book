"""Chapter 4 notebook: change and optimization (fictional data only).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""


def pile(w):
    """The toy leftover pile as a function of one knob."""
    return (w - 3) ** 2 + 1


def slope(w):
    """The slope of the toy pile at w (the touching-line steepness)."""
    return 2 * (w - 3)


print("1. the slope at a few points")
for w in [0, 1, 2, 3]:
    print("w =", w, " pile =", pile(w), " slope =", slope(w))

print()
print("2. descent with step 0.25 from w = 0")
w = 0.0
for step_i in range(4):
    s = slope(w)
    new_w = w - 0.25 * s
    print("w =", w, " slope =", s, " new w =", new_w, " gap to 3 =", round(3 - new_w, 4))
    w = new_w

print()
print("3. descent with step 0.05 from w = 0 (crawling)")
w = 0.0
for step_i in range(4):
    s = slope(w)
    new_w = w - 0.05 * s
    print("w =", round(w, 4), " slope =", round(s, 4), " new w =", round(new_w, 4))
    w = new_w

print()
print("4. descent with step 1.1 from w = 0 (overshoot)")
w = 0.0
for step_i in range(3):
    s = slope(w)
    new_w = w - 1.1 * s
    print("w =", round(w, 4), " slope =", round(s, 4), " new w =", round(new_w, 4))
    w = new_w

print()
print("5. two knobs: the gradient and one plain step")


def grad_a(a, b):
    return 2 * (a - 1)


def grad_b(a, b):
    return 2 * (b - 2)


a, b = 0.0, 0.0
for step_i in range(2):
    ga, gb = grad_a(a, b), grad_b(a, b)
    new_a = a - 0.25 * ga
    new_b = b - 0.25 * gb
    print("knobs =", (a, b), " gradient =", (ga, gb),
          " new knobs =", (new_a, new_b))
    a, b = new_a, new_b

print()
print("a smaller pile is an observation, not the truth")
