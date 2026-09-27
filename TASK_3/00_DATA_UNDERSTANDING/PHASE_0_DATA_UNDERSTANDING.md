# PHASE 0 — Data Understanding
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Files Identified in Workspace

| File | Size | Purpose |
|---|---|---|
| `consumer_financial_health_engagement_2025.csv` | ~3.3 MB | Monthly customer-level aggregated metrics |
| `consumer_transactions_2025.csv` | ~597 MB | Individual transaction records |
| `consumer_financial_health_case_study.md` | 9.8 KB | Competition business brief |
| `data_dictionary.xlsx` | 18 KB | Column-level definitions |

---

## 2. Dataset 1: `consumer_financial_health_engagement_2025.csv`

### Grain Verification
> **One row = one customer × one calendar month (2025)**

- Verified: every `(consumer_id, analysis_month)` pair appears exactly once.
- **Rows:** 10,992
- **Columns:** 30
- **Unique customers:** 999
- **Unique months:** 12 (January–December 2025)
- Note: 999 × 12 = 11,988 expected, but only 10,992 actual rows → **996 customer-months are missing** (some customers not active all 12 months).

### Date Range
- `analysis_month` min: `2025-01-01`
- `analysis_month` max: `2025-12-01`

### Missing Values
| Column | Missing |
|---|---|
| `next_month_low_health_flag` | 999 rows (December 2025 has no "next month") — expected |
| All other columns | 0 |

### Duplicate Records
- 0 duplicate rows.

### Key Columns for Task 3

| Column | Type | Business Meaning |
|---|---|---|
| consumer_id | str | Primary customer identifier |
| analysis_month | str (date) | Calendar month of aggregation |
| engagement_score | float | Monthly engagement score (0–100) |
| engagement_segment | str | Categorical label from score |
| financial_health_score | float | Monthly financial health score (0–100) |
| financial_health_segment | str | Categorical label from health score |
| transaction_count | int | Transactions in the month |
| active_transaction_days | int | Days with at least one transaction |
| transaction_recency_days | int | Days since last transaction (within month) |
| category_diversity | int | Unique spending categories used in the month |
| online_spend_ratio | float | Online spend / total spend |
| spend_to_income_ratio | float | Total spend / monthly income |
| credit_utilization_ratio | float | Credit used / credit limit |
| spending_volatility | float | Variability in spending amounts |

### Engagement Segment Boundaries (Verified from Data)
| Segment (Vietnamese) | English Label | Score Range |
|---|---|---|
| Tương tác rất cao | Very High Engagement | 80.0 – 99.6 |
| Tương tác cao | High Engagement | 60.1 – 79.9 |
| Tương tác trung bình | Moderate Engagement | 40.5 – 59.9 |
| Tương tác thấp | Low Engagement | 9.7 – 39.7 |

---

## 3. Dataset 2: `consumer_transactions_2025.csv`

### Grain Verification
> **One row = one transaction**

- Verified: `transaction_id` is unique across all 1,852,394 rows.
- **Rows:** 1,852,394
- **Columns:** 28
- **Unique customers:** 999
- **Duplicate transaction IDs:** 0
- **Duplicate full rows:** 0

### Date Range
- `activity_datetime` min: `2025-01-01 00:00:18`
- `activity_datetime` max: `2025-12-31 23:59:53`

### Missing Values — None across all 28 columns.

### Transaction Channels (Verified)
| Channel | Transactions | Share | Online Flag |
|---|---|---|---|
| POS | 1,089,518 | 58.8% | Always offline (0) |
| QR Payment | 367,682 | 19.9% | Always offline (0) |
| E-commerce | 161,670 | 8.7% | Always online (1) |
| Mobile App | 142,399 | 7.7% | Always online (1) |
| Recurring Payment | 91,125 | 4.9% | Always online (1) |

> Online channels = E-commerce + Mobile App + Recurring Payment. There is no ambiguity: each channel maps exclusively to either online or offline.

### Spending Categories — 14 unique categories verified in the data.

---

## 4. Dataset Relationship

Linked by `consumer_id`. Monthly aggregates in Dataset 1 are derived from raw transactions in Dataset 2. For Task 3, most customer-level metrics come from Dataset 1; Dataset 2 is used for channel adoption (unique customers per channel) and true recency calculation.

---

## 5. Important Data Quality Findings

| Finding | Impact | Action Taken |
|---|---|---|
| 996 missing customer-months | Some customers active <12 months | Use monthly averages, record months_observed |
| VND monetary values are synthetic | Absolute VND unreliable | Use ratios only |
| next_month_low_health_flag missing Dec | Expected | Excluded from Task 3 |
| transaction_recency_days is within-month | ≠ yearly recency | Compute true recency from df_trans with reference_date = 2025-12-31 |
| Engagement distribution heavily concentrated in High/Very High (99%) | Low/Moderate segments are very small | Document limitation explicitly |

---

## 6. Implications for Task 3

| Task | Primary Dataset | Key Variables |
|---|---|---|
| 3.1 Engagement Distribution | df_month | engagement_score, engagement_segment |
| 3.2 Channel Adoption | df_trans + df_month | transaction_channel, online_spend_ratio |
| 3.3 Category Diversity | df_month | category_diversity, engagement_score |
| 3.4 Frequency & Recency | df_month + df_trans | transaction_count, active_transaction_days, recency_days |
| 3.5 Healthy + Low Engagement | df_month → customer level | financial_health_score, engagement_score |
