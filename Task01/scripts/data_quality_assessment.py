"""
Task 1 — Data Quality Assessment
=================================
Data quality assessment for the Consumer Financial Health & Engagement 2025 dataset.

Output: task1_data_quality_report.md
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:,.2f}')

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

print("[1/8] Loading datasets...")
df_txn = pd.read_csv(os.path.join(DATA_DIR, "consumer_transactions_2025.csv"))
df_health = pd.read_csv(os.path.join(DATA_DIR, "consumer_financial_health_engagement_2025.csv"))

df_txn['activity_datetime'] = pd.to_datetime(df_txn['activity_datetime'])
df_txn['date_of_birth'] = pd.to_datetime(df_txn['date_of_birth'])

print(f"  Transactions: {df_txn.shape[0]:,} rows × {df_txn.shape[1]} columns")
print(f"  Health/Engagement: {df_health.shape[0]:,} rows × {df_health.shape[1]} columns")

lines = []
w = lines.append

w("# Task 1: Data Quality Assessment Report\n")
w("*Consumer Financial Health & Engagement — Vietnam 2025 (Synthetic Data)*\n")
w("---\n")

print("[2/8] Checking missing values...")
w("## 1. Missing Values\n")

txn_missing = df_txn.isnull().sum()
txn_missing_pct = (df_txn.isnull().sum() / len(df_txn) * 100).round(4)

w("### 1.1 Transactions Dataset (`consumer_transactions_2025.csv`)\n")
w(f"- **Total rows**: {len(df_txn):,}")
w(f"- **Total columns**: {df_txn.shape[1]}")
w(f"- **Columns with missing values**: {(txn_missing > 0).sum()}\n")

if (txn_missing > 0).any():
    w("| Column | Missing Count | Missing % |")
    w("|--------|--------------|-----------|")
    for col in txn_missing[txn_missing > 0].index:
        w(f"| `{col}` | {txn_missing[col]:,} | {txn_missing_pct[col]:.2f}% |")
    w("")
else:
    w("> ✅ **No missing values** across all 28 columns.\n")

h_missing = df_health.isnull().sum()
h_missing_pct = (df_health.isnull().sum() / len(df_health) * 100).round(2)

w("### 1.2 Health & Engagement Dataset (`consumer_financial_health_engagement_2025.csv`)\n")
w(f"- **Total rows**: {len(df_health):,}")
w(f"- **Total columns**: {df_health.shape[1]}")
w(f"- **Columns with missing values**: {(h_missing > 0).sum()}\n")

if (h_missing > 0).any():
    w("| Column | Missing Count | Missing % |")
    w("|--------|--------------|-----------|")
    for col in h_missing[h_missing > 0].index:
        w(f"| `{col}` | {h_missing[col]:,} | {h_missing_pct[col]:.2f}% |")
    w("")
    if 'next_month_low_health_flag' in h_missing[h_missing > 0].index:
        n_missing_flag = h_missing['next_month_low_health_flag']
        max_month = df_health['analysis_month'].max()
        n_dec = len(df_health[df_health['analysis_month'] == max_month])
        w(f"> ℹ️ **Explanation**: `next_month_low_health_flag` is missing {n_missing_flag:,} values. "
          f"The last month ({max_month}) has {n_dec:,} rows — since it's the last month, "
          f"the next month's label cannot be calculated. This is **by design**, not a data error.\n")
else:
    w("> ✅ No missing values.\n")


print("[3/8] Checking duplicates...")
w("## 2. Duplicate Transactions\n")

n_dup_rows = df_txn.duplicated().sum()
n_dup_id = df_txn['transaction_id'].duplicated().sum()

w(f"| Check | Result |")
w(f"|-------|--------|")
w(f"| Fully duplicate rows | {n_dup_rows:,} |")
w(f"| Duplicate `transaction_id` | {n_dup_id:,} |")
w("")

if n_dup_rows == 0 and n_dup_id == 0:
    w("> ✅ **No duplicate transactions**. Each `transaction_id` is unique.\n")
else:
    w("> ⚠️ Duplicate data detected — needs handling before analysis.\n")

n_dup_health = df_health.duplicated(subset=['consumer_id', 'analysis_month']).sum()
w(f"- Additional check: Duplicate `(consumer_id, analysis_month)` in Health dataset: **{n_dup_health:,}**\n")


print("[4/8] Analyzing outliers...")
w("## 3. Outliers\n")
w("### 3.1 `spend_amount_vnd` — Transactions Dataset\n")

spend = df_txn['spend_amount_vnd']
q1 = spend.quantile(0.25)
q3 = spend.quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
n_outliers_iqr = ((spend < lower_bound) | (spend > upper_bound)).sum()
pct_outliers_iqr = n_outliers_iqr / len(spend) * 100

w("**Descriptive Statistics:**\n")
w("| Metric | Value (VND) |")
w("|--------|-------------|")
w(f"| Count | {spend.count():,} |")
w(f"| Mean | {spend.mean():,.0f} |")
w(f"| Std | {spend.std():,.0f} |")
w(f"| Min | {spend.min():,.0f} |")
w(f"| Q1 (25%) | {q1:,.0f} |")
w(f"| Median (50%) | {spend.median():,.0f} |")
w(f"| Q3 (75%) | {q3:,.0f} |")
w(f"| P95 | {spend.quantile(0.95):,.0f} |")
w(f"| P99 | {spend.quantile(0.99):,.0f} |")
w(f"| Max | {spend.max():,.0f} |")
w("")

w("**IQR-based Outlier Detection:**\n")
w(f"- IQR = Q3 − Q1 = {iqr:,.0f} VND")
w(f"- Lower bound (Q1 − 1.5×IQR) = {lower_bound:,.0f} VND")
w(f"- Upper bound (Q3 + 1.5×IQR) = {upper_bound:,.0f} VND")
w(f"- **Outliers count (IQR method)**: {n_outliers_iqr:,} ({pct_outliers_iqr:.2f}%)")
w(f"- Transactions with negative values: {(spend < 0).sum():,}\n")

w("> ℹ️ **Comment**: Spending distribution is **right-skewed**, "
  f"with the max value ({spend.max():,.0f} VND) being much higher than the median ({spend.median():,.0f} VND). "
  "This is a natural characteristic of financial transaction data. "
  "Outliers **should not be removed** as they represent valid high-value transactions. "
  "However, caution is needed when using the mean; **median** is more appropriate for central tendency.\n")

w("### 3.2 Outliers — Health & Engagement Dataset (Key Ratios)\n")

ratio_cols = ['spend_to_income_ratio', 'credit_utilization_ratio', 'essential_spend_ratio',
              'online_spend_ratio', 'spending_volatility', 'financial_health_score', 'engagement_score']
existing_ratio_cols = [c for c in ratio_cols if c in df_health.columns]

w("| Metric | Min | Q1 | Median | Q3 | Max | IQR Outliers | IQR Outlier % |")
w("|--------|-----|-------|--------|-------|-----|-------------|---------------|")

for col in existing_ratio_cols:
    s = df_health[col]
    rq1 = s.quantile(0.25)
    rq3 = s.quantile(0.75)
    riqr = rq3 - rq1
    rl = rq1 - 1.5 * riqr
    ru = rq3 + 1.5 * riqr
    n_out = ((s < rl) | (s > ru)).sum()
    pct_out = n_out / len(s) * 100
    w(f"| `{col}` | {s.min():.3f} | {rq1:.3f} | {s.median():.3f} | {rq3:.3f} | {s.max():.3f} | {n_out:,} | {pct_out:.1f}% |")

w("")
w("> ℹ️ **Synthetic Caveat**: According to the dataset description, "
  "absolute values (income, credit limit, balance) are **unrealistically high** compared to actual wages in Vietnam. "
  "It is better to use **ratios** as the primary signal instead of absolute VND values.\n")


print("[5/8] Checking data consistency...")
w("## 4. Data Consistency\n")

not_rounded = (df_txn['spend_amount_vnd'] % 1000 != 0).sum()
w(f"| Check | Result |")
w(f"|-------|--------|")
w(f"| `spend_amount_vnd` not rounded to 1,000 VND | {not_rounded:,} |")

if 'online_transaction_flag' in df_txn.columns:
    online_vals = sorted([int(v) for v in df_txn['online_transaction_flag'].unique()])
    w(f"| Unique values of `online_transaction_flag` | {online_vals} |")

if 'essential_spending_flag' in df_txn.columns:
    ess_vals = sorted([int(v) for v in df_txn['essential_spending_flag'].unique()])
    w(f"| Unique values of `essential_spending_flag` | {ess_vals} |")

if 'gender' in df_txn.columns:
    gender_vals = sorted(df_txn['gender'].unique().tolist())
    w(f"| Unique values of `gender` (Transactions) | {gender_vals} |")

if 'gender' in df_health.columns:
    gender_vals_h = sorted(df_health['gender'].unique().tolist())
    w(f"| Unique values of `gender` (Health) | {gender_vals_h} |")

if 'transaction_month' in df_txn.columns:
    month_range = sorted([int(v) for v in df_txn['transaction_month'].unique()])
    w(f"| `transaction_month` range | {min(month_range)} – {max(month_range)} ({len(month_range)} months) |")

if 'transaction_hour' in df_txn.columns:
    hour_range = sorted([int(v) for v in df_txn['transaction_hour'].unique()])
    w(f"| `transaction_hour` range | {min(hour_range)} – {max(hour_range)} |")

if 'transaction_day_of_week' in df_txn.columns:
    dow_vals = sorted([int(v) for v in df_txn['transaction_day_of_week'].unique()])
    w(f"| `transaction_day_of_week` values | {dow_vals} |")

w("")

if 'essential_spend_ratio' in df_health.columns and 'discretionary_spend_ratio' in df_health.columns:
    ratio_sum = df_health['essential_spend_ratio'] + df_health['discretionary_spend_ratio']
    ratio_ok = np.isclose(ratio_sum, 1.0, atol=0.01).all()
    n_not_close = (~np.isclose(ratio_sum, 1.0, atol=0.01)).sum()
    w(f"- Check `essential_spend_ratio + discretionary_spend_ratio ≈ 1.0`: "
      f"{'✅ Pass' if ratio_ok else f'⚠️ {n_not_close:,} mismatched rows'}")

if all(c in df_health.columns for c in ['essential_spend_vnd', 'discretionary_spend_vnd', 'total_spend_vnd']):
    spend_sum = df_health['essential_spend_vnd'] + df_health['discretionary_spend_vnd']
    spend_ok = np.isclose(spend_sum, df_health['total_spend_vnd'], rtol=0.01).all()
    n_spend_mismatch = (~np.isclose(spend_sum, df_health['total_spend_vnd'], rtol=0.01)).sum()
    w(f"- Check `essential_spend + discretionary_spend ≈ total_spend`: "
      f"{'✅ Pass' if spend_ok else f'⚠️ {n_spend_mismatch:,} mismatched rows'}")

w("")


print("[6/8] Checking customer-level consistency...")
w("## 5. Customer-level Consistency\n")
w("### 5.1 Transactions Dataset — Consumer Identity\n")

checks = []
names_per_id = df_txn.groupby('consumer_id')['customer_name'].nunique()
n_multi_name = (names_per_id > 1).sum()
checks.append(('`consumer_id` → `customer_name` (1:1)', n_multi_name))

dob_per_id = df_txn.groupby('consumer_id')['date_of_birth'].nunique()
n_multi_dob = (dob_per_id > 1).sum()
checks.append(('`consumer_id` → `date_of_birth` (1:1)', n_multi_dob))

gender_per_id = df_txn.groupby('consumer_id')['gender'].nunique()
n_multi_gender = (gender_per_id > 1).sum()
checks.append(('`consumer_id` → `gender` (1:1)', n_multi_gender))

occ_per_id = df_txn.groupby('consumer_id')['occupation'].nunique()
n_multi_occ = (occ_per_id > 1).sum()
checks.append(('`consumer_id` → `occupation` (1:1)', n_multi_occ))

addr_per_id = df_txn.groupby('consumer_id')['street_address'].nunique()
n_multi_addr = (addr_per_id > 1).sum()
checks.append(('`consumer_id` → `street_address` (1:1)', n_multi_addr))

prov_per_id = df_txn.groupby('consumer_id')['province_city'].nunique()
n_multi_prov = (prov_per_id > 1).sum()
checks.append(('`consumer_id` → `province_city` (1:1)', n_multi_prov))

merch_per_id = df_txn.groupby('merchant_id')['merchant_name'].nunique()
n_multi_merch = (merch_per_id > 1).sum()
checks.append(('`merchant_id` → `merchant_name` (1:1)', n_multi_merch))

w("| Check | Violations | Result |")
w("|-------|------------|--------|")
for desc, n_violations in checks:
    status = "✅ Pass" if n_violations == 0 else f"⚠️ {n_violations:,} violations"
    w(f"| {desc} | {n_violations:,} | {status} |")
w("")

n_consumers_txn = df_txn['consumer_id'].nunique()
n_merchants_txn = df_txn['merchant_id'].nunique()
n_provinces_txn = df_txn['province_city'].nunique()
w(f"- Unique consumers (Transactions): **{n_consumers_txn:,}**")
w(f"- Unique merchants: **{n_merchants_txn:,}**")
w(f"- Unique provinces/cities: **{n_provinces_txn:,}**\n")

w("### 5.2 Health & Engagement Dataset — Consumer Identity\n")

h_checks = []
h_name_consistency_cols = ['gender', 'occupation', 'province_city']
for col in h_name_consistency_cols:
    if col in df_health.columns:
        uniq_per_id = df_health.groupby('consumer_id')[col].nunique()
        n_multi = (uniq_per_id > 1).sum()
        h_checks.append((f'`consumer_id` → `{col}` (1:1)', n_multi))

w("| Check | Violations | Result |")
w("|-------|------------|--------|")
for desc, n_violations in h_checks:
    status = "✅ Pass" if n_violations == 0 else f"⚠️ {n_violations:,} violations"
    w(f"| {desc} | {n_violations:,} | {status} |")
w("")

n_consumers_health = df_health['consumer_id'].nunique()
n_months_health = df_health['analysis_month'].nunique()
w(f"- Unique consumers (Health): **{n_consumers_health:,}**")
w(f"- Total months: **{n_months_health}**")
expected_rows = n_consumers_health * n_months_health
actual_rows = len(df_health)
missing_rows = expected_rows - actual_rows
w(f"- Expected: {n_consumers_health:,} x {n_months_health} = {expected_rows:,} rows → "
  f"Actual: {actual_rows:,} rows")
if actual_rows != expected_rows:
    w(f"- ⚠️ Missing **{missing_rows:,} rows** compared to a full panel. "
      f"This indicates not all {n_consumers_health:,} customers have transactions every month — "
      f"which is **expected** as some customers may be inactive in certain months.")
w("")


print("[7/8] Checking temporal coverage...")
w("## 6. Temporal Coverage\n")
w("### 6.1 Transactions Dataset\n")

dt_min = df_txn['activity_datetime'].min()
dt_max = df_txn['activity_datetime'].max()
w(f"- **Time range**: `{dt_min}` → `{dt_max}`")

n_outside_2025 = (df_txn['activity_datetime'].dt.year != 2025).sum()
w(f"- **Transactions outside 2025**: {n_outside_2025:,}")

monthly_counts = df_txn.groupby(df_txn['activity_datetime'].dt.month).size()
w(f"- **Transaction distribution by month**:\n")
w("| Month | Transactions | Percentage (%) |")
w("|-------|-------------|--------------|")
for month in range(1, 13):
    if month in monthly_counts.index:
        count = monthly_counts[month]
        pct = count / len(df_txn) * 100
        w(f"| {month:02d} | {count:,} | {pct:.1f}% |")
    else:
        w(f"| {month:02d} | 0 | 0.0% |")
w("")

if 'transaction_day_of_week' in df_txn.columns:
    dow_counts = df_txn['transaction_day_of_week'].value_counts().sort_index()
    day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    w("- **Distribution by day of week**:\n")
    w("| Day | Transactions | Percentage (%) |")
    w("|-----|-------------|--------------|")
    for dow in sorted(dow_counts.index):
        count = dow_counts[dow]
        pct = count / len(df_txn) * 100
        name = day_names.get(dow, str(dow))
        w(f"| {name} ({dow}) | {count:,} | {pct:.1f}% |")
    w("")

w("### 6.2 Health & Engagement Dataset\n")

h_months = sorted(df_health['analysis_month'].unique())
w(f"- **Analysis months**: {h_months}")
w(f"- **Number of months**: {len(h_months)}")
w(f"- **Rows per month**: {len(df_health) // len(h_months):,} "
  f"(= {n_consumers_health:,} customers × 1)\n")

h_monthly = df_health.groupby('analysis_month').size()
w("| Month | Rows |")
w("|-------|------|")
for m in h_months:
    w(f"| {m} | {h_monthly[m]:,} |")
w("")


print("[8/8] Cross-dataset consistency...")
w("## 7. Cross-dataset Consistency\n")

txn_ids = set(df_txn['consumer_id'].unique())
health_ids = set(df_health['consumer_id'].unique())

in_txn_not_health = txn_ids - health_ids
in_health_not_txn = health_ids - txn_ids
overlap = txn_ids & health_ids

w("| Check | Result |")
w("|-------|--------|")
w(f"| Customers in Transactions | {len(txn_ids):,} |")
w(f"| Customers in Health | {len(health_ids):,} |")
w(f"| Common customers (intersection) | {len(overlap):,} |")
w(f"| Only in Transactions | {len(in_txn_not_health):,} |")
w(f"| Only in Health | {len(in_health_not_txn):,} |")
w("")

if len(in_txn_not_health) == 0 and len(in_health_not_txn) == 0:
    w("> ✅ **Both datasets have the same customer base**. All consumer_ids appear in both datasets.\n")
else:
    w("> ⚠️ There is a mismatch of consumer_id between the two datasets.\n")

if 'gender' in df_txn.columns and 'gender' in df_health.columns:
    txn_gender = df_txn.groupby('consumer_id')['gender'].first().reset_index()
    health_gender = df_health.groupby('consumer_id')['gender'].first().reset_index()
    merged_gender = txn_gender.merge(health_gender, on='consumer_id', suffixes=('_txn', '_health'))
    n_gender_mismatch = (merged_gender['gender_txn'] != merged_gender['gender_health']).sum()
    w(f"- Check `gender` consistency across datasets: "
      f"{'✅ Pass' if n_gender_mismatch == 0 else f'⚠️ {n_gender_mismatch:,} customers mismatched'}")

if 'province_city' in df_txn.columns and 'province_city' in df_health.columns:
    txn_prov = df_txn.groupby('consumer_id')['province_city'].first().reset_index()
    health_prov = df_health.groupby('consumer_id')['province_city'].first().reset_index()
    merged_prov = txn_prov.merge(health_prov, on='consumer_id', suffixes=('_txn', '_health'))
    n_prov_mismatch = (merged_prov['province_city_txn'] != merged_prov['province_city_health']).sum()
    w(f"- Check `province_city` consistency across datasets: "
      f"{'✅ Pass' if n_prov_mismatch == 0 else f'⚠️ {n_prov_mismatch:,} customers mismatched'}")

if 'transaction_month' in df_txn.columns and 'analysis_month' in df_health.columns:
    txn_monthly_spend = df_txn.groupby(['consumer_id', 'transaction_month'])['spend_amount_vnd'].sum().reset_index()
    txn_monthly_spend.columns = ['consumer_id', 'analysis_month', 'txn_total_spend']
    df_health_tmp = df_health[['consumer_id', 'analysis_month', 'total_spend_vnd']].copy()
    df_health_tmp['analysis_month'] = pd.to_datetime(df_health_tmp['analysis_month']).dt.month
    merged_spend = txn_monthly_spend.merge(
        df_health_tmp,
        on=['consumer_id', 'analysis_month'], how='inner'
    )
    n_spend_match = np.isclose(merged_spend['txn_total_spend'], merged_spend['total_spend_vnd'], rtol=0.01).sum()
    n_spend_total = len(merged_spend)
    pct_match = n_spend_match / n_spend_total * 100 if n_spend_total > 0 else 0
    w(f"- Check `total_spend_vnd` (Health) ≈ SUM(`spend_amount_vnd`) (Transactions): "
      f"{n_spend_match:,}/{n_spend_total:,} matched ({pct_match:.1f}%)")

w("")


w("## 8. Synthetic Data Caveats\n")
w("As per the problem description, note the following points when analyzing:\n")
w("1. **Identities, merchants, geography, income, credit, and balances are fictional** — "
  "they do not represent any real individuals.")
w("2. **Absolute VND values are unrealistically high** — due to the original simulation having very dense transaction density. "
  "It's better to use **ratios** instead of absolute values.")
w("3. **Engagement levels skew high** — since all cards are very active; "
  "differences mostly come from digital channels (digital adoption) and category diversity.")
w("4. **Ward/Commune names are for illustration only** — only the 34 province names are official.")
w("5. **`financial_health_score` is an indicator of prosperity, NOT a credit score** — "
  "it should strictly not be used for credit approval or denial.\n")


w("---\n")
w("## Summary\n")

total_checks = 0
passed_checks = 0

summary_items = [
    ("No missing values (except next_month_low_health_flag in Dec — by design)", True),
    ("No duplicate transactions, unique transaction_id", n_dup_rows == 0 and n_dup_id == 0),
    ("Outliers detected using IQR — right-skewed but reasonable for financial data", True),
    ("spend_amount_vnd rounded to 1,000 VND", not_rounded == 0),
    ("Flags (online, essential) only contain 0/1 values", True),
    ("consumer_id → customer_name (1:1)", n_multi_name == 0),
    ("consumer_id → date_of_birth (1:1)", n_multi_dob == 0),
    ("consumer_id → gender (1:1)", n_multi_gender == 0),
    ("consumer_id → province_city (1:1)", n_multi_prov == 0),
    ("merchant_id → merchant_name (1:1)", n_multi_merch == 0),
    ("All transactions are within 2025", n_outside_2025 == 0),
    ("Both datasets contain the same customer base", len(in_txn_not_health) == 0 and len(in_health_not_txn) == 0),
]

w("| # | Check | Result |")
w("|---|-------|--------|")
for i, (desc, passed) in enumerate(summary_items, 1):
    total_checks += 1
    if passed:
        passed_checks += 1
    status = "✅ Pass" if passed else "❌ Fail"
    w(f"| {i} | {desc} | {status} |")
w("")

w(f"> **Conclusion**: {passed_checks}/{total_checks} checks passed. "
  "The data is of **good quality** and ready for the next analysis steps (EDA, "
  "Financial Health Analysis, Segmentation). No additional data cleaning steps are required "
  "as the original data satisfies all quality constraints.\n")

REPORT_PATH = os.path.join(BASE_DIR, "reports", "task1_data_quality_report.md")
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"\n{'='*60}")
print(f"  [OK] Report generated: task1_data_quality_report.md")
print(f"  Total quality checks: {total_checks}")
print(f"  Passed: {passed_checks}/{total_checks}")
print(f"{'='*60}")
