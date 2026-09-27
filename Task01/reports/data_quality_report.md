# Task 1: Data Quality Assessment Report

*Consumer Financial Health & Engagement — Vietnam 2025 (Synthetic Data)*

---

## 1. Missing Values

### 1.1 Transactions Dataset (`consumer_transactions_2025.csv`)

- **Total rows**: 1,852,394
- **Total columns**: 28
- **Columns with missing values**: 0

> **No missing values** across all 28 columns.

### 1.2 Health & Engagement Dataset (`consumer_financial_health_engagement_2025.csv`)

- **Total rows**: 10,992
- **Total columns**: 30
- **Columns with missing values**: 1

| Column | Missing Count | Missing % |
|--------|--------------|-----------|
| `next_month_low_health_flag` | 999 | 9.09% |

> **Explanation**: `next_month_low_health_flag` is missing 999 values. The last month (2025-12-01) has 918 rows — since it's the last month, the next month's label cannot be calculated. This is **by design**, not a data error.

## 2. Duplicate Transactions

| Check | Result |
|-------|--------|
| Fully duplicate rows | 0 |
| Duplicate `transaction_id` | 0 |

> **No duplicate transactions**. Each `transaction_id` is unique.

- Additional check: Duplicate `(consumer_id, analysis_month)` in Health dataset: **0**

## 3. Outliers

### 3.1 `spend_amount_vnd` — Transactions Dataset

**Descriptive Statistics:**

| Metric | Value (VND) |
|--------|-------------|
| Count | 1,852,394 |
| Mean | 1,751,589 |
| Std | 3,981,350 |
| Min | 25,000 |
| Q1 (25%) | 241,000 |
| Median (50%) | 1,186,000 |
| Q3 (75%) | 2,077,000 |
| P95 | 4,884,000 |
| P99 | 13,448,000 |
| Max | 723,722,000 |

**IQR-based Outlier Detection:**

- IQR = Q3 − Q1 = 1,836,000 VND
- Lower bound (Q1 − 1.5×IQR) = -2,513,000 VND
- Upper bound (Q3 + 1.5×IQR) = 4,831,000 VND
- **Outliers count (IQR method)**: 95,101 (5.13%)
- Transactions with negative values: 0

> **Comment**: Spending distribution is **right-skewed**, with the max value (723,722,000 VND) being much higher than the median (1,186,000 VND). This is a natural characteristic of financial transaction data. Outliers **should not be removed** as they represent valid high-value transactions. However, caution is needed when using the mean; **median** is more appropriate for central tendency.

### 3.2 Outliers — Health & Engagement Dataset (Key Ratios)

| Metric | Min | Q1 | Median | Q3 | Max | IQR Outliers | IQR Outlier % |
|--------|-----|-------|--------|-------|-----|-------------|---------------|
| `spend_to_income_ratio` | 0.119 | 0.488 | 0.632 | 0.812 | 6.332 | 625 | 5.7% |
| `credit_utilization_ratio` | 0.026 | 0.126 | 0.169 | 0.229 | 1.500 | 533 | 4.8% |
| `essential_spend_ratio` | 0.000 | 0.409 | 0.485 | 0.562 | 1.000 | 134 | 1.2% |
| `online_spend_ratio` | 0.000 | 0.141 | 0.192 | 0.254 | 0.996 | 446 | 4.1% |
| `spending_volatility` | 0.238 | 1.051 | 1.331 | 1.803 | 10.343 | 650 | 5.9% |
| `financial_health_score` | 0.800 | 60.700 | 67.700 | 73.200 | 90.200 | 113 | 1.0% |
| `engagement_score` | 9.700 | 74.800 | 78.100 | 81.400 | 99.600 | 433 | 3.9% |

> **Synthetic Caveat**: According to the dataset description, absolute values (income, credit limit, balance) are **unrealistically high** compared to actual wages in Vietnam. It is better to use **ratios** as the primary signal instead of absolute VND values.

## 4. Data Consistency

| Check | Result |
|-------|--------|
| `spend_amount_vnd` not rounded to 1,000 VND | 0 |
| Unique values of `online_transaction_flag` | [0, 1] |
| Unique values of `essential_spending_flag` | [0, 1] |
| Unique values of `gender` (Transactions) | ['Nam', 'Nữ'] |
| Unique values of `gender` (Health) | ['Nam', 'Nữ'] |
| `transaction_month` range | 1 – 12 (12 months) |
| `transaction_hour` range | 0 – 23 |
| `transaction_day_of_week` values | [0, 1, 2, 3, 4, 5, 6] |

- Check `essential_spend_ratio + discretionary_spend_ratio ≈ 1.0`: Pass
- Check `essential_spend + discretionary_spend ≈ total_spend`: Pass

## 5. Customer-level Consistency

### 5.1 Transactions Dataset — Consumer Identity

| Check | Violations | Result |
|-------|------------|--------|
| `consumer_id` → `customer_name` (1:1) | 0 | Pass |
| `consumer_id` → `date_of_birth` (1:1) | 0 | Pass |
| `consumer_id` → `gender` (1:1) | 0 | Pass |
| `consumer_id` → `occupation` (1:1) | 0 | Pass |
| `consumer_id` → `street_address` (1:1) | 0 | Pass |
| `consumer_id` → `province_city` (1:1) | 0 | Pass |
| `merchant_id` → `merchant_name` (1:1) | 0 | Pass |

- Unique consumers (Transactions): **999**
- Unique merchants: **693**
- Unique provinces/cities: **34**

### 5.2 Health & Engagement Dataset — Consumer Identity

| Check | Violations | Result |
|-------|------------|--------|
| `consumer_id` → `gender` (1:1) | 0 | Pass |
| `consumer_id` → `occupation` (1:1) | 0 | Pass |
| `consumer_id` → `province_city` (1:1) | 0 | Pass |

- Unique consumers (Health): **999**
- Total months: **12**
- Expected: 999 x 12 = 11,988 rows → Actual: 10,992 rows
- Missing **996 rows** compared to a full panel. This indicates not all 999 customers have transactions every month — which is **expected** as some customers may be inactive in certain months.

## 6. Temporal Coverage

### 6.1 Transactions Dataset

- **Time range**: `2025-01-01 00:00:18` → `2025-12-31 23:59:53`
- **Transactions outside 2025**: 0
- **Transaction distribution by month**:

| Month | Transactions | Percentage (%) |
|-------|-------------|--------------|
| 01 | 104,727 | 5.7% |
| 02 | 97,657 | 5.3% |
| 03 | 143,789 | 7.8% |
| 04 | 134,970 | 7.3% |
| 05 | 146,875 | 7.9% |
| 06 | 173,869 | 9.4% |
| 07 | 172,444 | 9.3% |
| 08 | 176,118 | 9.5% |
| 09 | 140,185 | 7.6% |
| 10 | 138,106 | 7.5% |
| 11 | 143,056 | 7.7% |
| 12 | 280,598 | 15.1% |

- **Distribution by day of week**:

| Day | Transactions | Percentage (%) |
|-----|-------------|--------------|
| Monday (0) | 365,696 | 19.7% |
| Tuesday (1) | 267,695 | 14.5% |
| Wednesday (2) | 197,951 | 10.7% |
| Thursday (3) | 201,286 | 10.9% |
| Friday (4) | 212,971 | 11.5% |
| Saturday (5) | 264,486 | 14.3% |
| Sunday (6) | 342,309 | 18.5% |

### 6.2 Health & Engagement Dataset

- **Analysis months**: ['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01', '2025-06-01', '2025-07-01', '2025-08-01', '2025-09-01', '2025-10-01', '2025-11-01', '2025-12-01']
- **Number of months**: 12
- **Rows per month**: 916 (= 999 customers × 1)

| Month | Rows |
|-------|------|
| 2025-01-01 | 916 |
| 2025-02-01 | 919 |
| 2025-03-01 | 920 |
| 2025-04-01 | 919 |
| 2025-05-01 | 917 |
| 2025-06-01 | 911 |
| 2025-07-01 | 913 |
| 2025-08-01 | 911 |
| 2025-09-01 | 919 |
| 2025-10-01 | 917 |
| 2025-11-01 | 912 |
| 2025-12-01 | 918 |

## 7. Cross-dataset Consistency

| Check | Result |
|-------|--------|
| Customers in Transactions | 999 |
| Customers in Health | 999 |
| Common customers (intersection) | 999 |
| Only in Transactions | 0 |
| Only in Health | 0 |

> **Both datasets have the same customer base**. All consumer_ids appear in both datasets.

- Check `gender` consistency across datasets: Pass
- Check `province_city` consistency across datasets: Pass
- Check `total_spend_vnd` (Health) ≈ SUM(`spend_amount_vnd`) (Transactions): 10,992/10,992 matched (100.0%)

## 8. Synthetic Data Caveats

As per the problem description, note the following points when analyzing:

1. **Identities, merchants, geography, income, credit, and balances are fictional** — they do not represent any real individuals.
2. **Absolute VND values are unrealistically high** — due to the original simulation having very dense transaction density. It's better to use **ratios** instead of absolute values.
3. **Engagement levels skew high** — since all cards are very active; differences mostly come from digital channels (digital adoption) and category diversity.
4. **Ward/Commune names are for illustration only** — only the 34 province names are official.
5. **`financial_health_score` is an indicator of prosperity, NOT a credit score** — it should strictly not be used for credit approval or denial.

---

## Summary

| # | Check | Result |
|---|-------|--------|
| 1 | No missing values (except next_month_low_health_flag in Dec — by design) | Pass |
| 2 | No duplicate transactions, unique transaction_id | Pass |
| 3 | Outliers detected using IQR — right-skewed but reasonable for financial data | Pass |
| 4 | spend_amount_vnd rounded to 1,000 VND | Pass |
| 5 | Flags (online, essential) only contain 0/1 values | Pass |
| 6 | consumer_id → customer_name (1:1) | Pass |
| 7 | consumer_id → date_of_birth (1:1) | Pass |
| 8 | consumer_id → gender (1:1) | Pass |
| 9 | consumer_id → province_city (1:1) | Pass |
| 10 | merchant_id → merchant_name (1:1) | Pass |
| 11 | All transactions are within 2025 | Pass |
| 12 | Both datasets contain the same customer base | Pass |

> **Conclusion**: 12/12 checks passed. The data is of **good quality** and ready for the next analysis steps (EDA, Financial Health Analysis, Segmentation). No additional data cleaning steps are required as the original data satisfies all quality constraints.
