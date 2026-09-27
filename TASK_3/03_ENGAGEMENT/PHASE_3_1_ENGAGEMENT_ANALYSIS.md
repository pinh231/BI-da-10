# PHASE 3.1 — Engagement Score Distribution
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Methodology

**Analysis level:** Customer level (999 customers), using yearly average `engagement_score` aggregated from the 12-month df_month dataset.

**Cutoff methodology:** The engagement segments and their boundaries are pre-defined in the source dataset (`engagement_segment` column in df_month). The boundaries were **verified from the actual data**:

| Segment (English) | Segment (Vietnamese) | Score Range | Verification |
|---|---|---|---|
| Very High Engagement | Tương tác rất cao | ≥ 80.0 | Verified min=80.0, max=99.6 |
| High Engagement | Tương tác cao | 60.0 – 79.9 | Verified min=60.1, max=79.9 |
| Moderate Engagement | Tương tác trung bình | 40.0 – 59.9 | Verified min=40.5, max=59.9 |
| Low Engagement | Tương tác thấp | < 40.0 | Verified min=9.7, max=39.7 |

**Decision:** We adopt the dataset's pre-defined boundaries (40 / 60 / 80) because (a) they are consistent across all 10,992 monthly observations, (b) they create meaningful behavioral distinctions confirmed by the data, and (c) using the pre-existing field avoids introducing subjective additional thresholds.

---

## 2. Descriptive Statistics (Customer Level, Yearly Average)

| Statistic | Value |
|---|---|
| N (customers) | 999 |
| Mean | 75.40 |
| Median | 78.17 |
| Standard Deviation | 9.31 |
| Min | ~9.7 (yearly avg of a low-engagement customer) |
| Max | ~99.6 |
| P10 | ~70.60 |
| P25 | 74.77 |
| P75 | 79.92 |
| P90 | ~84.90 |

**Distribution shape:** The distribution is **left-skewed** (mean < median indicates a tail toward low engagement). The vast majority of customers cluster in the 70–85 range.

---

## 3. Customer Counts by Segment

| Segment | Customers (n) | Percentage |
|---|---|---|
| Very High Engagement (≥80) | 241 | 24.1% |
| High Engagement (60–79.9) | 668 | 66.9% |
| Moderate Engagement (40–59.9) | 80 | 8.0% |
| Low Engagement (<40) | 10 | 1.0% |
| **Total** | **999** | **100%** |

---

## 4. Key Findings

1. **The customer base is predominantly engaged:** 91.0% of customers fall in the High or Very High engagement tier. The product ecosystem successfully retains most active customers at a high engagement level.

2. **A meaningful tail of disengaged customers exists:** 9.0% of customers (90 customers) score in the Moderate or Low engagement tiers. While small in percentage, these represent meaningful recovery/intervention opportunities.

3. **Bimodal concentration:** Scores cluster around 75–80 (High Engagement peak) with a secondary cluster around 82–86 (Very High). The distribution is not uniform — most customers are concentrated in a narrow "High" band rather than spread across the full 0–100 range.

4. **Low engagement is rare but extreme:** The 10 Low Engagement customers have scores as low as ~9.7, indicating near-total disengagement — a severity that warrants targeted intervention.

---

## 5. Business Interpretation

The high concentration of customers in the High Engagement segment suggests ITB's product ecosystem maintains strong baseline engagement. However, this also means the **critical differentiation lies within the "High" band (60–80)**: customers near the lower boundary of this tier may be at risk of sliding into Moderate Engagement.

The Moderate and Low tiers, though small, are strategically important: re-engaging these customers represents low-cost recovery opportunities compared to acquiring new customers.

---

## 6. Recommended Charts
- **Fig 3.1a:** Histogram of engagement score (customer-level yearly average) with mean, median, and segment cutoff lines.
- **Fig 3.1b:** Horizontal bar chart of customer counts per engagement segment.

Charts saved at: `task3/TASK_3/03_ENGAGEMENT/fig_3_1_engagement_distribution.png`
