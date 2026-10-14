# Chapter 21: Deployment, Monitoring, Concept Drift, and Human Loop
# Companion checker script (zero imports, deterministic hand audit)

print("stage 6 handoff received by stage 7")
print("  day train  : [1, 2, 4, 5, 6, 8] (med=1.0, w=2.0, b=-3.0)")
print("  day val    : [9, 10] (links=[0, 3], y=[0, 1], 2/2)")
print(
    "  day test   : [12, 14] (links=[2, 1], y=[1, 0], 2/2, reads=1)"
)
print("  day holdout: [15, 17, 19, 20] (raw_links=[None, 3, 0, 2])")
print("  stream test: 2000 (TP=14 FP=14 FN=6 TN=1966 F1=0.5833)")
print("  locked rule: tau=0.80, Brier=0.245, SOC cap <= 40/day")
print()

print("stage 7 deployment card (6 fields)")
print("  pipeline_bundle   : (Imputer med=1.0, Linear, Calibrator)")
print("  latency_budget    : p90 <= 500 us, throughput >= 5000/s")
print("  drift_monitor     : 3-bin links TV alarm >= 0.200")
print("  rejection_band    : quarantine p_cal in [0.40, 0.80)")
print("  human_retrain_loop: verify holdout + quarantine -> retrain")
print("  model_card        : 5-part scope, SLAs, fallback links>=2")
print()

# 1. Chained Pipeline on the 4 live holdout rows [15, 17, 19, 20]
holdout_ids = [15, 17, 19, 20]
raw_links = [None, 3, 0, 2]
train_med = 1.0
imp_links = [
    train_med if x is None else float(x) for x in raw_links
]
z_scores = [2.0 * x - 3.0 for x in imp_links]
cal_map = {-3.0: 0.01, -1.0: 0.15, 1.0: 0.55, 3.0: 0.85}
p_cals = [cal_map[z] for z in z_scores]
routes = [
    "ALERT" if p >= 0.80 else ("QUARANTINE" if p >= 0.40 else "PASS")
    for p in p_cals
]
# Live fit_transform bug: median of [3, 0, 2] is 2.0
live_med = 2.0
bug_links = [live_med if x is None else float(x) for x in raw_links]
bug_z = [2.0 * x - 3.0 for x in bug_links]

print("chained pipeline on live holdout rows [15, 17, 19, 20]")
print(f"  raw_links  : {raw_links}")
print(f"  imputed    : {imp_links} (locked train med={train_med})")
print(f"  z_scores   : {z_scores} (w=2.0, b=-3.0)")
print(f"  p_cal      : {p_cals}")
print(f"  routing    : {routes}")
print(
    f"  live fit_transform bug: med={live_med}"
    f" -> row 15 z={bug_z[0]}"
)
print()

# 2. Prediction latency (p90) and bulk throughput budget
atomic_us = [120, 130, 140, 150, 160, 170, 180, 190, 220, 450]
mean_us = sum(atomic_us) / len(atomic_us)
p90_atomic = atomic_us[8]
tp_atomic = 1000000 // p90_atomic
bulk100_batch_us = 2500
p90_bulk = bulk100_batch_us / 100.0
tp_bulk = int(1000000 / p90_bulk)
bloat_atomic = 2500
bloat_bulk = 625.0
tp_bloat = int(1000000 / bloat_bulk)

print("prediction latency (p90) and throughput (peak >= 5,000/s)")
print(
    f"  10 atomic calls (us): mean={mean_us:.1f}"
    f" p90={p90_atomic} us"
)
print(
    f"  3-feat atomic  : p90={p90_atomic:4d} us"
    f" | {tp_atomic:5d} pred/s (near)"
)
print(
    f"  3-feat bulk-100: p90={p90_bulk:4.1f} us"
    f" | {tp_bulk:5d} pred/s (PASS)"
)
print(
    f"  500-feat bloat : p90={bloat_bulk:4.1f} us"
    f" | {tp_bloat:5d} pred/s (FAIL)"
)
print()

# 3. 3-bin feature drift (TV) and 3-month time decay
bins_m1 = [1600, 300, 100]
bins_m2 = [1360, 500, 140]
bins_m3 = [1100, 700, 200]
p_m1 = [c / 2000.0 for c in bins_m1]
p_m2 = [c / 2000.0 for c in bins_m2]
p_m3 = [c / 2000.0 for c in bins_m3]
l1_m2 = sum(abs(a - b) for a, b in zip(p_m2, p_m1))
tv_m2 = 0.5 * l1_m2
l1_m3 = sum(abs(a - b) for a, b in zip(p_m3, p_m1))
tv_m3 = 0.5 * l1_m3

print("3-bin feature drift on links (2,000/month, alarm TV >= 0.200)")
r_m1 = [round(v, 3) for v in p_m1]
r_m2 = [round(v, 3) for v in p_m2]
r_m3 = [round(v, 3) for v in p_m3]
print(f"  month 1 ref : p={r_m1} L1=0.000 TV=0.000")
print(f"  month 2 mild: p={r_m2} L1={l1_m2:.3f} TV={tv_m2:.3f}")
print(f"  month 3 live: p={r_m3} L1={l1_m3:.3f} TV={tv_m3:.3f}")

months = [
    ("month 1 (TV=0.000)", 14, 14, 6, 1966),
    ("month 2 (TV=0.120)", 12, 18, 8, 1962),
    ("month 3 (TV=0.250)",  8, 16, 12, 1964),
]
print("3-month time decay of frozen detector at tau=0.80")
for label, tp, fp, fn, tn in months:
    al = tp + fp
    pr = tp / al
    rc = tp / (tp + fn)
    f1 = (2.0 * tp) / (2.0 * tp + fp + fn)
    print(
        f"  {label}: TP={tp:2d} FP={fp:2d}"
        f" FN={fn:2d} alerts={al:2d}"
    )
    print(f"    prec={pr:.4f} rec={rc:.4f} F1={f1:.4f}")
print()

# 4. Classification with rejection, human loop, and Month 4 retraining
print("month 3 rejection band [0.40, 0.80) and month 4 retraining")
print("  zone 1 auto-pass (<0.40)     : 1966 (1960 benign, 6 missed)")
print("  zone 2 quarantine [0.40,0.80):   10 (6 attacks, 4 benign)")
print("  zone 3 auto-alert (>=0.80)   :   24 (8 attacks, 16 false)")
print(
    "  human reviews: 24 + 10 = 34 <= 40"
    " | recall: 8 -> 14/20 (0.7000)"
)
print("  holdout [15, 17, 19, 20] human labels: [0, 1, 0, 1] (4/4)")

m4_cases = [
    ("month 4 human-retrained", 14, 15, 6, 1965),
    ("month 4 self-label trap",  6, 18, 14, 1962),
]
for label, tp, fp, fn, tn in m4_cases:
    al = tp + fp
    pr = tp / al
    rc = tp / (tp + fn)
    f1 = (2.0 * tp) / (2.0 * tp + fp + fn)
    print(
        f"  {label}: TP={tp:2d} FP={fp:2d}"
        f" FN={fn:2d} alerts={al:2d}"
    )
    print(f"    prec={pr:.4f} rec={rc:.4f} F1={f1:.4f}")
print("  part III 7-stage loop complete -> ready for part IV cases")
