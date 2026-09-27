# PHASE 2 — Customer-Level Analytical Table
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Objective

Construct one analytical row per customer (999 rows) by aggregating monthly observations from `df_month` and computing channel adoption and true recency from `df_trans`.

---

## 2. Metrics Constructed

| Column | Source | Calculation | Business Meaning |
|---|---|---|---|
| consumer_id | df_month | Primary key | Customer identifier |
| age, gender, occupation, province_city | df_month | .first() — static fields | Customer demographics |
| months_observed | df_month | count of months present | Observation completeness (max = 12) |
| engagement_score | df_month | mean across observed months | Yearly average engagement |
| financial_health_score | df_month | mean across observed months | Yearly average financial health |
| category_diversity_avg | df_month | mean of monthly category_diversity | Typical monthly breadth of spending categories |
| category_diversity_max | df_month | max of monthly category_diversity | Broadest month — peak behavioral range |
| transaction_count_monthly_avg | df_month | mean of monthly transaction_count | Typical monthly frequency |
| transaction_count_total | df_month | sum across months | Total yearly transaction count |
| active_days_avg | df_month | mean of active_transaction_days | Avg days per month with transactions |
| online_spend_ratio_avg | df_month | mean of monthly online_spend_ratio | Digital spending behavior (reliable ratio) |
| spend_to_income_ratio_avg | df_month | mean of monthly spend_to_income_ratio | Spending intensity |
| credit_utilization_avg | df_month | mean of monthly credit_utilization_ratio | Credit usage behavior |
| spending_volatility_avg | df_month | mean of monthly spending_volatility | Consistency of spending |
| engagement_segment_mode | df_month | most frequent monthly segment | Dominant engagement tier |
| financial_health_segment_mode | df_month | most frequent monthly segment | Dominant health tier |
| recency_days | df_trans | (2025-12-31) – max(activity_datetime) | Days since last transaction in 2025 |
| uses_POS, uses_E_commerce, uses_Mobile_App, uses_QR_Payment, uses_Recurring_Payment | df_trans | 1/0 per customer | Binary channel adoption flag |
| num_channels_used | df_trans | sum of channel flags | Multi-channel breadth |

---

## 3. Key Findings from Customer-Level Table

| Metric | Mean | Median | Min | Max |
|---|---|---|---|---|
| engagement_score | 75.40 | 78.17 | — | — |
| financial_health_score | 66.30 | 66.24 | — | — |
| category_diversity_avg | 12.94 | 13.92 | 2.00 | 14.00 |
| transaction_count_monthly_avg | 155.3 | 122.6 | 3.5 | 366.0 |
| active_days_avg | 26.4 | — | — | — |
| online_spend_ratio_avg | 0.247 | 0.204 | — | — |
| recency_days | 16.9 | -1 | -1 | 361 |

---

## 4. Notes on Methodology

- **Monetary values (VND)** are excluded from the analytical table — only ratios are used.
- **`category_diversity`** in df_month represents unique spending categories per customer per month (range: 1–14, with 14 categories total in the data). This is a pre-computed field in the dataset, not manually derived here.
- **True recency** is computed from df_trans (not df_month's within-month recency field).
- File saved at: `task3/TASK_3/DATA/customer_level_analysis.csv`
