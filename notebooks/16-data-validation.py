"""Chapter 16 notebook: data validation, cleaning, and labels (stage 2).

The running example's raw day: 20 fixed log lines with planted defects,
fictional, from the internal logs named in stage 1. The format contract
is stated before any line is parsed. Every exit from the clean table is
logged under its rule, nothing is silently fixed, and the label column
is audited against the incident record before the handoff to stage 3.
The day is a fixed list, so the output never changes between runs; the
printed output is the chapter's expected-output block.
"""

print("the format contract (stated before any parsing)")
print("  field 1, host: one of 2 known names, host-a or host-b")
print("  field 2, event: one of 4 known words, login browse scan deny")
print("  field 3, links: an integer, and only 0, 1, or 2")
print("  one line holds 3 comma-separated fields, no more, no fewer")
print("  the validation card runs 4 checks per row: field count,")
print("  type, range, verdict")

# the raw day: 20 fixed lines, defects planted where the contract
# locks them (rows 3, 7, 11, 13, 16, 18); every other row is valid
raw_lines = [
    "host-a,login,1",         # row 1
    "host-b,scan,2",          # row 2
    "host-a,login",           # row 3, truncated: stops at 2 fields
    "host-a,browse,0",        # row 4
    "host-b,deny,1",          # row 5
    "host-a,scan,2",          # row 6
    "host-a,browse,0",        # row 7, an exact copy of row 4
    "host-b,login,1",         # row 8
    "host-a,deny,2",          # row 9
    "host-b,scan,0",          # row 10
    "host-a,browse,1,extra",  # row 11, overlong: a 4th field rides
    "host-b,login,2",         # row 12
    "host-a,deny,",           # row 13, missing: the links slot is empty
    "host-b,browse,1",        # row 14
    "host-a,login,0",         # row 15
    "host-a,deny,2",          # row 16, an exact copy of row 9
    "host-b,browse,2",        # row 17
    "host-b,scan,many",       # row 18, wrong type: links is a word
    "host-a,login,2",         # row 19
    "host-b,deny,0",          # row 20
]

print()
print("the raw day: 20 lines as they arrived")
for number, line in enumerate(raw_lines, 1):
    print("  " + str(number).rjust(2) + "  " + line)

known_hosts = ("host-a", "host-b")
known_events = ("login", "browse", "scan", "deny")


def structure_check(line):
    """Run the 3 structural checks of the validation card.

    Returns (fired, kind, log_text): fired names the check that
    fired, kind sorts the exit into the tally, log_text is the
    cleaning log line. A line that passes returns three Nones.
    """
    fields = line.split(",")
    if len(fields) < 3:
        return ("field count: " + str(len(fields)) + " of 3 (truncated)",
                "malformed", "exit, rule malformed truncated"
                " (the line stops at " + str(len(fields)) + " fields)")
    if len(fields) > 3:
        return ("field count: " + str(len(fields)) + " of 3 (overlong)",
                "malformed", "exit, rule malformed overlong"
                " (" + str(len(fields)) + " fields, the contract"
                " allows 3)")
    host, event, links = fields
    if links == "":
        # a missing field is not a malformed line: the slot exists,
        # the value does not, and it is never guessed
        return ("type: links is empty (missing field)", "missing",
                "exit, rule missing field quarantined"
                " (links empty, never guessed)")
    if not links.isdigit():
        return ("type: links is not a number (wrong type)", "malformed",
                "exit, rule malformed wrong type (links is the word "
                + links + ")")
    if host not in known_hosts or event not in known_events:
        return ("range: a value outside the known sets", "malformed",
                "exit, rule malformed wrong type (unknown host or"
                " event)")
    if int(links) not in (0, 1, 2):
        return ("range: links outside 0, 1, 2", "malformed",
                "exit, rule malformed wrong type (links outside 0,"
                " 1, 2)")
    return (None, None, None)


# the parse station: structure first, duplicates second, clean last
# first_seen maps each kept line to the row number that first carried it
first_seen = {}
parse_table = []
exits = []
clean_rows = []

for number, line in enumerate(raw_lines, 1):
    field_total = len(line.split(","))
    fired, kind, log_text = structure_check(line)
    if fired is None and line in first_seen:
        # a duplicate is a value match against an earlier kept row,
        # not a numbering accident; the first copy stays
        first = first_seen[line]
        fired = "duplicate: exact copy of row " + str(first)
        kind = "duplicate"
        log_text = ("exit, rule duplicate of an earlier row, first"
                    " kept (row " + str(first) + ")")
    if fired is None:
        parse_table.append((number, field_total, "none", "clean"))
        first_seen[line] = number
        clean_rows.append(number)
    else:
        parse_table.append((number, field_total, fired, "exit"))
        exits.append((number, kind, log_text))

print()
print("the parse table (the validation card, one row per line)")
print("  " + "row".rjust(3) + "  " + "fields".rjust(6) + "  " +
      "check that fired".ljust(41) + "verdict")
for entry in parse_table:
    print("  " + str(entry[0]).rjust(3) + "  " +
          str(entry[1]).rjust(6) + "  " + entry[2].ljust(41) +
          entry[3])

print()
print("the cleaning log (one line per exit, every exit by name)")
for number, kind, log_text in exits:
    print("  row " + str(number).rjust(2) + ": " + log_text)

malformed_rows = []
duplicate_rows = []
missing_rows = []
for number, kind, log_text in exits:
    if kind == "malformed":
        malformed_rows.append(number)
    elif kind == "duplicate":
        duplicate_rows.append(number)
    else:
        missing_rows.append(number)

print()
print("the cleaning tally")
print("  malformed: " + str(len(malformed_rows)) + " (rows " +
      ", ".join([str(n) for n in malformed_rows]) + ")")
print("  duplicated: " + str(len(duplicate_rows)) + " (rows " +
      ", ".join([str(n) for n in duplicate_rows]) + ")")
print("  missing: " + str(len(missing_rows)) + " (row " +
      ", ".join([str(n) for n in missing_rows]) + ")")
print("  clean: " + str(len(clean_rows)))
print("  exits: " + str(len(exits)) + ", all logged")
print("  silent changes: 0")

print()
print("  hand check: " + str(len(malformed_rows)) + " malformed + " +
      str(len(duplicate_rows)) + " duplicated + " +
      str(len(missing_rows)) + " missing = " + str(len(exits)) +
      " exits")
print("  hand check: " + str(len(raw_lines)) + " rows in - " +
      str(len(exits)) + " exits = " + str(len(clean_rows)) + " clean")
print("  clean rows: " + ", ".join([str(n) for n in clean_rows]))
hand_list = [1, 2, 4, 5, 6, 8, 9, 10, 12, 14, 15, 17, 19, 20]
if clean_rows == hand_list:
    print("  the computed clean list matches the hand list: yes")

print()
print("the label-source card (the incident record, fictional)")
print("  who labeled: the SOC analyst on duty that day")
print("  when: during the shift itself, written as the events came")
print("    in, not reconstructed later")
print("  how: the analyst worked the day's alerts and recorded which")
print("    events belonged to the incident, row by row")
print("  how reliable: one careful source for one day; trustworthy")
print("    for this day, unproven beyond it, so the audit still runs")

# the label column under audit: 4 attack and 10 benign over the 14
# clean rows; the record below covers the 10 sampled rows only
column_label = {
    1: "benign", 2: "attack", 4: "benign", 5: "benign", 6: "attack",
    8: "benign", 9: "benign", 10: "attack", 12: "attack", 14: "benign",
    15: "benign", 17: "benign", 19: "benign", 20: "benign",
}
record_label = {
    1: "benign", 2: "attack", 4: "benign", 5: "attack", 6: "attack",
    8: "benign", 9: "benign", 10: "benign", 12: "attack", 14: "benign",
}


def count_word(labels, rows, word):
    total = 0
    for number in rows:
        if labels[number] == word:
            total = total + 1
    return total


sample = clean_rows[:10]
unaudited = clean_rows[10:]
attack_before = count_word(column_label, clean_rows, "attack")
benign_before = count_word(column_label, clean_rows, "benign")

print()
print("the label audit (the first 10 clean rows, column versus record)")
print("  sample: " + ", ".join([str(n) for n in sample]))
audit_rows = []
for number in sample:
    audit_rows.append((number, column_label[number],
                       record_label[number]))
print("  " + "row".rjust(3) + "  " + "column".ljust(7) +
      "record".ljust(8) + "result")
for number, col, rec in audit_rows:
    if col == rec:
        result = "agree"
    else:
        result = "disagree, column corrected to " + rec
    print("  " + str(number).rjust(3) + "  " + col.ljust(7) +
          rec.ljust(8) + result)

corrections = []
for number, col, rec in audit_rows:
    if col != rec:
        corrections.append(number)
for number in corrections:
    # the record is the named label source, so the column moves to it
    column_label[number] = record_label[number]

attack_after = count_word(column_label, clean_rows, "attack")
benign_after = count_word(column_label, clean_rows, "benign")

print()
print("  disagreements found: " + str(len(corrections)) +
      ", one each direction")
for number, col, rec in audit_rows:
    if col != rec:
        print("  row " + str(number) + ": record says " + rec +
              ", column says " + col + ", corrected to " + rec)
print("  label column before corrections: " + str(attack_before) +
      " attack, " + str(benign_before) + " benign")
print("  label column after corrections: " + str(attack_after) +
      " attack, " + str(benign_after) + " benign")
print("  audited rows agreeing after correction: " + str(len(sample)) +
      " of " + str(len(sample)))
print("  unaudited rows, flagged: " +
      ", ".join([str(n) for n in unaudited]) + " (" +
      str(len(unaudited)) + " rows)")
print("  note: rows 6 and 10 are both scan events; after the audit")
print("  one reads attack and one reads benign, so the event word")
print("  alone never decides the label")

print()
print("the synthetic-flag check (rides every batch, per stage 1)")
generator_rows = []  # the provenance card names the internal logs
flagged = 0
for number, line in enumerate(raw_lines, 1):
    if number in generator_rows:
        flagged = flagged + 1
print("  rows carrying the synthetic flag: " + str(flagged) +
      " of " + str(len(raw_lines)))

print()
print("the handoff tally to stage 3")
print("  rows in at stage 2: " + str(len(raw_lines)))
print("  exits, all logged: " + str(len(exits)))
print("  rows to stage 3: " + str(len(clean_rows)))
print("  corrections logged: " + str(len(corrections)))
print("  rows flagged unaudited: " + str(len(unaudited)))
print("  silent changes: 0")
