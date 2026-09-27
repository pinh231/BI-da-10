# PHASE 1 — Data Preparation
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Cleaning Decisions — Dataset 1 (consumer_financial_health_engagement_2025.csv)

| Issue | Found | Action | Impact |
|---|---|---|---|
| Duplicate rows | 0 | None required | None |
| Missing values (all except next_month_low_health_flag) | 0 | None required | None |
| Missing next_month_low_health_flag (December 2025) | 999 rows | Excluded from Task 3 (not needed) | None |
| Missing customer-months (10,992 of 11,988 expected) | 996 missing rows | Compute per-customer metrics as averages over observed months, record months_observed | Minor — results represent observed months only |
| Monetary values (VND) are synthetically inflated | All customers | Use ratios only: online_spend_ratio, spend_to_income_ratio, credit_utilization_ratio | Ratios are reliable; absolute VND figures are NOT used |

## 2. Cleaning Decisions — Dataset 2 (consumer_transactions_2025.csv)

| Issue | Found | Action | Impact |
|---|---|---|---|
| Duplicate transaction_ids | 0 | None | None |
| Duplicate full rows | 0 | None | None |
| Missing values | 0 in all 28 columns | None | None |
| Dates outside 2025 | 0 | None | None |
| Negative spend_amount_vnd | 0 | None | None |
| spend_amount_vnd outliers | Max = 728M VND (~29,000 USD) | Not removed — synthetic data, ratio analysis makes absolute value irrelevant | None |

## 3. Recency Calculation Note

**Decision:** True customer recency is computed from `df_trans` using:

```
recency_days = reference_date - max(activity_datetime per customer)
reference_date = 2025-12-31
```

**Reason:** The `transaction_recency_days` column in df_month represents within-month recency (days since the last transaction within that specific month), not yearly recency. For Task 3.4, we need the time elapsed since each customer's most recent transaction across the full 2025 period.

**Result:** 909 of 999 customers (90.9%) have `recency_days ≤ 0`, meaning they transacted on or after December 31, 2025 (recency_days = -1 indicates transaction on exactly Dec 31). Only 90 customers (9.0%) have a recency > 0 days, indicating inactivity in the last days of 2025.

## 4. No Outlier Removal

Following the competition brief's guidance that data is synthetic, no outliers were removed from `engagement_score`, `financial_health_score`, or transaction counts. Extreme values (e.g., max engagement_score = 99.6, min = 9.7) are retained as they represent genuine behavioral extremes in the dataset.

## 5. Final Datasets Used in Analysis

| Dataset | Rows | Columns | Usage |
|---|---|---|---|
| df_month (cleaned) | 10,992 | 30 | Task 3.1, 3.3 (monthly-grain analysis) |
| df_trans (cleaned) | 1,852,394 | 28 | Task 3.2 (channel), Task 3.4 (recency) |
| customer_level_analysis.csv | 999 | 27 | All customer-level analysis (Tasks 3.1–3.5) |
