# Task 3 — Customer Engagement Analysis
## BI10 Round 01 | ITB Consumer Finance Company | Final Report

> **Dataset:** 999 customers | 1,852,394 transactions | January–December 2025
> **Analysis Level:** Customer-level (yearly aggregates from 10,992 customer-month records)

---

## 3.1 Engagement Score Distribution

### Analytical Objective
Understand how customer engagement is distributed across ITB's 999-customer base and identify the proportion of customers in each engagement tier.

### Methodology
Engagement scores are computed monthly by the source system and stored in `engagement_score` (df_month). For customer-level analysis, the yearly average `engagement_score` per customer is used. Segment boundaries are adopted directly from the dataset's pre-defined `engagement_segment` field, verified to correspond to the thresholds: **< 40 (Low)**, **40–60 (Moderate)**, **60–80 (High)**, **≥ 80 (Very High)**.

### Key Statistics
| Statistic | Value |
|---|---|
| Total customers analyzed | 999 |
| Mean engagement score (yearly avg) | 75.40 |
| Median engagement score | 78.17 |
| Standard deviation | 9.31 |
| Score range | ~9.7 – ~99.6 |

### Engagement Segment Distribution
| Segment | Customers (n) | Percentage |
|---|---|---|
| Very High Engagement (≥ 80) | 241 | 24.1% |
| High Engagement (60–79.9) | 668 | 66.9% |
| Moderate Engagement (40–59.9) | 80 | 8.0% |
| Low Engagement (< 40) | 10 | 1.0% |

### Key Insight
**91.0% of ITB's customers fall into the High or Very High Engagement tier**, indicating a strongly engaged customer base overall. However, **90 customers (9.0%) are in the Moderate or Low tier**, and this minority shows extreme behavioral differences from the majority. The Low Engagement customers (n=10) have scores as low as ~9.7, representing near-total disengagement that warrants priority intervention.

### Business Implication
While the overall engagement picture is positive, the risk lies in customers near the lower boundary of the High tier (scores 60–65) who could slip into Moderate Engagement. ITB should monitor month-over-month score trends rather than treating the current snapshot as permanent. The 90 disengaged customers represent a high-value re-engagement opportunity.

**Recommended Chart:** Fig 3.1a (histogram with segment cutoff lines) + Fig 3.1b (horizontal bar chart of segment counts).

---

## 3.2 Channel Adoption & Digital Spending

### Methodology
Channel adoption is measured as the **percentage of unique customers** who used each channel at least once in 2025 (from df_trans). Transaction share and spending share are computed separately. Digital spend is measured using the pre-computed `online_spend_ratio` field in df_month (online_spend_vnd / total_spend_vnd). Digital channels are defined as: E-commerce, Mobile App, and Recurring Payment — all channels where `online_transaction_flag = 1`.

### Customer Channel Adoption (% of 999 Customers)
| Channel | Type | Adoption Rate |
|---|---|---|
| POS | Offline | 100.0% |
| E-commerce | Digital | 99.0% |
| Mobile App | Digital | 98.1% |
| QR Payment | Offline | 97.6% |
| Recurring Payment | Digital | 94.3% |

### Channel Transaction & Spend Share
| Channel | Transaction Share | Spending Share |
|---|---|---|
| POS | 58.8% | 58.5% |
| QR Payment | 19.9% | 19.6% |
| E-commerce | 8.7% | 9.6% |
| Mobile App | 7.7% | 7.6% |
| Recurring Payment | 4.9% | 4.6% |

### Digital Spending Behavior
- Customers allocate an average of **24.7% of their spending to online/digital channels** (median: 20.4%).
- 92.6% of customers use all 5 channels — multi-channel behavior is the norm.

### Key Insight
**Near-universal channel adoption means ITB has successfully introduced all channels to virtually its entire customer base. However, transaction volume remains heavily concentrated in offline channels (POS: 58.8%, QR: 19.9%).** Digital channels collectively represent 21.3% of transactions and ~21.8% of spending. The meaningful engagement opportunity is not onboarding customers to new channels — it is **increasing the frequency and regularity of digital channel usage** among already-adopted customers.

### Business Implication
Since almost all customers already have access to digital channels, conversion campaigns are not the right lever. ITB should focus on **habit-building interventions** within existing channels: e.g., incentivizing recurring digital payments (Direct Debit for utilities/subscriptions), push notifications for mobile app usage, and cashback rewards for digital-channel transactions.

**Recommended Charts:** Fig 3.2a (adoption), Fig 3.2b (transaction share), Fig 3.2c (spend share), Fig 3.2d (online spend ratio distribution).

---

## 3.3 Category Diversity & Engagement

### Methodology
`category_diversity` in df_month represents the number of unique spending categories (out of 14 total) a customer used in a given month. The correlation between yearly average category diversity and yearly average engagement score is computed at the customer level (n=999).

This metric measures **spending breadth**, not transaction volume or merchant count.

### Descriptive Statistics
| Statistic | Value |
|---|---|
| Mean (monthly avg per customer) | 12.94 categories |
| Median | 13.92 categories |
| Maximum possible | 14 categories |
| Customers achieving all 14 categories at least once | 907 (90.8%) |

### Relationship with Engagement
**Pearson correlation: r = 0.938** — the strongest single correlate of engagement in the dataset.

| Diversity Range | Avg Engagement Score | n (customer-months) |
|---|---|---|
| 1–5 categories | 47.51 | 71 |
| 6–9 categories | 51.20 | 26 |
| 10–12 categories | 69.70 | 488 |
| 13–14 categories | 78.47 | 10,407 |

### Key Insight
**Customers with higher category diversity consistently show significantly higher engagement scores (r = 0.938).** The relationship is monotonic and strong: customers spending across 13–14 categories average an engagement score of 78.5, while those spending across only 1–5 categories average 47.5 — a difference of 31 points. Category diversity is both the strongest predictor of engagement and a reliable behavioral indicator of disengagement when it declines.

> Note: This association does not establish causality. Category diversity and engagement may both reflect the same underlying behavioral activity dimension. See Section 3.6 for the cross-analysis context.

### Business Implication
Declining category diversity over consecutive months could serve as an **early warning indicator** for emerging disengagement. ITB should track month-over-month changes in `category_diversity` as a behavioral monitoring metric. Targeted promotions in underused spending categories (e.g., travel, dining) may help maintain or restore behavioral breadth.

**Recommended Charts:** Fig 3.3b (scatter plot with trend line), Fig 3.3c (bar chart by diversity group).

---

## 3.4 Transaction Frequency & Recency

### Definitions
- **Frequency:** Average number of transactions per month per customer (from df_month `transaction_count`).
- **Recency:** Days since the customer's last transaction to December 31, 2025 (computed from df_trans; reference date = 2025-12-31, the final day of the observation period).

Lower recency = more recent activity = higher engagement.

### Frequency Statistics
| Statistic | Value |
|---|---|
| Mean monthly transactions | 155.3 |
| Median monthly transactions | 122.6 |
| Min | 3.5 |
| Max | 366.0 |
| Correlation with engagement | r = 0.643 |

### Recency Statistics
| Statistic | Value |
|---|---|
| Customers who transacted on Dec 31, 2025 | 909 (90.9%) |
| Mean recency (full customer base) | 16.9 days |
| Median recency | -1 (= transacted Dec 31) |
| Max recency | 361 days |
| Correlation with engagement | r = -0.783 |

### Active Days (Supplementary)
- Average active transaction days per month: **26.4 days**.
- Correlation with engagement: **r = 0.943** — the strongest behavioral predictor.

### Key Insight
**Recency is a strong negative predictor of engagement (r = -0.783): customers who stopped transacting earlier show substantially lower engagement scores.** The vast majority of customers (90.9%) remain active through year-end, making recency most useful for identifying the disengaged minority. The High Health + Low Engagement group has a mean recency of 232 days — they effectively stopped engaging in May 2025.

**Active transaction days per month is the strongest engagement driver (r = 0.943):** Behavioral regularity — spreading transactions across many days per month — is more strongly associated with engagement than raw transaction count. This suggests that daily-use habits (e.g., using the card for routine purchases) are more valuable than occasional high-volume transactions.

### Business Implication
- **Recency monitoring:** Implement a 30-day inactivity alert trigger for proactive re-engagement outreach.
- **Frequency incentives:** Design daily-use campaigns (small cashback per day of card use) to increase `active_transaction_days` rather than total transaction count.
- **Do not** treat high recency as a churn indicator without a validated churn model.

**Recommended Charts:** Fig 3.4a–d (distribution and scatter plots for frequency and recency).

---

## 3.5 Financially Healthy but Low-Engagement Customers

### Analytical Framework
A Health × Engagement matrix is constructed at the customer level to identify the quadrant of customers who are financially stable but behaviorally disengaged.

### Cutoff Selection
| Dimension | Cutoff | Rationale |
|---|---|---|
| Financial Health | ≥ 70 | ~0.8 SD above mean (66.3); clearly above-average health |
| Engagement Score | < 70 | Below overall mean (75.4) and P25 (74.8); meaningfully low engagement |

Sensitivity analysis confirmed that Health ≥ 70 + Engagement < 70 produces a stable group of 25 customers. Stricter (Health ≥ 75) yields too few (9) for profiling; looser (Health ≥ 65) dilutes the "healthy" definition.

### Group Size
| Metric | Value |
|---|---|
| High-health + low-engagement customers | **25** |
| As % of total customer base (999) | **2.5%** |

### Health × Engagement Quadrant Breakdown
| Quadrant | Customers | % |
|---|---|---|
| High Health + High Engagement | ~246 | ~24.6% |
| **High Health + Low Engagement (Target Group)** | **25** | **2.5%** |
| Low Health + High Engagement | ~728 | ~72.9% |
| Low Health + Low Engagement | ~0 | ~0% |

### Behavioral Profile of the Target Group (vs. All Others)
| Metric | Target Group (n=25) | All Others (n=974) |
|---|---|---|
| Engagement Score | **46.83** | 76.14 |
| Financial Health Score | **74.03** | 66.10 |
| Avg Monthly Transactions | **9.9** | 159.1 |
| Recency (days since last txn) | **232.0** | 11.3 |
| Category Diversity (avg) | **4.68** | 13.15 |
| Online Spend Ratio | **0.606** | 0.238 |
| Active Days per Month | **2.00** | 27.04 |

### Key Insight
**These 25 customers (2.5% of the base) are financially the healthiest in the portfolio but among the least behaviorally active.** They make fewer than 10 transactions per month (vs. ~159 average), transact on only 2 active days per month (vs. 27), have not transacted for approximately 7–8 months before year-end (mean recency 232 days), and engage with fewer than 5 spending categories (vs. 13+). Their limited remaining activity is disproportionately digital (60.6% online ratio), suggesting they use the card only for occasional online or automated payments.

> **These customers are described as "low engagement" — NOT "churned" or "at risk of default."** They are financially stable and represent a dormant engagement opportunity.

### Business Implication
This group represents ITB's **highest-value re-engagement opportunity**: customers who are creditworthy, financially stable, and therefore receptive to premium product offers — but who have drifted away from active use. Recommended non-punitive interventions:
1. **Re-engagement campaign:** Personalized "welcome back" offers with cashback incentives for first transaction after 30 days of inactivity.
2. **Digital activation:** Since they respond to digital channels, engage via mobile app push notifications with category-specific vouchers.
3. **Breadth incentives:** Reward spending across multiple categories to rebuild behavioral diversity.
4. **Premium product introduction:** Given their financial health, this is an appropriate group for credit limit increase offers or premium card upgrades.

**Recommended Charts:** Fig 3.5a (scatter plot with highlighted group), Fig 3.5b (2×2 quadrant matrix).

---

## 3.6 Overall Task 3 Insights

### Insight 1 — Engagement is Driven by Behavioral Regularity, Not Volume
**Finding:** Active transaction days per month (r = 0.943) and category diversity (r = 0.938) are the strongest predictors of engagement — stronger than total transaction count (r = 0.643).  
**Evidence:** Customers averaging 26+ active days per month have engagement scores in the 78–80 range, while those averaging 2 active days score around 47.  
**Interpretation:** Engagement is built through daily habits and behavioral breadth, not occasional large purchases.  
**Business Implication:** ITB should design daily-use incentives (routine spending rewards) and category-breadth promotions rather than focusing solely on transaction volume.

### Insight 2 — Channel Adoption is Nearly Universal; the Gap is in Digital Usage Intensity
**Finding:** 94–100% of customers have adopted all 5 channels, yet POS still dominates at 58.8% of transactions.  
**Evidence:** Digital channels collectively account for only 21.3% of transactions despite 98–99% adoption of E-commerce and Mobile App.  
**Interpretation:** The barrier is not awareness or access — it is habit and frequency of digital channel use.  
**Business Implication:** ITB should invest in digital-habit building campaigns rather than digital onboarding campaigns.

### Insight 3 — Category Diversity is a Leading Behavioral Indicator of Disengagement
**Finding:** Category diversity (r = 0.938 with engagement) is the single strongest engagement predictor.  
**Evidence:** Customers scoring in Moderate or Low Engagement average only 4.68 categories per month vs. 13.15 for the rest.  
**Interpretation:** Narrowing category diversity is an early behavioral signal that a customer is retreating to essential-only spending — a precursor to disengagement.  
**Business Implication:** Month-over-month category diversity tracking should be implemented as an early warning monitoring metric.

### Insight 4 — Financial Health and Engagement are Independent (r = 0.015)
**Finding:** Financial health score and engagement score are essentially uncorrelated.  
**Evidence:** The High Health + Low Engagement group (n=25) has a mean health score of 74.0 — well above the overall mean — while scoring only 46.8 on engagement.  
**Interpretation:** A customer can be financially responsible while being behaviorally dormant. These dimensions require completely separate analytical and strategic treatment.  
**Business Implication:** ITB must not conflate financial health monitoring with engagement monitoring. Low engagement customers with high health are opportunities, not risks.

### Insight 5 — 25 High-Health Low-Engagement Customers Represent the Priority Re-Engagement Opportunity
**Finding:** 25 customers (2.5%) are financially healthy (health ≥ 70) but severely disengaged (engagement < 70, mean = 46.8), with a mean recency of 232 days.  
**Evidence:** These customers average only 9.9 transactions/month, 2 active days/month, and 4.68 categories — all dramatically below the portfolio average.  
**Interpretation:** These are dormant but creditworthy customers who have stopped using ITB as their primary financial product while maintaining good financial standing.  
**Business Implication:** This is the single most actionable segment from Task 3 — targeted re-engagement with personalized offers represents both high probability of success (financially stable customers) and significant revenue recovery potential.
