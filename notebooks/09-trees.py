"""Chapter 9 notebook: trees, forests, and boosting (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""


def wrongness(group):
    """How many the majority answer gets wrong in a leaf."""
    phish = sum(1 for _, label in group if label == "phishing")
    benign = len(group) - phish
    return min(phish, benign)


def walk(odd, links):
    """The learned tree: odd at least 3, then links at least 2."""
    if odd >= 3:
        return "phishing"
    if links >= 2:
        return "phishing"
    return "benign"


emails = [
    ("E1", 1, 1, "benign"), ("E2", 2, 0, "benign"),
    ("E3", 2, 2, "phishing"), ("E4", 3, 1, "phishing"),
    ("E5", 4, 2, "phishing"), ("E6", 5, 0, "phishing"),
    ("E7", 6, 3, "phishing"),
]

print("1. the wrongness ruler and the root candidates")
all_g = [(name, label) for name, _, _, label in emails]
print("before any split: 2 wrong of 7 (majority phishing)")
yes_odd = [(n, l) for n, o, k, l in emails if o >= 3]
no_odd = [(n, l) for n, o, k, l in emails if o < 3]
print("odd >= 3:", [n for n, _ in yes_odd], " wrong:",
      wrongness(yes_odd), "+", wrongness(no_odd), "=", 
      wrongness(yes_odd) + wrongness(no_odd))
yes_links = [(n, l) for n, o, k, l in emails if k >= 2]
no_links = [(n, l) for n, o, k, l in emails if k < 2]
print("links >= 2:", [n for n, _ in yes_links], " wrong:",
      wrongness(yes_links), "+", wrongness(no_links), "=",
      wrongness(yes_links) + wrongness(no_links))
print("the root picks odd >= 3 (1 beats 2)")
print("after the root: 1 wrong; after links >= 2 on the NO group: 0")

print()
print("2. walking the tree")
for odd, links in [(2, 1), (3, 2), (6, 3), (1, 1)]:
    print(f"  ({odd}, {links}) -> {walk(odd, links)}")

print()
print("3. the forest: three stirred copies vote")
copy_a = ["E1", "E1", "E2", "E4", "E5", "E6", "E7"]
copy_b = ["E2", "E3", "E4", "E5", "E6", "E7", "E7"]
copy_c = ["E1", "E2", "E2", "E3", "E4", "E6", "E7"]
print("copy A drops E3, repeats E1:", copy_a)
print("copy B drops E1, repeats E7:", copy_b)
print("copy C drops E5, repeats E2:", copy_c)
print("(this toy regrows the same two questions on each copy)")
print("new email (2, 1): tree A: benign  tree B: benign  tree C: benign")
print("the aggressive variant (tree B prime, links at least 1):")
print("  (2, 1) -> phishing")
print("the vote: 2 benign, 1 phishing  verdict: benign (holds)")

print()
print("4. boosting: aim at the misses")
print("round 1 stump (odd >= 3): E1 ok, E2 ok, E3 MISS, E4-E7 ok")
print("1 wrong of 7; E3's weight doubles: 1 -> 2 (others stay 1)")
print("round 2 focused tree (links >= 2): catches E3 (2 links)")
print("combined stack: 0 wrong of 7")
print("caution: 7 emails memorizes fast; real boosting takes small steps")

print()
print("5. feature importance from the split gains")
gain_odd = 2 - 1
gain_links = 1 - 0
total = gain_odd + gain_links
print("odd characters gain:", gain_odd, " links gain:", gain_links)
print("shares: odd", round(gain_odd / total, 3),
      " links", round(gain_links / total, 3))
print("(toy shares; real forests accumulate many splits)")

print()
print("importance ranks work done, not causes")
