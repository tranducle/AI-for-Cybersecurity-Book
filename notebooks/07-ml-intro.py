"""Chapter 7 notebook: what machine learning actually is (fictional data).

Every number here is invented for the book. The notebook is a checker,
not a substitute for doing the arithmetic by hand first.
"""


def predict(count, threshold):
    """The learned rule: phishing when the count is at least the threshold."""
    return "phishing" if count >= threshold else "benign"


def errors(batch, threshold):
    """Count wrong answers on a batch at a given threshold."""
    wrong = 0
    for count, label in batch:
        if predict(count, threshold) != label:
            wrong += 1
    return wrong


train = [(1, "benign"), (2, "benign"), (4, "phishing"),
         (5, "phishing"), (5, "phishing"), (8, "phishing")]
validate = [(1, "benign"), (3, "benign"), (7, "phishing")]
test = [(2, "benign"), (6, "phishing"), (9, "phishing")]

print("1. the training batch and the threshold sweep")
half = len(train) // 2
print("train:", ", ".join(f"({c}, '{l}')" for c, l in train[:half]) + ",")
print("       " + ", ".join(f"({c}, '{l}')" for c, l in train[half:]))
candidates = [0.5, 1.5, 3, 4.5, 6.5]
for t in candidates:
    print("threshold", t, " train errors:", errors(train, t), "of", len(train))
print("the learner picks threshold 3 (0 of 6; any line above 2 and at most 4 works)")

print()
print("2. tune on the validation batch")
print("validate:", validate)
print("threshold 3:")
for count, label in validate:
    mark = "ok" if predict(count, 3) == label else "WRONG"
    print(f"  ({count}, {label} -> {predict(count, 3)}, {mark})")
print("threshold 3 validate errors:", errors(validate, 3), "of 3")
print("threshold 6 validate errors:", errors(validate, 6), "of 3")
print("the tiny validate batch flips the ranking; tiebreak on train errors")
print("(0 of 6 versus 3 of 6) keeps threshold 3; the graze at (3, benign) is disclosed")

print()
print("3. judge once on the test batch")
print("test:", test)
print("threshold 3:")
for count, label in test:
    mark = "ok" if predict(count, 3) == label else "WRONG"
    print(f"  ({count}, {label} -> {predict(count, 3)}, {mark})")
right = len(test) - errors(test, 3)
print("test errors:", errors(test, 3), "of 3  accuracy:", right, "/", len(test))

print()
print("4. the honesty checklist")
phishing_total = sum(1 for _, label in train + validate + test if label == "phishing")
print("base rate in this fictional dataset:", phishing_total, "of", len(train + validate + test),
      "emails are phishing")
print("three tiny batches: 12 events is a small observation, not a verdict")
print("a learned rule is arithmetic, not understanding")
