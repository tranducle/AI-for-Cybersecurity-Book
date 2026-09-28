# Companion notebook 01: check the decoded formula (accuracy).
# The formula: accuracy = (1/n) * sum over i of 1(predicted_i == true_i).
# All values fictional; nothing here is real data.
tp, fp, fn, tn = 7, 2, 3, 8   # fictional counts of a phishing detector
n = tp + fp + fn + tn
correct = tp + tn
accuracy = correct / n
# The indicator function, one sample at a time:
predicted = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
true =      [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
indicator = [1 if p == t else 0 for p, t in zip(predicted, true)]
n2 = len(indicator)
accuracy2 = sum(indicator) / n2
print("n =", n, "| correct =", correct, "| accuracy =", accuracy)
print("indicator sum =", sum(indicator), "/ n =", n2,
      "| accuracy =", accuracy2)
print("symbol check: n (count), hat (estimate), 1(x) (indicator)")
