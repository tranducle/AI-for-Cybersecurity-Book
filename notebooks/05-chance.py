"""Chapter 5 notebook: chance and evidence (fictional data only).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""


print("1. a distribution of odd characters in 20 fictional emails")
counts = {0: 2, 1: 5, 2: 6, 3: 4, 4: 2, 5: 1}
total = sum(counts.values())
print("counts per value:", counts)
print("total emails:", total)
for value in sorted(counts):
    share = counts[value] / total
    print("P(" + str(value) + " odd characters) =", counts[value], "/", total,
          "=", round(share, 3))
share_2 = counts[2] / total
share_4plus = (counts[4] + counts[5]) / total
print("P(2) =", round(share_2, 3), " P(4 or more) =", round(share_4plus, 3))

print()
print("2. expectation of a fictional phishing loss")
p_loss = 0.01
loss = 1000
per_email = p_loss * loss + (1 - p_loss) * 0
print("expected loss per email =", p_loss, "*", loss, "+",
      round(1 - p_loss, 2), "* 0 =", per_email)
print("for 500 emails:", 500, "*", per_email, "=", 500 * per_email)
die = (1 + 2 + 3 + 4 + 5 + 6) / 6
print("fair die expectation =", die, "(a value no single roll shows)")

print()
print("3. the alarm tree on 10,000 fictional events")
events = 10000
attacks = 100
benign = events - attacks
caught = 99
missed = attacks - caught
false_alarms = int(benign * 0.05)
quiet = benign - false_alarms
alarms = caught + false_alarms
print("events =", events, " attacks =", attacks, " benign =", benign)
print("caught =", caught, " missed =", missed)
print("false alarms =", false_alarms, " quiet =", quiet)
print("alarms =", caught, "+", false_alarms, "=", alarms)
print("real share =", caught, "/", alarms, "=", round(caught / alarms, 4),
      "(1 in", round(alarms / caught, 1), ")")

print()
print("4. Bayes by fractions, the same answer")
p_attack = 0.01
p_alarm_attack = 0.99
p_alarm_benign = 0.05
p_benign = 0.99
numerator = p_alarm_attack * p_attack
false_stream = p_alarm_benign * p_benign
denominator = numerator + false_stream
print("P(alarm | attack) * P(attack) =", round(numerator, 4))
print("P(alarm | benign) * P(benign) =", round(false_stream, 4))
print("P(alarm) =", round(denominator, 4))
posterior = numerator / denominator
print("P(attack | alarm) =", round(numerator, 4), "/", round(denominator, 4),
      "=", round(posterior, 4), "(", round(posterior * 100, 1), "percent )")

print()
print("5. the base-rate shift: 50 percent are attacks")
attacks2 = 5000
benign2 = 5000
caught2 = int(attacks2 * 0.99)
false2 = int(benign2 * 0.05)
alarms2 = caught2 + false2
print("caught =", caught2, " false alarms =", false2, " alarms =", alarms2)
print("real share =", caught2, "/", alarms2, "=", round(caught2 / alarms2, 4),
      "(", round(caught2 / alarms2 * 100, 1), "percent )")

print()
print("an alarm is an observation, not a verdict")
