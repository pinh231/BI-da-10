# PHASE 4 — Channel Adoption & Digital Spending
## BI10 Round 01 | Task 3: Customer Engagement Analysis

---

## 1. Channel Definitions (Verified from Data)

Five transaction channels exist in the dataset. Their online/offline nature is consistent and unambiguous:

| Channel | Type | online_transaction_flag |
|---|---|---|
| POS | Offline | Always 0 |
| QR Payment | Offline | Always 0 |
| E-commerce | Online / Digital | Always 1 |
| Mobile App | Online / Digital | Always 1 |
| Recurring Payment | Online / Digital | Always 1 |

**Digital channel definition:** E-commerce + Mobile App + Recurring Payment (all map to `online_transaction_flag = 1`).

**Important distinctions:**
- **Customer Adoption Rate:** % of unique customers who used a channel at least once in 2025.
- **Transaction Share:** % of total transactions attributed to the channel.
- **Spending Share:** % of total VND spent through the channel.

These three metrics measure different things and may differ significantly.

---

## 2. Customer Channel Adoption

| Channel | Customers Using | Adoption Rate |
|---|---|---|
| POS | 999 / 999 | 100.0% |
| E-commerce | 989 / 999 | 99.0% |
| Mobile App | 980 / 999 | 98.1% |
| QR Payment | 975 / 999 | 97.6% |
| Recurring Payment | 942 / 999 | 94.3% |

**Key finding:** Adoption rates are remarkably high across all channels. Even the least-used channel (Recurring Payment) is adopted by 94.3% of customers. This indicates **near-universal multi-channel behavior** in this customer base.

**Multi-channel breadth:**
- 925 customers (92.6%) use all 5 channels.
- 41 customers (4.1%) use 4 channels.
- 30 customers (3.0%) use 3 channels.
- 3 customers (0.3%) use only 2 channels.

---

## 3. Transaction Share by Channel

| Channel | Transactions | Transaction Share |
|---|---|---|
| POS | 1,089,518 | 58.8% |
| QR Payment | 367,682 | 19.9% |
| E-commerce | 161,670 | 8.7% |
| Mobile App | 142,399 | 7.7% |
| Recurring Payment | 91,125 | 4.9% |
| **Total** | **1,852,394** | **100%** |

Despite near-universal adoption, **POS dominates transaction volume** (58.8%). Digital channels collectively account for 21.3% of transactions.

---

## 4. Spending Share by Channel

| Channel | Spending Share |
|---|---|
| POS | 58.5% |
| QR Payment | 19.6% |
| E-commerce | 9.6% |
| Mobile App | 7.6% |
| Recurring Payment | 4.6% |

Spending shares mirror transaction shares closely, indicating similar average transaction values across channels.

---

## 5. Online/Digital Spending Behavior

**Online spend ratio** = `online_spend_vnd / total_spend_vnd` (pre-computed in df_month).

| Metric | Value |
|---|---|
| Customer-level yearly average: Mean | 24.7% |
| Customer-level yearly average: Median | 20.4% |
| Standard deviation | 14.6% |

The distribution is **right-skewed**: most customers have a relatively modest online spend ratio (~20%), with a minority of digitally-intensive customers pushing the mean higher.

---

## 6. Key Findings

1. **Near-universal multi-channel adoption:** Almost all customers use all 5 channels, meaning channel adoption rate alone is not a useful differentiator. The meaningful question is *how much* customers use each channel, not whether they do.

2. **POS remains dominant despite digital availability:** 58.8% of transactions and 58.5% of spending still flow through POS. QR Payment is the second-largest channel at 19.9%.

3. **Digital channels account for 21.3% of transactions and approximately 21.8% of spending:** E-commerce, Mobile App, and Recurring Payment collectively represent a meaningful but minority share of activity.

4. **Online spend ratio averages ~20–25%:** The typical customer allocates approximately one-quarter of their spending to online/digital channels.

---

## 7. Business Implications for ITB

- Since almost all customers already adopt all channels, ITB should focus on **increasing digital transaction frequency** rather than onboarding customers to new channels.
- The high POS dependency suggests that **in-store experience and card-present transactions** remain the core engagement driver.
- Recurring Payment has the lowest adoption (94.3%) — this channel represents a structured engagement opportunity (utility payments, subscriptions) that could improve engagement predictability.

---

## 8. Recommended Charts
- **Fig 3.2a:** Customer adoption rate by channel (bar chart).
- **Fig 3.2b:** Transaction share by channel (bar chart).
- **Fig 3.2c:** Spending share by channel (bar chart).
- **Fig 3.2d:** Distribution of yearly average online spend ratio (histogram).

Charts saved at: `task3/TASK_3/04_CHANNEL/`
