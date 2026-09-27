# PHASE 8 — Cross-Analysis
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Methodology

After completing Tasks 3.1–3.5 individually, this phase identifies the relationships between all key metrics to construct a coherent behavioral story rather than five disconnected analyses.

---

## 2. Correlation Matrix (Key Engagement Metrics — Customer Level)

| | engagement | health | txn_count | recency | cat_diversity | online_ratio | active_days |
|---|---|---|---|---|---|---|---|
| engagement_score | 1.000 | 0.015 | 0.643 | -0.783 | 0.938 | -0.674 | 0.943 |
| financial_health_score | 0.015 | 1.000 | 0.021 | -0.003 | 0.036 | -0.083 | 0.054 |
| transaction_count_monthly_avg | 0.643 | 0.021 | 1.000 | -0.413 | 0.549 | -0.395 | 0.631 |
| recency_days | -0.783 | -0.003 | -0.413 | 1.000 | -0.845 | 0.764 | -0.838 |
| category_diversity_avg | 0.938 | 0.036 | 0.549 | -0.845 | 1.000 | -0.861 | 0.981 |
| online_spend_ratio_avg | -0.674 | -0.083 | -0.395 | 0.764 | -0.861 | 1.000 | -0.856 |
| active_days_avg | 0.943 | 0.054 | 0.631 | -0.838 | 0.981 | -0.856 | 1.000 |

---

## 3. Key Relationships Identified

### 3.1 — The Engagement Cluster (active_days + category_diversity + engagement)

**r(active_days, engagement) = 0.943**  
**r(category_diversity, engagement) = 0.938**  
**r(active_days, category_diversity) = 0.981**

These three variables form a tightly inter-correlated cluster. They likely reflect the same underlying behavioral phenomenon: **active customers transact on more days AND across more spending categories, and both behaviors are jointly captured by the engagement score.**

This is important: it means these are likely not independent drivers of engagement but rather different measurements of the same "behavioral activity" construct. When presenting to business stakeholders, they should be interpreted as complementary indicators, not competing explanations.

### 3.2 — Recency is the Critical Separator

**r(recency, category_diversity) = -0.845**  
**r(recency, active_days) = -0.838**  
**r(recency, engagement) = -0.783**

Recency has strong negative correlations with all activity indicators. Customers who stopped transacting earlier show lower category diversity, fewer active days, and lower engagement. Recency effectively identifies the disengaged minority (9.1% of customers with >0 recency days).

### 3.3 — Online Spend Ratio is Inversely Associated with Engagement

**r(online_spend_ratio, engagement) = -0.674**  
**r(online_spend_ratio, category_diversity) = -0.861**  
**r(online_spend_ratio, active_days) = -0.856**

Higher online spend ratio is associated with **lower** engagement, lower category diversity, and fewer active days. This counter-intuitive finding is explained by the behavioral profile of low-engagement customers: they make infrequent but digitally-concentrated transactions (e.g., occasional online payments). Their high online ratio reflects **low offline activity** rather than genuine digital adoption.

### 3.4 — Financial Health is Independent of Engagement

**r(financial_health, engagement) = 0.015**

Financial health score is essentially uncorrelated with engagement. This is a critical finding: **a customer can be highly engaged while financially stretched, or financially healthy while nearly dormant.** The two dimensions are genuinely orthogonal and must be analyzed separately.

---

## 4. Overall Behavioral Story

The data tells a clear story about what drives engagement at ITB:

> **Engagement is fundamentally driven by behavioral activity breadth and regularity — how many days per month a customer transacts (active_days) and how many categories they spend across (category_diversity). These two behaviors are essentially the same behavioral dimension and together explain ~90% of engagement score variance.**

> **Customers who become disengaged show a characteristic pattern: they stop transacting across multiple categories, their active days collapse, and their remaining limited transactions shift disproportionately to online/digital channels — likely occasional utility payments or subscriptions. This creates the counter-intuitive negative correlation between online_spend_ratio and engagement.**

> **Financial health is entirely separate from this engagement dynamic. ITB has financially healthy customers who are nearly dormant, and financially stretched customers who remain highly engaged. This justifies analyzing both dimensions independently and designing separate intervention strategies for each.**

---

## 5. Chart
- **Fig 3.6a:** Correlation heatmap of all key engagement metrics.
Charts saved at: `task3/TASK_3/08_CROSS_ANALYSIS/fig_3_6_correlation_matrix.png`
