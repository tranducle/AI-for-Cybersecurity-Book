# Chapter 20: Evaluation, Metrics, Calibration, and Interpretation
# Stage 6 in depth on our running intrusion-detection example.
# Standard library only (zero imports).


def section(title):
    print(title)


# 1. Stage 5 handoff and Stage 6 evaluation card
section("stage 5 handoff received by stage 6")
day_train = [1, 2, 4, 5, 6, 8]
day_val = [9, 10]
day_test = [12, 14]
day_holdout = [15, 17, 19, 20]
print("  day train  :", day_train, "(w=2.0, b=-3.0)")
print("  day val    :", day_val, "(links=[0, 3], y=[0, 1])")
print("  day test   :", day_test, "(links=[2, 1], y=[1, 0], locked)")
print("  day holdout:", day_holdout, "(unaudited)")
print("  stream val : 2000 (20 attack, 1980 benign)")
print("  stream test: 2000 (20 attack, 1980 benign, locked)")
print("  stage 5 winner: alpha=2.0, max_depth=2 (val bal 0.900)")
print("  test_reads entering stage 6: 0")
print()

section("stage 6 evaluation card (6 fields)")
print("  confusion_counts : TP=18, FP=198, FN=2, TN=1782 (tau=0.50)")
print("  operating_thresh : tau=0.80 (<=40 daily SOC alert budget)")
print("  curve_summary    : ROC (0.100,0.900) vs PR (0.900,0.0833)")
print("  calibration_check: 5-alert Brier 0.330 raw -> 0.240 cal")
print("  attribution_audit: perm drop 0.450; SHAP +0.600, +0.200")
print("  single_pass_test : unlock test once (test_reads: 0 -> 1)")
print()


# 2. Confusion matrix and 1% base-rate metrics on 2,000 val events
def metrics_from_counts(tp, fp, fn, tn):
    alerts = tp + fp
    rec = tp / (tp + fn)
    fpr = fp / (fp + tn)
    spec = tn / (fp + tn)
    bal = (rec + spec) / 2.0
    prec = tp / alerts if alerts > 0 else 0.0
    f1 = (2.0 * tp) / (2.0 * tp + fp + fn)
    return alerts, rec, fpr, spec, bal, prec, f1


section("confusion matrix and base-rate shock on 2,000 val events")
for label, (tp, fp, fn, tn) in [
    ("baseline links>=2", (12, 99, 8, 1881)),
    ("winner at tau=0.50", (18, 198, 2, 1782)),
]:
    al, rec, fpr, spec, bal, prec, f1 = metrics_from_counts(
        tp, fp, fn, tn
    )
    print(
        f"  {label:18s}: TP={tp:2d} FP={fp:3d} FN={fn:1d}"
        f" TN={tn:4d} alerts={al:3d}"
    )
    print(
        f"    TPR={rec:.3f} FPR={fpr:.3f} bal={bal:.3f}"
        f" | prec={prec:.4f} F1={f1:.4f}"
    )
print()


# 3. 3-threshold sweep (ROC vs PR) for a 40-alert SOC triage desk
section("3-threshold sweep on 2,000 val events (SOC cap <= 40)")
thresholds = [
    (0.20, 19, 396, 1, 1584),
    (0.50, 18, 198, 2, 1782),
    (0.80, 15, 15, 5, 1965),
]
for tau, tp, fp, fn, tn in thresholds:
    al, rec, fpr, spec, bal, prec, f1 = metrics_from_counts(
        tp, fp, fn, tn
    )
    ok = "SELECT" if al <= 40 else "flood"
    print(
        f"  tau={tau:.2f}: TP={tp:2d} FP={fp:3d} alerts={al:3d}"
        f" ({ok:6s}) ROC=({fpr:.4f},{rec:.3f})"
    )
    print(
        f"    PR=(rec={rec:.3f}, prec={prec:.4f})"
        f" | F1={f1:.4f} bal={bal:.4f}"
    )
print()


# 4. Probability calibration: 5-alert Brier score and 3-bin diagram
section("probability calibration: 5-alert Brier score and 3 bins")
y_five = [1, 1, 0, 1, 0]
emp_five = sum(y_five) / len(y_five)
for name, p_val in [
    ("raw p=0.90", 0.90),
    ("cal p=0.60", 0.60),
    ("half p=0.50", 0.50),
]:
    sq_list = [round((y - p_val) ** 2, 4) for y in y_five]
    sq_sum = sum(sq_list)
    bs = sq_sum / len(y_five)
    gap = abs(p_val - emp_five)
    print(
        f"  {name:10s}: sum_sq={sq_sum:.2f} Brier={bs:.3f}"
        f" | emp={emp_five:.3f} gap={gap:.3f}"
    )

bins = [
    ("low ", 1920, 2, 0.020, 0.001),
    ("mid ", 50, 3, 0.350, 0.060),
    ("high", 30, 15, 0.850, 0.500),
]
for bname, n_b, pos_b, p_raw, p_cal in bins:
    emp_b = pos_b / n_b
    print(
        f"  bin {bname} (n={n_b:4d}, pos={pos_b:2d}):"
        f" emp={emp_b:.4f} raw={p_raw:.3f} cal={p_cal:.3f}"
    )
print()


# 5. Global permutation importance and local SHAP/LIME on row 10
section("global permutation importance on validation (base F1=0.600)")
base_f1 = 0.600
for feat, shuf_f1 in [
    ("links   ", 0.150),
    ("bytes_kb", 0.480),
    ("noise_id", 0.600),
]:
    drop = base_f1 - shuf_f1
    print(
        f"  shuffle {feat}: F1 {base_f1:.3f} -> {shuf_f1:.3f}"
        f" (drop={drop:.3f})"
    )

section("local 2-feature SHAP and LIME on row 10 (links=3, bytes=8)")
v_empty = 0.010
v_links = 0.510
v_bytes = 0.110
v_both = 0.810
o1_links = v_links - v_empty
o1_bytes = v_both - v_links
o2_bytes = v_bytes - v_empty
o2_links = v_both - v_bytes
phi_links = (o1_links + o2_links) / 2.0
phi_bytes = (o1_bytes + o2_bytes) / 2.0
tot_shap = v_empty + phi_links + phi_bytes
lime_pred = 0.010 + 0.200 * 3 + 0.025 * 8
print(
    f"  order 1 (links->bytes): +{o1_links:.3f}, +{o1_bytes:.3f}"
)
print(
    f"  order 2 (bytes->links): +{o2_bytes:.3f}, +{o2_links:.3f}"
)
print(
    f"  SHAP: base={v_empty:.3f} phi_links=+{phi_links:.3f}"
    f" phi_bytes=+{phi_bytes:.3f} sum={tot_shap:.3f}"
)
print(f"  LIME: 0.010 + 0.200*3 + 0.025*8 = {lime_pred:.3f}")
print()


# 6. Unlocking the test vault once (test_reads: 0 -> 1)
section("single-pass test vault audit (test_reads: 0 -> 1)")
test_links = [2, 1]
test_y = [1, 0]
test_scores = [round(2.0 * x - 3.0, 1) for x in test_links]
test_preds = [1 if z >= 0.0 else 0 for z in test_scores]
print(
    f"  day test [12, 14]: z={test_scores} preds={test_preds}"
    f" y={test_y} (2/2)"
)
for label, (tp, fp, fn, tn) in [
    ("test baseline links>=2", (12, 99, 8, 1881)),
    ("test winner tau=0.80  ", (14, 14, 6, 1966)),
]:
    al, rec, fpr, spec, bal, prec, f1 = metrics_from_counts(
        tp, fp, fn, tn
    )
    print(
        f"  {label}: TP={tp:2d} FP={fp:2d} FN={fn:1d}"
        f" TN={tn:4d} alerts={al:3d}"
    )
    print(
        f"    prec={prec:.4f} rec={rec:.4f} F1={f1:.4f} bal={bal:.4f}"
    )
print("  stage 6 handoff to stage 7: test_reads = 1, Brier = 0.245")
