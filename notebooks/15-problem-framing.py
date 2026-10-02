"""Chapter 15 notebook: problem framing and data acquisition (stage 1).

Four artifacts for the running intrusion example: the framing card,
the 12-source inventory with its license gate, two provenance cards,
and the seed-13 synthetic generator. Four rows are real pages named
with their verified license terms; the other eight rows are fictional.
The generator is a fixed rule, never the random module: the same seed
always gives the same 8 rows. The printed output is the chapter's
expected-output block.
"""

print("stage 1, artifact 1: the framing card (the running example)")
print("  question: which events on the network day deserve a second look?")
print("  decision served: the queue's ranking")
print("  who acts: the analyst")
print("  what a flag means: an invitation, not a verdict")

print()
print("stage 1, artifact 2: the 12-source inventory")

inventory = [
    ("CTU-13", "permissive", "real"),
    ("OpenML repository entry", "permissive", "real"),
    ("university lab day", "permissive", "fictional"),
    ("honeypot day", "permissive", "fictional"),
    ("CIC-IDS2017", "conditional", "real"),
    ("UNSW-NB15", "conditional", "real"),
    ("partner-org flows", "conditional", "fictional"),
    ("vendor feed", "restricted", "fictional"),
    ("internal firewall logs", "restricted", "fictional"),
    ("red-team sandbox corpus", "restricted", "fictional"),
    ("the attack batch", "synthetic", "synthetic"),
    ("a benign day", "synthetic", "synthetic"),
]

for number, row in enumerate(inventory, 1):
    print(" ", str(number).rjust(2), row[0].ljust(24),
          row[1].ljust(12), row[2])

tally = {}
for row in inventory:
    tally[row[1]] = tally.get(row[1], 0) + 1

print()
print("  tally: permissive " + str(tally["permissive"]) +
      ", conditional " + str(tally["conditional"]) +
      ", restricted " + str(tally["restricted"]) +
      ", synthetic " + str(tally["synthetic"]))

# the book's policy: restricted rows never leave the building
print("  redistribution: 0 of the", tally["restricted"],
      "restricted sources may be redistributed")

print()
print("the acquisition gate: 3 questions, 4 outcomes")
print("  1 does the license permit the use?")
print("  2 does the policy permit copying and redistribution,"
      " or use in place?")
print("  3 can provenance be recorded?")


def yes_no(answer):
    if answer:
        return "yes"
    return "no"


def gate(license_ok, policy_ok, provenance_ok):
    # the gate is a visible rule, not a feeling
    if license_ok and policy_ok and provenance_ok:
        return "acquire"
    if license_ok and (not policy_ok) and provenance_ok:
        return "feature vectors only"
    if license_ok and (not policy_ok):
        return "reference only"
    return "synthesize"


gate_rows = [
    ("CTU-13", True, True, True),
    ("CIC-IDS2017", True, False, True),
    ("internal firewall logs", True, False, False),
    ("vendor feed", False, False, False),
]

for row in gate_rows:
    print(" ", row[0].ljust(24), yes_no(row[1]), yes_no(row[2]),
          yes_no(row[3]), "->", gate(row[1], row[2], row[3]))

print()
print("stage 1, artifact 3: the provenance cards")

provenance_cards = [
    (
        "card 1 of 2: CIC-IDS2017",
        "source: https://www.unb.ca/cic/datasets/ids-2017.html",
        "claim and location: the License section says the labeled flows",
        ["and CSV files are publicly available for researchers, and asks",
         "users to cite the related paper"],
        "access date: 2026-10-02",
        "confidence: high",
        "license or reuse: research use with citation (conditional)",
        "intended use: inventory row and license-pole teaching example",
    ),
    (
        "card 2 of 2: UNSW-NB15",
        "source: https://research.unsw.edu.au/projects/unsw-nb15-dataset",
        "claim and location: the page grants free academic research use",
        ["in perpetuity, reserves commercial use, and asserts copyright"],
        "access date: 2026-10-02",
        "confidence: high",
        "license or reuse: academic use free, commercial use reserved "
        "(conditional)",
        "intended use: inventory row and restrictive-pole teaching example",
    ),
]

for card in provenance_cards:
    print()
    print(" " + card[0])
    print("  " + card[1])
    print("  " + card[2])
    for line in card[3]:
        print("    " + line)
    print("  " + card[4])
    print("  " + card[5])
    print("  " + card[6])
    print("  " + card[7])

print()
print("stage 1, artifact 4: the synthetic generator (seed 13)")

seed = 13
n = seed
events = []
for step in range(1, 9):
    # every intermediate product is printed so readers can follow by hand
    product = 3 * n + 7
    nxt = product % 20
    print("  step " + str(step) + ": 3 * " + str(n) + " + 7 = " +
          str(product) + ", " + str(product) + " mod 20 = " + str(nxt))
    if n % 2 == 1:
        links = 1
    else:
        links = 2
    events.append((n, links, "attack", "synthetic"))
    n = nxt

print()
for number, event in enumerate(events, 1):
    print("  event " + str(number) + ": n = " + str(event[0]) +
          ", links = " + str(event[1]) + ", label = " + event[2] +
          ", flag = " + event[3])

flagged = 0
for event in events:
    if event[3] == "synthetic":
        flagged = flagged + 1

print()
print("  synthetic flag on", flagged, "of", len(events),
      "rows (100 percent)")

cycle_length = 0
m = seed
while True:
    m = (3 * m + 7) % 20
    cycle_length = cycle_length + 1
    if m == seed:
        break

trace = ""
for position in range(4):
    if position > 0:
        trace = trace + ", "
    trace = trace + str(events[position][0])

print("  cycle note: trace " + trace + ", back to 13")
print("  cycle length: " + str(cycle_length) + "; " + str(len(events)) +
      " events = " + str(len(events) // cycle_length) + " full cycles")

print()
print("the honesty note (rides every synthetic batch)")
print("  synthetic rows are used cautiously and only when other")
print("  alternatives are not available")
print("  synthetic rows are never assumed to be representative")
print("  synthetic rows are not used to generalize results")
print("  0 synthetic rows enter a claim-bearing training batch")
