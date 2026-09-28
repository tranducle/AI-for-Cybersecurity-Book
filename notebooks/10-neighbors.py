"""Chapter 10 notebook: nearest neighbors and clustering (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

import math


def dist(p, q):
    """The chapter 2 distance: squared differences, summed, rooted."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


emails = [
    ("E1", (1, 1), "benign"), ("E2", (2, 0), "benign"),
    ("E3", (2, 2), "phishing"), ("E4", (3, 1), "phishing"),
    ("E5", (4, 2), "phishing"), ("E6", (5, 0), "phishing"),
    ("E7", (6, 3), "phishing"),
]

print("1. asking the room: distances from the new email (4, 1)")
new = (4, 1)
by_distance = sorted((round(dist(new, p), 3), name) for name, p, _ in emails)
for d, name in by_distance:
    print(f"  {name}: {d}")
print("the three nearest: E4 (1), E5 (1), E6 (about 1.414): all phishing")
print("the vote: phishing 3 of 0 (E4 and E5 tie at 1: an honest tie)")

print()
print("2. k-means round by round: start centers (1, 1) and (6, 3)")
start_a = (1, 1)
start_b = (6, 3)
group_a = []
group_b = []
for name, p, _ in emails:
    if dist(p, start_a) <= dist(p, start_b):
        group_a.append(name)
    else:
        group_b.append(name)
print("round 1 groups: A", group_a, " B", group_b)
cent_a = (sum(p[0] for n, p, _ in emails if n in group_a) / len(group_a),
          sum(p[1] for n, p, _ in emails if n in group_a) / len(group_a))
cent_b = (sum(p[0] for n, p, _ in emails if n in group_b) / len(group_b),
          sum(p[1] for n, p, _ in emails if n in group_b) / len(group_b))
print("new center A =", [round(v, 3) for v in cent_a])
print("new center B =", [round(v, 3) for v in cent_b])
same = True
for name, p, _ in emails:
    closer_a = dist(p, cent_a) <= dist(p, cent_b)
    if (name in group_a) != closer_a:
        same = False
print("round 2: every email keeps its group:", same)
print("converged after 2 rounds")

print()
print("3. the inertia pile after convergence")
pile_a = sum(dist(p, cent_a) ** 2 for n, p, _ in emails if n in group_a)
pile_b = sum(dist(p, cent_b) ** 2 for n, p, _ in emails if n in group_b)
print("group A pile =", round(pile_a, 4), " group B pile =", round(pile_b, 4))
print("total pile =", round(pile_a + pile_b, 4))

print()
print("4. the ruler is part of the claim")
raw = dist((1, 1), (2, 2))
rescaled = dist((1, 2), (2, 4))
print("raw counts: (1,1) to (2,2) =", round(raw, 3))
print("half-links: (1,2) to (2,4) =", round(rescaled, 3))
print("same pair, different looks: report the units with every distance")

print()
print("groups are the ruler's opinion, not the truth")
