"""Chapter 11 notebook: anomaly detection, mining the rare (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

import math


def dist(p, q):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


emails = [("E1", (1, 1)), ("E2", (2, 0)), ("E3", (2, 2)), ("E4", (3, 1)),
          ("E5", (4, 2)), ("E6", (5, 0)), ("E7", (6, 3))]
far = ("F", (10, 8))


def score(point):
    """Oddness: the distance to the second-nearest neighbor."""
    ds = sorted(round(dist(point, p), 3) for _, p in emails if p != point)
    return ds[1]


print("1. the oddness score (second-nearest-neighbor distance)")
for name, p in [emails[0], emails[1], emails[6], far]:
    ds = sorted(round(dist(p, q), 3) for _, q in emails if q != p)
    print(f"  {name}: nearest {ds[0]}, second-nearest {ds[1]}"
          f" -> score {ds[1]}")
print("the room scores about 1.4 to 3.2; F scores about 8.5: the flag")

print()
print("2. the density view: neighbors within radius 2")
for name, p in [emails[0], emails[1], emails[6], far]:
    count = sum(1 for _, q in emails if q != p and dist(p, q) <= 2)
    print(f"  {name}: {count} neighbors within radius 2")
count_f5 = sum(1 for _, q in emails if dist(far[1], q) <= 5)
print("F neighbors within radius 5:", count_f5)
print("E7's nearest (E5) sits at", round(dist(emails[6][1],
      emails[4][1]), 3), ", just outside the circle")

print()
print("3. the flag column on 10,000 events (chapter 5's network)")
events = 10000
attacks = 100
flags = int(events * 0.01)
caught = 5
weird = flags - caught
print("flags (top 1 percent):", flags)
print("caught attacks:", caught, " weird-but-benign:", weird)
print("real share:", caught, "of", flags, "=",
      round(caught / flags * 100, 1), "percent")
print("chapter 5's tuned detector by pointer: 99 of 594, 1 in 6")

print()
print("an anomaly is odd under a chosen normal, not malice;")
print("name the view, the ruler, the threshold, and the base rate")
