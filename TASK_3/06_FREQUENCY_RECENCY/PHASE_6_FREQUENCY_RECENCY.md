# PHASE 6 — Transaction Frequency & Recency
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Definitions

### Frequency
**Metric used:** `transaction_count_monthly_avg` — average number of transactions per observed month per customer.

**Formula:**
```
transaction_count_monthly_avg = sum(monthly transaction_count) / months_observed
```

**Alternative metric considered:** `active_transaction_days` (average days per month with at least one transaction) — included as supplementary measure. This proves to be even more strongly correlated with engagement (r = 0.943).

### Recency
**Metric used:** `recency_days` — calendar days between a customer's last transaction in 2025 and the reference date.

**Formula:**
```
recency_days = 2025-12-31 - max(activity_datetime per customer)
```

**Reference date justification:** December 31, 2025 is the last day of the observation period. Using this date measures how recently, relative to the end of the dataset, each customer last transacted. A lower recency_days value = more recent activity = more engaged customer.

---

## 2. Frequency — Descriptive Statistics

| Statistic | Value |
|---|---|
| Mean (monthly avg txn count) | 155.3 |
| Median | 122.6 |
| Min | 3.5 |
| Max | 366.0 |
| Correlation with engagement_score | **r = 0.643** |

**Interpretation:** The distribution is right-skewed (mean > median), with a small number of very high-frequency customers pulling the mean up. A typical customer makes ~123 transactions per month. The positive correlation (r = 0.643) confirms that more frequent transacting is associated with higher engagement.

---

## 3. Recency — Descriptive Statistics

| Statistic | Value |
|---|---|
| Mean recency_days | 16.9 |
| Median recency_days | -1 (i.e., transacted on Dec 31) |
| Min | -1 |
| Max | 361 |
| Customers with recency ≤ 0 days | 909 (90.9%) |
| Correlation with engagement_score | **r = -0.783** |

**Note on recency = -1:** A value of -1 indicates the customer's last transaction was on December 31, 2025 itself. This is the most recent possible recency value in the dataset.

**Interpretation:** 90.9% of customers transacted on or very close to December 31, 2025, meaning the vast majority of customers remained active through year-end. The 9.1% with recency > 0 days are customers who had already stopped transacting before December 31 — these are the customers worth monitoring.

The negative correlation (r = -0.783) confirms: **higher recency days = longer since last transaction = lower engagement score.** Recency is a strong inverse predictor of engagement.

---

## 4. Active Transaction Days

| Statistic | Value |
|---|---|
| Mean (active days per month) | 26.4 |
| Correlation with engagement_score | **r = 0.943** |

Active transaction days is the **strongest individual predictor of engagement** among the frequency/recency metrics. Customers who transact on more calendar days per month consistently show higher engagement scores.

---

## 5. Relationship Summary

| Metric | Correlation with Engagement | Direction |
|---|---|---|
| active_days_avg | 0.943 | Positive — more active days → higher engagement |
| category_diversity_avg | 0.938 | Positive — more categories → higher engagement |
| transaction_count_monthly_avg | 0.643 | Positive — more transactions → higher engagement |
| recency_days | -0.783 | Negative — more days since last txn → lower engagement |
| online_spend_ratio_avg | -0.674 | Negative — higher digital ratio → lower engagement |

---

## 6. Key Findings

1. **Active days per month is the strongest frequency predictor of engagement (r = 0.943):** Customers who transact across more days each month — not just more total transactions — are consistently the most engaged. This suggests that **behavioral regularity** (spreading activity across the month) matters more than transaction volume alone.

2. **Recency is a strong negative predictor (r = -0.783):** Customers who stopped transacting earlier in the year have markedly lower engagement scores. The High Health + Low Engagement group has a mean recency of 232 days — more than 7 months of inactivity.

3. **90.9% of customers are "recent" (transacted on or close to Dec 31, 2025):** Recency is a highly effective separator for the disengaged minority rather than a general differentiator across the full customer base.

---

## 7. Business Implications

- **Frequency intervention:** Encourage customers to spread transactions across more days per month (e.g., incentivize using the card for daily small purchases, not just monthly big-ticket items).
- **Recency monitoring:** Customers who have not transacted for 30+ days should trigger a proactive re-engagement notification or offer.
- **Caution:** Do NOT interpret recency as a churn indicator — no churn labels are available in this dataset. Interpret as "potential disengagement signal" requiring follow-up.

---

## 8. Recommended Charts
- **Fig 3.4a:** Histogram of monthly transaction frequency per customer.
- **Fig 3.4b:** Histogram of recency days per customer.
- **Fig 3.4c:** Scatter plot of frequency vs engagement score.
- **Fig 3.4d:** Scatter plot of recency vs engagement score.

Charts saved at: `task3/TASK_3/06_FREQUENCY_RECENCY/fig_3_4_frequency_recency.png`
