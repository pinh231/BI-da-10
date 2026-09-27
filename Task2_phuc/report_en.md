# BI10 Task 2 — Competition report

## Detect pressure when it happens, then offer support that matches its scale.

The annual mean health score is 66.37, but December’s mean is 54.25 and 772 of 918 observed customers (84.10%) score below 60. A small stressed segment alone does not describe the full support opportunity.

Among 909 customers observed in both November and December, average health falls by 13.35 points. Transaction frequency increases 95.82% on a geometric-mean basis, while average ticket size increases only 0.11% and income increases 0.44%. Category mix remains broadly stable.

Use a broad, low-cost budgeting response for customers with observed spending pressure, with more focused support for the stressed group. Engagement determines a potential route for delivery; it must not determine who deserves support.

## One source of truth; three explicitly different denominators.

Primary population: 10,992 customer-month observations, 999 distinct customers and 12 calendar months in 2025. Transaction checks cover all 1,852,394 source transactions. The original data are retained without deletion, imputation or outlier winsorization.

Annual prevalence uses customer-months. Annual reach uses unique customers who ever qualify. Current support reach uses only the 918 customers observed in December. Time comparisons use 909 matched November–December customers; a separate 908-customer panel observed in all 12 months confirms the direction.

908 customers have 12 months, 86 have one month and five have two months. Missing months are not zero-spend months. The optional next-month label has 999 missing values at each customer’s last observation; these rows remain in the descriptive analysis.

Official scope retained: score distribution; factors associated with low health; occupation, age and province differences; a reproducible stressed/high-engagement rule. The team’s earlier workload allocation does not limit the analysis. This remains the financial-health task, with evidence handed to segmentation and recommendations.

## Stable annual averages conceal periods of low health.

Mean 66.3660; median 67.7000; sample standard deviation 9.4760 (ddof=1). Quartiles: 60.7 and 73.2. Range: 0.8–90.2. Giving each customer equal weight instead produces a mean of 66.3028.

Stable [60,80): 7,965 / 10,992 (72.46%). Monitoring [40,60): 2,457 (22.35%). Healthy [80,100]: 475 (4.32%). Stressed [0,40): 95 (0.86%). The combined share below 60 is 23.22%.

70 of 999 customers (7.01%) experience at least one stressed month. No customer has a full-observed-period average below 40; using that average to identify stressed customers would miss all 70. “Ever stressed” is not “currently stressed” or “persistently stressed”.

## The December deterioration survives a like-for-like customer comparison.

In the 909-customer matched sample, mean health changes from 67.52 to 54.16: -13.35 points (customer bootstrap 95% interval -13.92 to -12.74; 3,000 resamples). Median change is −13.70; 840 / 909 customers (92.41%) decline.

Below-60 prevalence rises from 139 / 909 (15.29%) to 769 / 909 (84.60%), an increase of 69.31 percentage points. Of 770 previously stable or healthy customers, 642 (83.38%) fall below 60. These are the matched-sample results, distinct from the full December snapshot.

The complete 908-customer panel shows a -13.41-point mean change. The result is not explained solely by new or disappearing customers. One synthetic year cannot establish recurring seasonality or identify why the data generator produced this pattern.

## More transactions, rather than larger tickets, account for the pressure increase.

For each matched customer, spend / income = transaction count × exact average ticket / income. The December / November geometric-mean multipliers are 1.9582× for count, 1.0011× for ticket, 1.0044× for income and 1.9518× for spend/income. Multiplicative changes are decomposed with logarithms, without a residual.

Mean log contributions are +0.67204 from frequency, +0.00114 from ticket size and −0.00444 from income. Frequency contributes 100.49% of the net log increase; the value exceeds 100% because the small income increase offsets part of the pressure. This is an accounting identity, not a causal attribution to customer intent.

In the transaction-level attribution, the mean of individual spending increases is +105.56%. This arithmetic average differs from the +96.05% geometric average by design. For each category we divide its spending change by that customer’s November total; the category contributions sum exactly to +105.56 percentage points.

All 14 categories contribute positively. In-store groceries contributes the most (+15.83 points), but represents only 15.00% of total mean growth. The largest absolute category-share movement is just 0.53 percentage points. This supports a broad frequency increase, not a demonstrated shift toward one discretionary category.

## Spending relative to income remains the strongest pooled association.

An exploratory screen covers 13 contemporaneous numeric indicators: the four main ratios, engagement, online share, transaction count, active days, category diversity, recency, age and opening/ending balance normalized by income. Spend/income and utilization remain the strongest pooled Pearson associations. Future labels, health-band labels, identifiers and raw financial VND magnitudes are excluded; discretionary share is omitted because it equals one minus essential share.

Pooled Pearson correlations with health: spend/income −0.898; utilization −0.862; volatility −0.496; essential share +0.481. Spearman gives the same direction. Spend/income remains −0.902 when December is excluded and −0.850 after removing both customer and month averages in the balanced panel.

Essential share is positively associated with health at the monthly grain, but its correlation across customer averages is only +0.079. A monthly composition signal is not a stable customer trait. Volatility shows the same distinction: pooled −0.496 versus customer-average −0.125.

A sensitivity analysis removes the outer 1% of each predictor separately; no sign changes occur. The primary analysis retains all observations. Two-way demeaning controls additive customer and month differences; it does not eliminate every confounder.

Spend/income and utilization share spending in their numerators. Their conditional-model VIFs are about 10.8 and 10.7, so coefficients cannot reliably separate independent effects. The in-sample explanatory R² of 0.849 is not a predictive accuracy claim. The score-generation formula is not supplied; some association may be built into the derived score.

## Demographics explain where to investigate, not whom to penalize.

Age: pooled means range from 65.79 (25–34, 177 customers) to 66.92 (55+, 390 customers), a 1.13-point gap. The lowest group changes to under-25s when each customer receives equal weight. The effect is small relative to the temporal deterioration.

Province: Ha Tinh averages 60.43 (12 customers), versus Hanoi 68.04 (80), a 7.61-point gap. The same extremes persist with equal-customer weighting. Rankings remain unadjusted for customer composition, and small provincial samples limit generalization.

Occupation: 396 labels for 999 customers; 128 occupations have only one customer and none exceeds ten. The extremes are film-set designer, 49.80 (one customer), and marketing director, 77.72 (three). Report these because the task requests them; do not treat them as occupational population estimates.

The complete tables include pooled means, equal-customer means, full-panel means, customer counts and bootstrap intervals. The demographic bootstrap intervals estimate the equal-customer mean, not the pooled customer-month mean. A one-customer group has no reported bootstrap interval. Demographics are excluded from the proposed support-eligibility rules.

## Use an interpretable strict rule, and show the sensitivity rather than hide it.

Primary crossover definition: financial_health_score <40 AND engagement_score ≥80 in the same customer-month. The health threshold matches the stressed band; the engagement threshold matches the supplied “very high engagement” band. This stricter definition replaces the previous team-example threshold of 70, not the underlying data.

The rule identifies 52 / 10,992 observations (0.4731%), 45 / 999 ever-qualifying customers (4.5045%), and eight / 918 December customers (0.8715%). Six of the 45 qualify in two or more months. All 52 observations have spending above income.

At health <40, engagement ≥60 identifies 93 observations / 69 customers; ≥70 identifies 81 / 64; ≥80 identifies 52 / 45. December counts are 25, 25 and eight respectively. A stricter reach estimate is not inherently better: ≥80 gives a clear segment definition, while support is still available to every stressed customer.

Very high engagement occurs in 54.74% of stressed observations versus 34.79% of all observations. At the ≥70 threshold, the comparison reverses (85.26% versus 91.44%). Therefore “stressed customers are more engaged” is not threshold-independent. Engagement describes recorded transactions, not marketing consent or verified contactability.

## Match the support model to a 681-customer December pressure cohort.

Tier 1 — 25 stressed customers (2.72% of December): offer a voluntary budget review and tailored reminders; eight have very high engagement. This group may warrant more intensive support because its observed health is below 40, not because of demographic membership.

Tier 2 — 656 monitoring customers whose spending exceeds income (71.46%): provide scalable, opt-in budgeting and cumulative-spend alerts. 298 have very high engagement. At this scale, a mass service workflow is more plausible than an individually staffed intervention for every customer.

Tier 3 — 91 monitoring customers without spend above income (9.91%): provide light-touch education or planning support, avoiding inaccurate “you overspent your income” messages. Tier 4 — 146 stable/healthy customers (15.90%): retain general self-service tools. The four groups are disjoint and cover all 918 observed customers.

Tier 1 + Tier 2 reaches 681 distinct customers (74.18% of the December snapshot), including 306 with very high engagement. This is observed eligibility, not predicted conversion, validated intervention effectiveness, or confirmed delivery capacity.

Channel evidence: POS averages 62.96% of spend for Tier 1 and 59.24% for Tier 2 (equal-customer average). High engagement does not establish an app-first customer journey. App-only outreach should not be assumed; contact permissions and usable delivery channels are absent from the dataset.

## Propose measurable validation, without inventing a business lift.

Proposed pilot, not a result: at the next observable cycle, identify customers using only information available by that date, record consent/contactability, and randomize eligible customers between a support invitation and existing service. Randomize by customer, stratifying by support tier; keep access to standard support unchanged.

Primary outcome proposal: the next-month share spending above income, evaluated by original randomized assignment. Secondary outcomes: spend/income, health-score change, tool activation and opt-out/complaint rate. Report follow-up coverage and missing outcomes by arm; do not silently drop customers who disappear.

Reach is measured here; effect size, ROI, saved VND and channel response are not. A power calculation requires a justified minimum worthwhile effect, usable cohort size and follow-up assumptions; those are not supplied. January 2026 outcomes are absent, so the December intervention cannot be backtested as effective.

If monthly aggregate files are the only available feed, run support after the month closes. In-month early warnings require live transaction totals and an income estimate available at that time, followed by separate validation. Do not claim a real-time capability from a year-end CSV.

The score is a wellbeing indicator. Never use it to approve or deny credit, cut credit limits or block accounts. No proposed support rule uses occupation, age or province to exclude customers.

## What is verified, and what remains uncertain.

Verified: 16 core checks and 15 extension checks pass, including source fingerprint consistency, exact per-customer log decomposition, paired transition totals, complete December tier coverage and reconciliation of transaction categories to monthly spend. Key headline calculations are independently recomputed with Python’s standard library.

The paired comparison resamples customers, not individual months, 3,000 times with seed 20260928. Category and demographic intervals use 1,000 customer resamples. These quantify resampling stability in the synthetic sample; they do not certify population estimates or correct for exploratory multiple comparisons.

The case notes that source simulation dates were folded into a single 2025 year. Transaction-density and calendar artifacts may explain the observed pattern. Treat the December result as a diagnostic and an intervention hypothesis, not a forecast of every future December.

Main data limitation: synthetic income/credit magnitudes, unknown score-generation formula, one year, incomplete customer coverage and tiny occupation samples. Credit utilization here is spend/credit limit capped at 1.5. Spending volatility is supplied as a coefficient of variation without a fully documented aggregation window.

Source documents: BI10_ROUND01.pdf (Task 2, PDF page 9), supplied case-study file and data_dictionary.xlsx. Official presentation language is English. All required Task 2 elements are covered; extra temporal and transaction analysis strengthens the evidence rather than replaces them.

## Recommended presentation narrative: six evidence-led pages.

1. The annual average hides a December deterioration. Show distribution plus the monthly below-60 chart. State the customer-month denominator.

2. The deterioration occurs within the same customers. Show the paired transition matrix and −13.35-point change with the bootstrap interval.

3. The pressure is frequency-led and broad-based. Show geometric multipliers and category attribution. State arithmetic versus geometric definitions.

4. Behavioral associations are robust; demographic stories are weaker. Show the correlation robustness and compact age/province/occupation panels with n.

5. Define stressed and very highly engaged transparently. Show 52 observations, 45 ever-customers, eight December customers and sensitivity to 60/70/80.

6. Turn the finding into a support design. Show the 25/656/91/146 tiers, measured reach and proposed experiment. Do not claim proven lift. Six pages are a recommendation for this section; the team should allocate them within the full-deck limit.