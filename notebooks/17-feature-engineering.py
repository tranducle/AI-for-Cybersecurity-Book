"""Chapter 17 notebook: feature engineering and representation (stage 3).

The running example's 14 clean rows arrive from stage 2 with their audited
labels. Each row becomes a list of numbers under written rules (the feature
card), categories are one-hot encoded, and every candidate feature passes
the decision-time check before the table moves to stage 4. Tiny invented
inputs show the security feature families by hand: one 8-byte window, two
URLs on reserved documentation hosts, one flow, and two import lists with
fictional names. Zero imports: every share in the byte window is a power of
two, so surprise is found by counting halvings, chapter 6's ladder. The
printed output is the chapter's expected-output block.
"""

print("the feature card (5 fields, one card per feature)")
print("  name: what the column is called")
print("  source field: which raw field it reads")
print("  rule: how the number is computed, written down")
print("  kind: count, share, 0 or 1, or plain number")
print("  available at decision time: yes or no")

# the integer-code trap: codes chosen in arbitrary order look like amounts
codes = {"login": 0, "browse": 1, "scan": 2, "deny": 3}
print()
print("the integer-code trap (arbitrary codes read as amounts)")
print("  codes: login 0, browse 1, scan 2, deny 3")
middle = (codes["login"] + codes["scan"]) / 2
names_by_code = {v: k for k, v in codes.items()}
print("  average of login and scan: (0 + 2) / 2 = " + str(middle))
print("  code " + str(int(middle)) + " is " + names_by_code[int(middle)]
      + ": the codes claim browse sits halfway between")
print("  login and scan, which means nothing, so events get one-hot")
print("  columns instead")

# stage 2's handoff: 14 clean rows, labels after the audit
# (attack at rows 2, 5, 6, 12; rows 15, 17, 19, 20 flagged unaudited)
clean_rows = [
    (1, "host-a", "login", 1),
    (2, "host-b", "scan", 2),
    (4, "host-a", "browse", 0),
    (5, "host-b", "deny", 1),
    (6, "host-a", "scan", 2),
    (8, "host-b", "login", 1),
    (9, "host-a", "deny", 2),
    (10, "host-b", "scan", 0),
    (12, "host-b", "login", 2),
    (14, "host-b", "browse", 1),
    (15, "host-a", "login", 0),
    (17, "host-b", "browse", 2),
    (19, "host-a", "login", 2),
    (20, "host-b", "deny", 0),
]
attack_rows = (2, 5, 6, 12)
flagged_rows = (15, 17, 19, 20)

hosts = ("host-a", "host-b")
events = ("login", "browse", "scan", "deny")
columns = ["host_a", "host_b", "login", "browse", "scan", "deny", "links"]


def encode(host, event, links):
    """One-hot host (2 columns), one-hot event (4 columns), links kept."""
    vector = [1 if host == h else 0 for h in hosts]
    vector += [1 if event == e else 0 for e in events]
    vector.append(links)
    return vector


print()
print("the encoding table (14 rows, 7 feature columns, 1 label column)")
print("  vector order: " + ", ".join(columns))
print("  row  clean row         vector                 label")
table = []
for number, host, event, links in clean_rows:
    vector = encode(host, event, links)
    label = 1 if number in attack_rows else 0
    table.append((number, vector, label))
    flag = "  flagged" if number in flagged_rows else ""
    raw = host + "," + event + "," + str(links)
    print("  " + str(number).rjust(3) + "  " + raw.ljust(16) + "  "
          + str(tuple(vector)) + "  " + str(label) + flag)

print()
print("column sums over the 14 rows")
sums = [sum(vector[i] for _, vector, _ in table) for i in range(7)]
for name, total in zip(columns, sums):
    print("  " + name + ": " + str(total))
ones = sum(label for _, _, label in table)
print("  label: " + str(ones) + " ones, " + str(len(table) - ones)
      + " zeros")
print("  hand check: host_a + host_b = " + str(sums[0]) + " + "
      + str(sums[1]) + " = " + str(sums[0] + sums[1]) + " rows")
print("  hand check: login + browse + scan + deny = " + " + ".join(
      str(s) for s in sums[2:6]) + " = " + str(sum(sums[2:6])) + " rows")


def halvings(count, total):
    """Surprise in bits of a share count/total that is a power of two.

    Chapter 6's ladder: count the halvings from 1 down to the share.
    """
    steps = 0
    while count < total:
        count = count * 2
        steps = steps + 1
    if count != total:
        raise ValueError("share is not a power of two")
    return steps


def byte_entropy(window):
    """Histogram, shares, surprises, and entropy of a byte window."""
    counts = {}
    for byte in window:
        counts[byte] = counts.get(byte, 0) + 1
    total = len(window)
    rows = []
    entropy = 0.0
    for byte in sorted(counts):
        bits = halvings(counts[byte], total)
        share = counts[byte] / total
        entropy = entropy + share * bits
        rows.append((byte, counts[byte], share, bits))
    return rows, entropy


print()
print("the byte window (8 bytes, invented): AAAABBCD")
rows, entropy = byte_entropy("AAAABBCD")
print("  byte  count  share  surprise (halvings)  share x surprise")
for byte, count, share, bits in rows:
    print("     " + byte + "      " + str(count) + "  " + str(share).ljust(5)
          + "  " + str(bits) + " bits" + " " * 14 + str(share * bits))
print("  entropy: " + " + ".join(str(s * b) for _, _, s, b in rows)
      + " = " + str(entropy) + " bits")

print()
print("contrasts")
for window in ("AAAAAAAA", "ABCDEFGH", "AABBCCDD"):
    _, value = byte_entropy(window)
    print("  " + window + ": " + str(value) + " bits")
ceiling = 0
values = 1
while values < 256:
    values = values * 2
    ceiling = ceiling + 1
print("  ceiling for all 256 byte values: 2 doubled " + str(ceiling)
      + " times is " + str(values) + ", so " + str(ceiling) + " bits")
print("  entropy measures how evenly the bytes are spread, not whether")
print("  a file is bad: compressed benign files also sit near the ceiling")


def url_features(url):
    """5 lexical counts: length, dots, digits, at sign, IP host."""
    host = url.split("://", 1)[1].split("/", 1)[0]
    pieces = host.split(".")
    ip_host = 1 if len(pieces) == 4 and all(p.isdigit() for p in pieces) \
        else 0
    return [len(url), url.count("."), sum(c.isdigit() for c in url),
            1 if "@" in url else 0, ip_host]


print()
print("URL lexical features (invented, reserved documentation hosts)")
print("  (length, dots, digits, at sign, IP host)")
for url in ("http://shop.example.com/cart", "http://198.51.100.7/a@b",
            "http://203.0.113.25/secure"):
    print("  " + url.ljust(30) + " " + str(tuple(url_features(url))))
print("  the suspicious second URL is shorter than the first,")
print("  so length alone misleads; read the vector together")


def flow_stats(times, sizes):
    """5 flow statistics: duration, packets, bytes, mean size, rate."""
    duration = times[-1] - times[0]
    total = sum(sizes)
    return [duration, len(sizes), total, total / len(sizes),
            total / duration]


print()
print("flow statistics (invented)")
print("  (duration s, packets, bytes, mean size, bytes per second)")
for name, times, sizes in (("F1", [0, 0.5, 1.0, 2.0], [100, 300, 300, 100]),
                           ("F2", [0, 1, 4], [200, 400, 600])):
    stats = flow_stats(times, sizes)
    print("  " + name + ": times " + str(times) + ", sizes " + str(sizes))
    print("      " + str(tuple(stats)))

vocabulary = ("open_file", "read_file", "send_data", "set_autorun")
programs = (("P", ("open_file", "read_file")),
            ("Q", ("open_file", "send_data", "set_autorun")))
print()
print("import presence vectors (fictional names, 4-name vocabulary)")
print("  vocabulary: " + ", ".join(vocabulary))
vectors = {}
for name, imports in programs:
    vectors[name] = [1 if v in imports else 0 for v in vocabulary]
    print("  " + name + " imports " + ", ".join(imports) + ": "
          + str(tuple(vectors[name])))
shared = sum(a * b for a, b in zip(vectors["P"], vectors["Q"]))
print("  names imported by both: " + str(shared))

# the decision-time check: every candidate feature, one verdict each
candidates = [(c, "yes", "kept") for c in columns]
candidates.append(("incident_flag", "no", "rejected"))
print()
print("the decision-time check (8 candidates)")
print("  feature        available at decision time  verdict")
for name, available, verdict in candidates:
    print("  " + name.ljust(15) + available.ljust(28) + verdict)
print("  incident_flag is copied from the incident record, which is")
print("  written after the alert was worked: it would not be")
print("  available at prediction time, so it leaks the answer")
kept = [c for c in candidates if c[2] == "kept"]
print("  kept: " + str(len(kept)) + ", rejected: "
      + str(len(candidates) - len(kept)))

print()
print("the handoff tally to stage 4")
print("  rows: " + str(len(table)))
print("  feature columns: " + str(len(kept)))
print("  label columns: 1 (" + str(ones) + " attack, "
      + str(len(table) - ones) + " benign)")
print("  rows flagged unaudited: " + str(len(flagged_rows)))
print("  kept features failing the decision-time check: "
      + str(sum(1 for c in kept if c[1] != "yes")))
