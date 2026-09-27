# PHASE 5 — Category Diversity & Engagement
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Definition

**Category diversity** (`category_diversity` in df_month) = number of unique spending categories a customer used within a given calendar month.

**Important distinctions:**
- This is NOT the number of transactions.
- This is NOT the number of merchants.
- This is the number of **distinct spending category types** (e.g., Food & Beverage, Transportation, Healthcare, etc.) engaged in that month.
- **Maximum possible value: 14** (14 unique spending categories exist in the dataset).

---

## 2. Distribution (Customer-Level Yearly Average)

| Statistic | Value |
|---|---|
| Mean (monthly avg per customer) | 12.94 |
| Median (monthly avg per customer) | 13.92 |
| Min | 2.00 |
| Max | 14.00 |

**Distribution of Max Category Diversity Achieved (per customer, across 2025):**

| Max Diversity | Customers | % |
|---|---|---|
| 2 | 2 | 0.2% |
| 3 | 5 | 0.5% |
| 4 | 19 | 1.9% |
| 5 | 40 | 4.0% |
| 6 | 18 | 1.8% |
| 7 | 7 | 0.7% |
| 13 | 1 | 0.1% |
| **14 (maximum)** | **907** | **90.8%** |

> **90.8% of customers achieved all 14 spending categories at least once in 2025.** Category diversity at the maximum level is the norm, not the exception.

---

## 3. Relationship with Engagement

**Pearson Correlation (category_diversity_avg vs engagement_score): r = 0.938**

This is the **strongest single predictor of engagement score** in the entire dataset — stronger than frequency or recency.

**Average engagement by category diversity group:**

| Diversity Range | Avg Engagement Score | Customer-Months (n) | Std |
|---|---|---|---|
| 1–5 | 47.51 | 71 | 10.46 |
| 6–9 | 51.20 | 26 | 7.40 |
| 10–12 | 69.70 | 488 | 6.44 |
| 13–14 | 78.47 | 10,407 | 5.28 |

There is a clear monotonic increase: customers with higher category diversity consistently show higher engagement scores.

---

## 4. Interpretation (Causal Language Caution)

> The analysis shows that customers with higher category diversity **tend to have** significantly higher engagement scores (r = 0.938). This strong positive association suggests that broader spending behavior across more categories is closely linked to the engagement scoring methodology.

This does **not** imply that encouraging customers to spend in more categories will mechanically increase their engagement score. The relationship may reflect that both category diversity and engagement are jointly driven by underlying behavioral activity (e.g., active days, transaction count). See Phase 3.6 (Cross Analysis) for the multicollinearity context.

---

## 5. Key Findings

1. **Category diversity is the single strongest correlate of engagement** (r = 0.938), even stronger than active transaction days (r = 0.943 with engagement) and frequency.

2. **The dataset is concentrated at maximum diversity:** 90.8% of customers reached all 14 categories. This limits category diversity's usefulness as a customer differentiator within the "active" majority.

3. **Category diversity effectively separates disengaged customers:** The 9.0% of customers with Moderate or Low engagement are characterized by very low category diversity (mean ~4.7 categories for the High Health + Low Engagement group). This is a reliable behavioral marker.

---

## 6. Business Implications

- Customers who engage with only a narrow range of spending categories may be early indicators of disengagement.
- Monitoring whether a customer's category diversity is declining month-over-month could serve as an **early warning signal** for proactive engagement intervention.
- Product bundles or promotions encouraging spending across underused categories (e.g., travel, dining) could serve as non-punitive engagement nudges.

---

## 7. Recommended Charts
- **Fig 3.3a:** Histogram of max category diversity per customer.
- **Fig 3.3b:** Scatter plot of avg category diversity vs engagement score with trend line.
- **Fig 3.3c:** Bar chart of average engagement score by diversity group (1–5 / 6–9 / 10–12 / 13–14).

Charts saved at: `task3/TASK_3/05_CATEGORY/`
