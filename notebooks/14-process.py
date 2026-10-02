"""Chapter 14 notebook: the whole process at once (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""

print("the running example walked through all seven stages")
print()

print("stage 1, problem framing")
print("  question: which events deserve a human look?")
print("  a flag is an invitation, not a verdict")

print()
print("stage 2, data and labels")
events = 10000
attacks = 100
print("  events:", events, " attacks:", attacks,
      " base rate:", attacks / events)

print()
print("stage 3, features")
print("  two counts: odd characters and links")
print("  the 7-email table from chapter 9 rides along by pointer")

print()
print("stage 4, model")
risk = 0.5 + 0.6 * 6
print("  risk line: risk = 0.5 + 0.6 * events")
print("  at 6 events the risk score is", round(risk, 1))
print("  the forest takes over when the story bends")

print()
print("stage 5, evaluation")
caught = 99
false_alarms = 495
alarms = caught + false_alarms
print("  the three batches: 6 train, 3 validate, 3 judge-once")
print("  the alarm column:", caught, "+", false_alarms, "=",
      alarms, "alarms")
print("  real share:", caught, "/", alarms, "=",
      round(caught / alarms, 3), "(1 in 6)")

print()
print("stage 6, deployment")
queue = int(events * 0.01)
print("  top 1 percent queue:", queue, "flags; the analyst decides")

print()
print("stage 7, monitoring")
print("  drift watch: re-check the normal and the ruler")
print("  label check: audit a sample of past flags")

print()
print("every score reports its batches, base rate, sample size,")
print("threshold, and the one-sentence what-it-cannot-say")
