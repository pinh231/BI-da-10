# PHASE 7 — Financially Healthy but Low-Engagement Customers
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Cutoff Methodology

**Objective:** Identify customers who are financially healthy (i.e., low financial risk, stable finances) but exhibit significantly lower engagement than the typical customer.

### Selected Cutoffs
| Dimension | Cutoff | Rationale |
|---|---|---|
| Financial Health | ≥ 70 | Represents above-average financial health. Dataset mean = 66.3, std = 4.7. A score ≥ 70 is approximately 0.8 standard deviations above the mean — clearly in the "healthy" range. |
| Engagement Score | < 70 | Falls below the P25 of engagement (74.77) and well below the overall mean (75.40). Customers below 70 are meaningfully less engaged than the typical customer. |

### Cutoff Sensitivity Analysis
| Cutoffs | Customers | % of Base |
|---|---|---|
| Health ≥ 75 AND Engagement < 70 | 9 | 0.9% |
| **Health ≥ 70 AND Engagement < 70 (SELECTED)** | **25** | **2.5%** |
| Health ≥ 70 AND Engagement < 65 | 25 | 2.5% |
| Health ≥ 65 AND Engagement < 70 | 48 | 4.8% |

**Justification for selected cutoff (Health ≥ 70, Engagement < 70):**
- Using Health ≥ 75 yields only 9 customers — too small for meaningful profiling.
- Using Health ≥ 65 expands to 48 customers but includes many near-average health customers.
- Health ≥ 70 provides a meaningful "healthy" definition (above average) while keeping a sufficiently sized group (25 customers) for behavioral profiling.
- Engagement < 70 is chosen over < 65 because the same 25 customers satisfy both conditions — indicating these customers are concentrated in the 60–70 engagement range.

---

## 2. Group Size

| Metric | Value |
|---|---|
| Total customers | 999 |
| High-health customers (health ≥ 70) | ~271 |
| High-health + low-engagement customers | **25** |
| As % of total customer base | **2.5%** |
| As % of high-health customers | **~9.2%** |

---

## 3. Behavioral Profile

| Metric | HD Group (n=25) | All Others (n=974) | Overall (n=999) |
|---|---|---|---|
| engagement_score | **46.83** | 76.14 | 75.40 |
| financial_health_score | **74.03** | 66.10 | 66.30 |
| transaction_count_monthly_avg | **9.9** | 159.1 | 155.3 |
| recency_days | **232.0** | 11.3 | 16.9 |
| category_diversity_avg | **4.68** | 13.15 | 12.94 |
| online_spend_ratio_avg | **0.606** | 0.238 | 0.247 |
| active_days_avg | **2.00** | 27.04 | 26.41 |

---

## 4. Key Behavioral Characteristics

1. **Extremely low transaction frequency:** Average of only 9.9 transactions per month (vs. 159.1 for all others). These customers make approximately 1 transaction every 3 days, compared to ~5 per day for typical customers.

2. **Very long recency (mean 232 days):** On average, these customers last transacted approximately 7–8 months before December 31. Most had already become inactive by May 2025.

3. **Narrow category diversity (mean 4.68 of 14 possible):** These customers spend in fewer than 5 spending categories, compared to 13+ for typical customers. Their spending is highly concentrated in a few essential areas.

4. **High online spend ratio (60.6% vs. 24.7% for others):** Despite their low transaction volume, their limited spending disproportionately occurs through digital channels. This is consistent with occasional online-only purchasing (e.g., utility payments, infrequent e-commerce).

5. **Better financial health (score 74.03 vs. 66.30):** These customers maintain healthy spending-to-income and credit utilization ratios — they are financially stable, not financially stressed.

---

## 5. Interpretation

> These 25 customers represent a **financially stable, low-engagement segment** — customers who maintain adequate financial health but have significantly reduced their interaction with ITB's ecosystem. They are NOT financially vulnerable; rather, they appear to have drifted away from active product use while remaining financially responsible.

**This is NOT interpreted as churn** — no churn labels are available in this dataset. The appropriate interpretation is: these are customers at risk of becoming **dormant** or **lapsed** who currently retain good financial standing. They represent an **engagement opportunity** rather than a financial risk.

---

## 6. Business Implications

| Observation | Non-Punitive Implication |
|---|---|
| Long recency (7+ months inactive) | Proactive re-engagement campaigns: "We miss you" offers, cashback for returning activity |
| Low category diversity | Targeted vouchers for underused categories (e.g., dining, travel) to encourage broader spending |
| High financial health | These customers are creditworthy — appropriate upsell/cross-sell candidates for premium products |
| High digital ratio | They respond to digital channels — engage via mobile app push notifications, not branch visits |
| Low active days (avg 2 days/month) | Goal: increase active transaction days as primary re-engagement KPI |

---

## 7. Recommended Charts
- **Fig 3.5a:** Scatter plot of financial health score vs engagement score, with HD group highlighted in red.
- **Fig 3.5b:** Health × Engagement 2×2 quadrant matrix with group sizes.

Charts saved at: `task3/TASK_3/07_HEALTH_LOW_ENGAGEMENT/fig_3_5_health_engagement_matrix.png`
