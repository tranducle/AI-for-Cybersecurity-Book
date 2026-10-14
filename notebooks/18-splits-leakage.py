# Companion script for Ch 18: Splits, Leakage, and Class Imbalance
# Zero third-party imports; deterministic pure-Python arithmetic.

# 14 clean rows handed off from Stage 2 (Ch 16) and Stage 3 (Ch 17)
# Fields: (row_id, host, links, scan_count, label, audited)
clean_rows = [
    (1, "host_a", 0, 1, 0, True),
    (2, "host_b", 2, 5, 1, True),
    (4, "host_a", 0, 1, 0, True),
    (5, "host_b", 2, 4, 1, True),
    (6, "host_a", 2, 6, 1, True),
    (8, "host_b", 1, 1, 0, True),
    (9, "host_b", 1, 1, 0, True),
    (10, "host_a", 1, 2, 0, True),
    (12, "host_b", 2, 6, 1, True),
    (14, "host_b", 1, 1, 0, True),
    (15, "host_b", 1, 2, 0, False),
    (17, "host_c", 2, 5, 1, False),
    (19, "host_c", 0, 1, 0, False),
    (20, "host_c", 2, 4, 1, False),
]

print("the split card (6 fields, written before cutting any batch)")
print("  order rule: sort by arrival time, never random shuffle")
print("  unaudited-row rule: hold unaudited rows out of evaluation")
print("  batch cut: 60% train, 20% validate, 20% test in time order")
print("  group check: check if one host or lab VM holds the attacks")
print("  fit-only-on-train fence: scalers and samplers fit on train")
print("  test-set lock: test stays at natural base rate, judged once")
print()

# Naive 14-row cut (8 / 3 / 3) before checking the audit flag
naive_val = clean_rows[8:11]
naive_test = clean_rows[11:14]
val_un = [r[0] for r in naive_val if not r[5]]
test_un = [r[0] for r in naive_test if not r[5]]

print("naive 14-row cut (8 / 3 / 3) before checking audit flags")
print(f"  validate unaudited rows: {val_un} ({len(val_un)} row)")
print(f"  test unaudited rows: {test_un} ({len(test_un)} rows)")
print("  verdict: rejected, unaudited labels cannot score a model")
print()

# Honest Stage 4 cut: separate 4 unaudited rows into holdout tray
audited = [r for r in clean_rows if r[5]]
holdout = [r for r in clean_rows if not r[5]]
train_rows = audited[:6]
val_rows = audited[6:8]
test_rows = audited[8:10]

train_ids = [r[0] for r in train_rows]
val_ids = [r[0] for r in val_rows]
test_ids = [r[0] for r in test_rows]
holdout_ids = [r[0] for r in holdout]

train_atk = [r[0] for r in train_rows if r[4] == 1]
val_atk = [r[0] for r in val_rows if r[4] == 1]
test_atk = [r[0] for r in test_rows if r[4] == 1]

assert train_ids == [1, 2, 4, 5, 6, 8]
assert val_ids == [9, 10]
assert test_ids == [12, 14]
assert holdout_ids == [15, 17, 19, 20]

print("honest stage 4 cut on the 14 rows (6 / 2 / 2 + 4 holdout)")
print(f"  unaudited holdout tray: rows {holdout_ids} (4 rows)")
print(f"  train (6 rows, 60%): rows {train_ids}, attacks {train_atk}")
print(f"  validate (2 rows, 20%): rows {val_ids}, attacks {val_atk}")
print(f"  test (2 rows, 20%): rows {test_ids}, attacks {test_atk}")
print()

# Random-shuffle future leak and host concentration check
shuf_train = [r for r in audited if r[0] in (2, 8, 9, 10, 12, 14)]
shuf_test = [r for r in audited if r[0] in (1, 4, 5, 6)]
shuf_tr_ids = [r[0] for r in shuf_train]
shuf_te_ids = [r[0] for r in shuf_test]
max_tr_atk = max(r[0] for r in shuf_train if r[4] == 1)
early_atk = [
    r[0] for r in shuf_test if r[4] == 1 and r[0] < max_tr_atk
]

hb_rows = [r[0] for r in audited if r[1] == "host_b"]
hb_atk = [r[0] for r in audited if r[1] == "host_b" and r[4] == 1]
ha_rows = [r[0] for r in audited if r[1] == "host_a"]
ha_atk = [r[0] for r in audited if r[1] == "host_a" and r[4] == 1]

print("random-shuffle future leak and host concentration check")
print(f"  shuffled train: {shuf_tr_ids} (max atk {max_tr_atk})")
print(f"  shuffled test: {shuf_te_ids} (early {early_atk})")
print(
    f"  future leak: {len(early_atk)} test attacks arrived"
    f" before row {max_tr_atk}"
)
print(
    f"  host_b audited: {len(hb_rows)} of 10,"
    f" attacks {hb_atk} (3 of 4)"
)
print(
    f"  host_a audited: {len(ha_rows)} of 10,"
    f" attacks {ha_atk} (1 of 4)"
)
print()

# Preprocessing fence: train-only statistics vs leaked all-row stats
hb_tr = sum(1 for r in train_rows if r[1] == "host_b")
hb_all = len(hb_rows)
tr_share = hb_tr / len(train_rows)
all_share = hb_all / len(audited)

links_tr = sum(r[2] for r in train_rows)
links_val = sum(r[2] for r in val_rows)
links_te = sum(r[2] for r in test_rows)
links_all = sum(r[2] for r in audited)

# 5-flow byte scaling walk (Stage 3 table + 2 test bursts)
flows_tr = [100, 150, 200]
flows_te = [200, 400]
flows_all = flows_tr + flows_te

mean_tr = sum(flows_tr) // len(flows_tr)
max_tr = max(flows_tr)
mean_all = sum(flows_all) // len(flows_all)
max_all = max(flows_all)

sc_tr_honest = tuple(round(x / max_tr, 3) for x in flows_tr)
sc_tr_leaked = tuple(round(x / max_all, 3) for x in flows_tr)
burst_honest = 400 / max_tr
burst_leaked = 400 / max_all

# Exercise D1 4-flow walk: train [50, 150], test [100, 300]
ex_tr = [50, 150]
ex_all = [50, 150, 100, 300]
ex_mean_tr = sum(ex_tr) // len(ex_tr)
ex_max_tr = max(ex_tr)
ex_mean_all = sum(ex_all) // len(ex_all)
ex_max_all = max(ex_all)

print("preprocessing fence: train-only stats vs leaked all-row stats")
print(
    f"  host_b share on train (6 rows): {hb_tr} / 6 ="
    f" {tr_share:.1f}"
)
print(
    f"  host_b share on all 10 rows: {hb_all} / 10 ="
    f" {all_share:.1f} (leak 0.1)"
)
print(
    f"  links sums: train {links_tr}, val {links_val},"
    f" test {links_te}, all {links_all}"
)
print(f"  5-flow scaling walk: train {flows_tr}, test {flows_te}")
print(
    f"  honest train fit: mean {mean_tr}, max {max_tr}"
    f" -> {sc_tr_honest}"
)
print(
    f"  leaked all-5 fit: mean {mean_all}, max {max_all}"
    f" -> {sc_tr_leaked}"
)
print(
    f"  test burst 400 scaled: honest {burst_honest:.1f}"
    f" vs leaked {burst_leaked:.1f}"
)
print(
    f"  exercise 4-flow: train {ex_tr}"
    f" (mean {ex_mean_tr}, max {ex_max_tr})"
)
print(
    f"  exercise all-4: mean {ex_mean_all}, max {ex_max_all}"
    " (150 -> 1.0 vs 0.5)"
)
print()

# 10,000-event security stream (1% base rate, 60 / 20 / 20 cut)
s_total = 10000
s_tr, s_val, s_te = 6000, 2000, 2000
tr_atk_n, tr_ben_n = 60, 5940
val_atk_n, val_ben_n = 20, 1980
te_atk_n, te_ben_n = 20, 1980
w_ratio = tr_ben_n // tr_atk_n

print("10,000-event security stream (1% base rate, 60 / 20 / 20 cut)")
print(
    f"  train: {s_tr} events ({tr_atk_n} attack,"
    f" {tr_ben_n} benign, {w_ratio}:1)"
)
print(
    f"  validate: {s_val} events ({val_atk_n} attack,"
    f" {val_ben_n} benign, 1%)"
)
print(
    f"  test: {s_te} events ({te_atk_n} attack,"
    f" {te_ben_n} benign, 1%)"
)
print(
    "  exercise 5,000-event stream"
    " (2% base rate, 100 atk, 4900 ben):"
)
print("    train 3000 (60 attack, 2940 benign, weight 49 to 1)")
print("    validate 1000 (20 atk, 980 ben), test 1000 (20, 980)")
print()

# Four imbalance tools on the 6,000 train rows
under_rows = tr_atk_n + tr_atk_n
under_drop = tr_ben_n - tr_atk_n
over_atk = tr_atk_n * w_ratio
over_rows = tr_ben_n + over_atk
over_add = over_atk - tr_atk_n

print("four imbalance tools on 6,000 train rows (60 atk, 5,940 ben)")
print(
    f"  1. class weights: benign 1, attack {w_ratio}"
    f" -> {tr_ben_n} vs {tr_atk_n * w_ratio}"
)
print(f"     rows kept: {s_tr} (0 dropped, 0 fake rows added)")
print(
    "  2. majority undersampling: 60 attack, 60 benign"
    f" -> {under_rows} rows"
)
print(
    f"     benign dropped: {tr_ben_n} - 60 = {under_drop}"
    " (98 of 99 dropped)"
)
print(
    f"  3. random oversampling: {tr_ben_n} benign,"
    f" 60 * 99 = {over_atk} attack"
)
print(
    f"     train rows: {over_rows} ({over_add} duplicate"
    " attack rows added)"
)
print(
    f"  4. SMOTE on train: {tr_ben_n} benign,"
    f" 60 + {over_add} = {over_atk} attack"
)
print(
    f"     train rows: {over_rows} ({over_add} interpolated"
    " attack rows added)"
)
print()

# SMOTE interpolation by hand
A = (2, 4)
B = (6, 8)
C = (10, 4)
d2_ab = (B[0] - A[0]) ** 2 + (B[1] - A[1]) ** 2
d2_ac = (C[0] - A[0]) ** 2 + (C[1] - A[1]) ** 2
diff_ab = (B[0] - A[0], B[1] - A[1])


def interp(p, q, lam_num, lam_den):
    dx = (q[0] - p[0]) * lam_num // lam_den
    dy = (q[1] - p[1]) * lam_num // lam_den
    return (p[0] + dx, p[1] + dy)


s_25 = interp(A, B, 1, 4)
s_50 = interp(A, B, 2, 4)
s_75 = interp(A, B, 3, 4)
bridge_ac = interp(A, C, 1, 2)

P, Q = (1, 2), (5, 10)
pq_25 = interp(P, Q, 1, 4)
pq_50 = interp(P, Q, 2, 4)

print("SMOTE interpolation by hand (features: links, scan_count)")
print(f"  minority train points: A = {A}, B = {B}, C = {C}")
print(f"  squared distance A to B: 4^2 + 4^2 = 16 + 16 = {d2_ab}")
print(f"  squared distance A to C: 8^2 + 0^2 = 64 + 0 = {d2_ac}")
print(f"  nearest neighbor of A is B (32 < 64), diff = {diff_ab}")
print(f"  synthetic on AB: 0.25->{s_25}, 0.50->{s_50}, 0.75->{s_75}")
print(f"  outlier bridge A to C at 0.50: {bridge_ac} (in benign)")
print(
    f"  exercise P={P}, Q={Q}, diff (4, 8):"
    f" 0.25->{pq_25}, 0.5->{pq_50}"
)
print()

# Pre-split resampling trap (two failures)
T = (6, 8)
S_leak = interp(A, T, 1, 2)
d2_st = (T[0] - S_leak[0]) ** 2 + (T[1] - S_leak[1]) ** 2

tp_nat, fp_nat = 20, 180
prec_nat = tp_nat / (tp_nat + fp_nat) * 100
tp_fake = 20 * 99
prec_fake = tp_fake / (tp_fake + fp_nat) * 100

print("the pre-split resampling trap (two failures)")
print(f"  failure 1 (coordinate leak): train A = {A}, test T = {T}")
print(f"    pre-split SMOTE puts S = {S_leak} into train from test T")
print(
    f"    squared distance S to test T: {d2_st}"
    f" (vs A to T: {d2_ab})"
)
print("  failure 2 (test balance distortion on 2,000 test events):")
print(
    f"    natural 1% test (20 atk, 1980 ben):"
    f" {tp_nat} caught, {fp_nat} false"
)
print(
    f"      alarms -> {tp_nat} / {tp_nat + fp_nat} ="
    f" {prec_nat:.1f}% true precision"
)
print(
    f"    leaked 99x test (1980 atk, 1980 ben):"
    f" {tp_fake} caught, {fp_nat}"
)
print(
    f"      false alarms -> {tp_fake} / {tp_fake + fp_nat} ="
    f" {prec_fake:.1f}% fake precision"
)
print()

print("the handoff tally to stage 5")
print("  14-row table: 6 train, 2 validate, 2 test, 4 holdout")
print("  10,000-event stream: 6000 train (w=99), 2000 val, 2000 test")
print("  test rows touched by fit or SMOTE: 0")
print("  synthetic rows in validate or test: 0")
