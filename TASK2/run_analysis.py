#!/usr/bin/env python3
"""
Heart Failure Mortality Prediction — One-Click Reproduction Script

Run:  python run_analysis.py

Generates all figures, tables, and CSV files referenced in the LaTeX paper:
    - outlier_summary.csv
    - heatmap.png
    - feature_importance.png
    - model_performance.csv
    - roc_curve.png
"""

import os
import sys
import warnings
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless environments
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, roc_curve,
)
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

# Paths relative to script location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "heart_failure_clinical_records_dataset.csv")

# ── 1. Load data ──────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Loading dataset")
print("=" * 60)

df = pd.read_csv(DATA_PATH)
print(f"Shape: {df.shape[0]} patients × {df.shape[1]} variables")
print(f"Class distribution:\n{df['DEATH_EVENT'].value_counts().to_string()}")
print()

# ── 2. Descriptive statistics ─────────────────────────────────────────────────
print("=" * 60)
print("STEP 2: Descriptive statistics")
print("=" * 60)
print(df.describe().T.to_string())
print()

# ── 3. Missing values ─────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 3: Missing value check")
print("=" * 60)
missing = df.isnull().sum()
print(missing.to_string())
print(f"Total missing: {missing.sum()}")
print()

# ── 4. Duplicates ─────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 4: Duplicate record check")
print("=" * 60)
dup_count = df.duplicated().sum()
print(f"Duplicate rows: {dup_count}")
print()

# ── 5. Outlier detection (IQR) ────────────────────────────────────────────────
print("=" * 60)
print("STEP 5: Outlier detection (IQR method)")
print("=" * 60)

binary_cols = ["anaemia", "diabetes", "high_blood_pressure", "sex", "smoking", "DEATH_EVENT"]
continuous_cols = [c for c in df.columns if c not in binary_cols]

outlier_records = []
for col in continuous_cols:
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    lb, ub = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    n = df[(df[col] < lb) | (df[col] > ub)].shape[0]
    outlier_records.append({"variable": col, "lower_bound": lb, "upper_bound": ub, "outlier_count": n})

outlier_df = pd.DataFrame(outlier_records)
outlier_df.to_csv(os.path.join(BASE_DIR, "outlier_summary.csv"), index=False)
print(outlier_df.to_string(index=False))
print("\n(Outliers retained — extreme values reflect genuine pathophysiology.)\n")

# ── 6. Correlation heatmap ────────────────────────────────────────────────────
print("=" * 60)
print("STEP 6: Correlation heatmap")
print("=" * 60)

corr = df.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", square=True, linewidths=0.5)
plt.title("Correlation Heatmap of Clinical Variables")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "heatmap.png"), dpi=300, bbox_inches="tight")
plt.close()
print("Saved: heatmap.png")

death_corr = corr["DEATH_EVENT"].drop("DEATH_EVENT").sort_values(ascending=False)
print("Correlation with DEATH_EVENT:")
print(death_corr.to_string())
print()

# ── 7. Welch's t-test ─────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 7: Welch's t-test for risk factors")
print("=" * 60)

cont_for_ttest = ["age", "creatinine_phosphokinase", "ejection_fraction",
                  "platelets", "serum_creatinine", "serum_sodium", "time"]
ttest_rows = []
for col in cont_for_ttest:
    alive = df[df["DEATH_EVENT"] == 0][col]
    death = df[df["DEATH_EVENT"] == 1][col]
    t_stat, p_val = ttest_ind(death, alive, equal_var=False)
    ttest_rows.append({"variable": col, "alive_mean": alive.mean(), "death_mean": death.mean(),
                       "t_statistic": t_stat, "p_value": p_val})

ttest_df = pd.DataFrame(ttest_rows).sort_values("p_value")
print(ttest_df.to_string(index=False))
print()

# ── 8. Random Forest feature importance ───────────────────────────────────────
print("=" * 60)
print("STEP 8: Random Forest feature importance")
print("=" * 60)

X = df.drop(columns=["DEATH_EVENT"])
y = df["DEATH_EVENT"]

rf = RandomForestClassifier(n_estimators=500, random_state=42, class_weight="balanced")
rf.fit(X, y)

importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_
}).sort_values("importance", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=importance_df, x="importance", y="feature")
plt.title("Feature Importance Based on Random Forest")
plt.xlabel("Importance")
plt.ylabel("Clinical Variable")
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "feature_importance.png"), dpi=300, bbox_inches="tight")
plt.close()
print("Saved: feature_importance.png")
print(importance_df.to_string(index=False))
print()

# ── 9. Train/test split ──────────────────────────────────────────────────────
print("=" * 60)
print("STEP 9: Train/test split (80/20, stratified)")
print("=" * 60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train: {len(X_train)}  |  Test: {len(X_test)}")
print(f"Train class ratio: {y_train.mean():.3f}")
print(f"Test  class ratio: {y_test.mean():.3f}")
print()

# ── 10. Model training & evaluation ──────────────────────────────────────────
print("=" * 60)
print("STEP 10: Training and evaluating 4 classifiers")
print("=" * 60)

models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ]),
    "Random Forest": RandomForestClassifier(
        n_estimators=500, random_state=42, class_weight="balanced"),
    "XGBoost": XGBClassifier(
        n_estimators=300, max_depth=3, learning_rate=0.05, subsample=0.8,
        colsample_bytree=0.8, eval_metric="logloss", random_state=42),
    "MLP": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", MLPClassifier(hidden_layer_sizes=(32, 16), activation="relu",
                              solver="adam", max_iter=1000, early_stopping=True,
                              random_state=42)),
    ]),
}

results = []
roc_data = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "AUC": roc_auc_score(y_test, y_prob),
    })

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_data[name] = (fpr, tpr, roc_auc_score(y_test, y_prob))

results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(BASE_DIR, "model_performance.csv"), index=False)
print(results_df.to_string(index=False))
print("\nSaved: model_performance.csv\n")

# ── 11. ROC curves ────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 11: ROC curves")
print("=" * 60)

plt.figure(figsize=(8, 6))
for name, (fpr, tpr, auc_val) in roc_data.items():
    plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})")

plt.plot([0, 1], [0, 1], "k--", label="Random Guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves of Prediction Models")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(BASE_DIR, "roc_curve.png"), dpi=300, bbox_inches="tight")
plt.close()
print("Saved: roc_curve.png")

# Print best model
best = results_df.loc[results_df["AUC"].idxmax()]
print(f"\nBest model: {best['Model']} (AUC = {best['AUC']:.3f}, F1 = {best['F1 Score']:.3f})")
print()

# ── 12. New patient prediction ────────────────────────────────────────────────
print("=" * 60)
print("STEP 12: New patient mortality probability")
print("=" * 60)

new_patient = pd.DataFrame([{
    "age": 65, "anaemia": 1, "creatinine_phosphokinase": 250,
    "diabetes": 0, "ejection_fraction": 30, "high_blood_pressure": 1,
    "platelets": 220000, "serum_creatinine": 2.1, "serum_sodium": 134,
    "sex": 1, "smoking": 0, "time": 90,
}])

for name, model in models.items():
    prob = model.predict_proba(new_patient)[:, 1][0]
    print(f"  {name}: predicted death probability = {prob:.3f}")

print()
print("=" * 60)
print("ALL DONE — All output files regenerated.")
print("=" * 60)
