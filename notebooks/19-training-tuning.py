# Chapter 19: Training, Tuning, and Baselines (Stage 5 in Depth)
# Companion checker script (zero imports, deterministic hand checks)

# 1. Stage 4 handoff check (14-row day and 10,000-event stream)
audited_rows = [1, 2, 4, 5, 6, 8, 9, 10, 12, 14]
holdout_rows = [15, 17, 19, 20]
links_col = [1, 2, 1, 2, 0, 0, 0, 3, 2, 1]
labels_col = [0, 1, 0, 1, 0, 0, 0, 1, 1, 0]

train_rows = audited_rows[:6]
val_rows = audited_rows[6:8]
test_rows = audited_rows[8:10]
train_links = links_col[:6]
train_y = labels_col[:6]
val_links = links_col[6:8]
val_y = labels_col[6:8]

print("stage 4 handoff received by stage 5")
print(f"  day train rows (6): {train_rows} (2 attack, 4 benign)")
print(f"  day val rows   (2): {val_rows} (1 attack, 1 benign)")
print(f"  day test rows  (2): {test_rows} (locked in vault)")
print(f"  holdout tray   (4): {holdout_rows} (unaudited)")
print("  stream batches: train 6000 (60/5940), val 2000 (20/1980)")
print("  stream test vault: 2000 (20/1980), weights 1 and 99")
print()

# 2. The 6-field training card
print("training card (6 fields before calling fit)")
print("  baseline_floor: beat 0.500 dummy and 0.775 domain rule")
print("  fitted_parameters: weights w, bias b, or split cutoffs")
print("  hyperparameter_space: constructor knobs (alpha, max_depth)")
print("  validation_scheme: val batch or expanding TimeSeriesSplit")
print("  regularization_guard: L2 penalty, depth cap, early stop")
print("  test_vault_status: 0 test evaluations during stage 5")
print()

# 3. Three-rung baseline ladder and fitted vs hyperparameter walk
val_attacks = 20
val_benign = 1980
val_total = val_attacks + val_benign

# Rung 1: most_frequent dummy (always 0)
mf_raw = val_benign / val_total
mf_rec = 0 / val_attacks
mf_spec = val_benign / val_benign
mf_bal = (mf_rec + mf_spec) / 2.0

# Rung 2: constant=1 dummy (always 1)
c1_raw = val_attacks / val_total
c1_rec = val_attacks / val_attacks
c1_spec = 0 / val_benign
c1_bal = (c1_rec + c1_spec) / 2.0

# Rung 3: 1-feature domain rule (links >= 2)
rule_tp = 12
rule_fp = 99
rule_tn = val_benign - rule_fp
rule_rec = rule_tp / val_attacks
rule_spec = rule_tn / val_benign
rule_bal = (rule_rec + rule_spec) / 2.0

print("three-rung baseline ladder on 2,000 validation events")
print(
    f"  1. most_frequent: raw {mf_raw * 100:.1f}%, "
    f"rec {mf_rec:.3f}, spec {mf_spec:.3f}, bal {mf_bal:.3f}"
)
print(
    f"  2. constant=1   : raw  {c1_raw * 100:.1f}%, "
    f"rec {c1_rec:.3f}, spec {c1_spec:.3f}, bal {c1_bal:.3f}"
)
print(
    f"  3. links >= 2   : tp {rule_tp}/20 ({rule_rec:.3f}), "
    f"fp {rule_fp}/1980 ({rule_spec:.3f}), bal {rule_bal:.3f}"
)

w_fit = 2.0
b_fit = -3.0
scores_6 = [w_fit * x + b_fit for x in train_links]
preds_6 = [1 if s > 0 else 0 for s in scores_6]
val_preds_2 = [1 if (w_fit * x + b_fit) > 0 else 0 for x in val_links]

print("fitted parameters vs constructor hyperparameters (6 train)")
print(f"  train links: {train_links}, labels: {train_y}")
print(f"  learned inside fit: w = {w_fit:.1f}, b = {b_fit:.1f}")
print(f"  linear scores w*links + b: {scores_6}")
print(f"  train preds: {preds_6}, val preds: {val_preds_2}")
print()

# 4. 3-fold TimeSeriesSplit vs 4-fold KFold on 8 pre-test rows
pre_test = audited_rows[:8]
blocks = [pre_test[0:2], pre_test[2:4], pre_test[4:6], pre_test[6:8]]

print("3-fold TimeSeriesSplit vs 4-fold KFold (8 pre-test rows)")
ts_leaks = 0
for k in range(1, 4):
    tr = []
    for b in blocks[:k]:
        tr.extend(b)
    va = blocks[k]
    leak = 1 if max(tr) > min(va) else 0
    ts_leaks += leak
    print(f"  TSS fold {k}: train {tr} -> val {va} (leak {leak})")

kf_leaks = 0
for i in range(4):
    va = blocks[i]
    tr = []
    for j in range(4):
        if j != i:
            tr.extend(blocks[j])
    if max(tr) > min(va):
        kf_leaks += 1
print(
    f"  future-in-train folds: "
    f"TimeSeriesSplit {ts_leaks}/3, KFold {kf_leaks}/4"
)
print()

# 5. 9-trial GridSearchCV vs RandomizedSearchCV on (alpha, u)
def val_score(alpha_val):
    return round(0.900 - 0.05 * abs(alpha_val - 2.0), 3)

grid_alphas = [0.0, 5.0, 10.0]
grid_us = [1, 2, 3]
grid_trials = []
for a in grid_alphas:
    for u in grid_us:
        grid_trials.append((a, u, val_score(a)))
best_grid = max(t[2] for t in grid_trials)

rand_alphas = [0.5, 1.5, 2.0, 3.0, 4.0, 5.5, 7.0, 8.5, 9.5]
rand_scores = [val_score(a) for a in rand_alphas]
best_rand = max(rand_scores)

print("9-trial search: GridSearchCV vs RandomizedSearchCV")
print("  response: score(alpha, u) = 0.900 - 0.05 * |alpha - 2.0|")
print(
    f"  3x3 grid alphas {grid_alphas} x u {grid_us}: "
    f"distinct alphas = {len(grid_alphas)}"
)
print(
    "  grid scores: "
    f"0.0->{val_score(0.0):.3f}, "
    f"5.0->{val_score(5.0):.3f}, "
    f"10.0->{val_score(10.0):.3f} (best {best_grid:.3f})"
)
print(f"  random alphas (9): {rand_alphas}")
print(f"  random scores 1-5: {rand_scores[:5]}")
print(f"  random scores 6-9: {rand_scores[5:]}")
print(
    f"  best random score: {best_rand:.3f} at alpha = 2.0 "
    f"(18/20 rec, 1782/1980 spec)"
)
print()

# 6. L2 weight penalty and decision-tree depth sweep
alpha_l2 = 0.5
n_samp = 5
factor = alpha_l2 / (2 * n_samp)
data_loss = 0.200

for name, w_vec in [
    ("W_U (spike)", (4, 2)),
    ("W_R (even) ", (2, 2)),
    ("W_C (ex 6) ", (3, 1)),
]:
    norm_sq = w_vec[0] ** 2 + w_vec[1] ** 2
    pen = factor * norm_sq
    tot = data_loss + pen
    print(
        f"L2 {name} {w_vec}: ||W||^2={norm_sq:2d}, "
        f"pen={pen:.3f}, total={tot:.3f}"
    )

print("decision-tree max_depth sweep on train and validation")
tree_sweep = [
    (1, 0.775, 0.775, "underfit stump"),
    (2, 0.910, 0.900, "selected tree"),
    (3, 0.960, 0.850, "overfit starts"),
    (6, 1.000, 0.750, "memorized leaves"),
]
for d, tr_s, va_s, note in tree_sweep:
    gap = tr_s - va_s
    print(
        f"  depth {d}: train {tr_s:.3f}, val {va_s:.3f}, "
        f"gap {gap:.3f} ({note})"
    )
print()

# 7. Deep learning training knobs and early stopping
n_train_stream = 6000
batch_sz = 200
steps_per_epoch = n_train_stream // batch_sz
w0 = 2.0
grad = 0.5
w_small = w0 - 0.01 * grad
w_good = w0 - 0.20 * grad
w_big = w0 - 1.00 * grad

print("deep learning knobs and patience-2 early stopping")
print(
    f"  minibatches: {n_train_stream} / {batch_sz} = "
    f"{steps_per_epoch} steps/epoch (150 in 5 epochs)"
)
print(
    f"  step from w0=2.0 (g=0.5): eta 0.01->{w_small:.3f}, "
    f"0.20->{w_good:.3f}, 1.00->{w_big:.3f}"
)

epochs = [
    (1, 30, 0.450, 0.820),
    (2, 60, 0.320, 0.880),
    (3, 90, 0.240, 0.900),
    (4, 120, 0.150, 0.890),
    (5, 150, 0.080, 0.870),
    (6, 180, 0.030, 0.840),
]
best_v = -1.0
best_ep = 0
wait = 0
stopped_ep = 0
for ep, stp, tl, vs in epochs:
    if vs > best_v:
        best_v = vs
        best_ep = ep
        wait = 0
        tag = "new best"
    else:
        wait += 1
        tag = f"wait {wait}"
        if wait == 2 and stopped_ep == 0:
            stopped_ep = ep
            tag = "wait 2 -> stop"
    print(
        f"  epoch {ep} ({stp:3d} steps): loss {tl:.3f}, "
        f"val {vs:.3f} ({tag})"
    )
print(
    f"  early_stopping stops at epoch {stopped_ep}, "
    f"restores epoch {best_ep} (val {best_v:.3f})"
)
print()

# 8. Stage 5 handoff tally to Stage 6
print("stage 5 handoff to stage 6 (chapter 20)")
print("  selected models: alpha=2.0 (epoch 3) and tree max_depth=2")
print("  validation score: 0.900 (beats 0.775 rule and 0.500 dummy)")
print("  test vault: 2 day rows + 2000 stream events, 0 test reads")
