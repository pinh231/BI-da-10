# Task 3 — Slide-Ready Content
## BI10 Round 01 | Customer Engagement Analysis

> All content in English. Numbers are exact figures from the analysis.

---

## Slide 1 — Customer Engagement: Overview

**Section Title:** Task 3 — Customer Engagement Analysis

**Objective:** Understand how ITB's 999 customers engage with its financial products, identify engagement drivers, and surface the highest-priority customer group for re-engagement.

**Key Message:**
> ITB maintains a predominantly engaged customer base (91% in High/Very High tier), but a distinct group of 25 financially healthy yet dormant customers represents the single most actionable re-engagement opportunity.

**Key KPIs:**
- 999 customers analyzed | 1,852,394 transactions | Jan–Dec 2025
- 91.0% of customers: High or Very High Engagement
- 9.0% of customers: Moderate or Low Engagement (90 customers)
- 25 customers: Financially Healthy + Low Engagement (Priority Group)

---

## Slide 2 — Engagement Score Distribution

**Chart:** Fig 3.1a + Fig 3.1b

**Key Findings:**
- Mean engagement score: **75.4** | Median: **78.2** | SD: **9.3**
- **66.9%** of customers: High Engagement (score 60–80)
- **24.1%** of customers: Very High Engagement (score ≥ 80)
- **8.0%** Moderate + **1.0%** Low = **90 customers require attention**

**Cutoff Explanation (for judges):**
> Segment boundaries (40 / 60 / 80) are pre-defined in the source dataset and verified to be consistent across all 10,992 monthly observations. They are adopted as-is, not arbitrarily applied.

**Business Takeaway:**
> The engagement distribution is healthy overall, but the 9% tail of disengaged customers represents a measurable gap in product retention.

---

## Slide 3 — Channel Adoption & Digital Spending

**Chart:** Fig 3.2a (adoption) + Fig 3.2c (spend share)

**Key Findings:**
- **100%** of customers use POS | **99.0%** use E-commerce | **98.1%** use Mobile App
- **92.6%** of customers use all 5 channels — multi-channel adoption is the norm
- Despite universal adoption: **POS still accounts for 58.8% of transactions**
- Digital channels (E-com + Mobile + Recurring): **21.3% of transactions**
- Average online spend ratio per customer: **24.7%** (median: 20.4%)

**Insight:**
> The engagement gap is NOT in channel availability — it is in digital usage frequency. Customers have access to all channels but default to offline (POS) for the majority of activity.

**Business Implication:**
> ITB should invest in digital habit-building (daily-use incentives, recurring payment setup nudges) rather than digital onboarding.

---

## Slide 4 — Category Diversity & Engagement

**Chart:** Fig 3.3b (scatter) + Fig 3.3c (bar by group)

**Key Finding:**
> Customers spending across more categories consistently show higher engagement scores — with a Pearson correlation of **r = 0.938**, category diversity is the single strongest engagement predictor in the dataset.

**Evidence:**
| Diversity Range | Avg Engagement |
|---|---|
| 1–5 categories | 47.5 |
| 6–9 categories | 51.2 |
| 10–12 categories | 69.7 |
| 13–14 categories | **78.5** |

**Insight:**
> 90.8% of customers use all 14 categories in at least one month. Customers who narrow their category breadth are showing an early disengagement signal.

**Business Implication:**
> Track month-over-month category diversity as an early warning monitoring metric. Design promotions in underused categories to maintain behavioral breadth.

---

## Slide 5 — Frequency & Recency

**Chart:** Fig 3.4c + Fig 3.4d

**Key Findings:**

| Metric | Overall Mean | HD Group Mean |
|---|---|---|
| Avg monthly transactions | 155.3 | 9.9 |
| Active days/month | 26.4 | 2.0 |
| Recency (days) | 16.9 | 232.0 |

- **Active days/month** (r = 0.943): the strongest behavioral engagement predictor.
- **Recency** (r = -0.783): customers inactive for 7+ months show drastically lower engagement.
- **90.9%** of customers transacted on or after Dec 31 — recency distinguishes the disengaged minority.

**Insight:**
> Engagement is built through daily habits. Customers who spread transactions across 26+ days/month (nearly every day) are the most engaged. Those transacting only 2 days/month are highly disengaged.

**Business Implication:**
> Design daily-use incentives (e.g., reward every calendar day of card use). Implement a 30-day inactivity alert system for proactive outreach.

---

## Slide 6 — Financially Healthy but Low-Engagement Segment

**Chart:** Fig 3.5a (scatter with highlight) + Fig 3.5b (quadrant matrix)

**The Segment:**
> Customers with Financial Health Score ≥ 70 AND Engagement Score < 70

**Cutoff Rationale:**
- Health ≥ 70: above-average health (mean = 66.3, SD = 4.7; ≥ 70 is ~0.8 SD above mean)
- Engagement < 70: below the P25 (74.8) and mean (75.4) — meaningfully low engagement

**Group Profile:**

| Metric | Target Group (n=25) | Portfolio Average |
|---|---|---|
| Group size | **25 customers (2.5%)** | — |
| Financial health score | **74.0** | 66.3 |
| Engagement score | **46.8** | 75.4 |
| Monthly transactions | **9.9** | 155.3 |
| Recency (days) | **232** | 16.9 |
| Category diversity | **4.68** | 12.94 |
| Online spend ratio | **60.6%** | 24.7% |

**Insight:**
> These 25 customers are ITB's most financially stable segment — yet they have been effectively dormant since approximately May 2025. They represent an engagement opportunity, NOT a financial risk.

**Recommended Actions (Non-Punitive):**
1. Personalized re-engagement offer via mobile app (they respond to digital channels)
2. Category-breadth vouchers to rebuild spending variety
3. Premium card upgrade or credit limit review (financially qualified)
4. Recurring payment setup incentive to establish a sustainable engagement habit

---

## Slide 7 — Task 3 Key Takeaways

**5 Strongest Findings:**

1. **91% engaged, but behavioral quality varies sharply within tiers**
   > Engagement score differentiation is most meaningful within the High tier (60–80). Customers near the lower boundary require monitoring.

2. **Channel adoption is universal; digital usage depth is the gap**
   > 99% adoption of E-commerce, but only 21% of transactions are digital. The opportunity is habit intensity, not channel introduction.

3. **Category diversity (r = 0.938) is the best leading indicator of engagement**
   > Narrowing spending breadth is the earliest observable behavioral signal of approaching disengagement.

4. **Active transaction days (r = 0.943) define the engaged customer**
   > 26+ active days/month = highly engaged. 2 active days/month = severely disengaged. Regularity beats volume.

5. **25 financially healthy, dormant customers = the highest-value re-engagement target**
   > Health score 74.0 (above average), engagement score 46.8, inactive 7+ months. Creditworthy, recoverable, and likely to respond to personalized digital outreach.

**Strategic Priorities:**
- Monitor: category diversity decline month-over-month as early warning
- Intervene: 30-day inactivity trigger for proactive re-engagement
- Build: daily-use habit campaigns to increase active transaction days
- Target: 25 high-health dormant customers with personalized premium offers
