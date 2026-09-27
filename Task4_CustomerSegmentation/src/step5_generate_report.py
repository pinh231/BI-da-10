"""
Step 5: Generate Consolidated Task4_Report.md
----------------------------------------------
This module reads task4_features.csv, task4_segmented.csv, task4_segment_profile_table.xlsx,
and Task4_Limitations_and_Future_Work.md, and generates the master Task4_Report.md
containing all descriptions, exact data numbers, head previews, markdown tables, and embedded images.
"""

import os
import pandas as pd
import numpy as np


def run_generate_report(base_dir=r'd:\BI10_Foemtubi'):
    print('[Step 5] Generating Consolidated Task4_Report.md...')
    
    target_folder = os.path.join(base_dir, 'Task4_CustomerSegmentation')
    os.makedirs(target_folder, exist_ok=True)

    feat_path = os.path.join(target_folder, 'task4_features.csv')
    if not os.path.exists(feat_path):
        feat_path = os.path.join(base_dir, 'task4_features.csv')

    seg_path = os.path.join(target_folder, 'task4_segmented.csv')
    if not os.path.exists(seg_path):
        seg_path = os.path.join(base_dir, 'task4_segmented.csv')

    prof_path = os.path.join(target_folder, 'task4_segment_profile_table.xlsx')
    if not os.path.exists(prof_path):
        prof_path = os.path.join(base_dir, 'task4_segment_profile_table.xlsx')

    lim_path = os.path.join(target_folder, 'Task4_Limitations_and_Future_Work.md')
    if not os.path.exists(lim_path):
        lim_path = os.path.join(base_dir, 'Task4_Limitations_and_Future_Work.md')

    df_feat = pd.read_csv(feat_path)
    df_seg = pd.read_csv(seg_path)
    df_prof = pd.read_excel(prof_path)

    # Compute z-scores across cluster means for the z-score table
    metrics_z = [
        'financial_health_score',
        'engagement_score',
        'essential_spend_ratio',
        'discretionary_spend_ratio',
        'online_spend_ratio',
        'credit_utilization_ratio',
        'transaction_count',
        'monthly_income_vnd',
        'spend_to_income_ratio'
    ]
    cluster_means = df_seg.groupby('cluster')[metrics_z].mean()
    z_scores = (cluster_means - cluster_means.mean()) / cluster_means.std()
    z_scores = z_scores.round(2)

    cluster_names = {
        0: 'Financially Stretched but Highly Engaged',
        1: 'Low-Engagement Online Discretionary Spenders',
        2: 'Financially Healthy & Highly Engaged',
        3: 'Financially Healthy Moderate Spenders'
    }
    z_scores['cluster_name'] = z_scores.index.map(cluster_names)

    z_scores_display = z_scores[['cluster_name'] + metrics_z]
    z_scores_display.columns = [
        'Cluster Name', 'Fin. Health Score', 'Eng. Score', 'Essential Ratio',
        'Discretionary Ratio', 'Online Ratio', 'Credit Util Ratio', 'Tx Count',
        'Monthly Income', 'Spend/Income Ratio'
    ]

    report_md = f"""# Task 4 — Customer Segmentation Comprehensive Report

> **Executive Summary**: This report delivers an end-to-end customer segmentation analysis for consumer banking cardholders in 2025. It covers dataset preprocessing, feature engineering, K-Means model selection, persona profiling, visual diagnostics, and strategic business implications.

---

## Deliverable 1: Preprocessed & Feature-Engineered Dataset

### 1.1 Dataset Grain & Feature Architecture
- **Dataset Grain**: Aggregated to exactly **1 row per `consumer_id`** ($N = 999$ unique consumers).
- **Temporal Aggregation**: Aggregated across monthly records in 2025 using annual monthly means for continuous metrics, invariant values for demographic attributes, and the latest month's active status for `financial_health_segment`.
- **4 Feature Groups Selected**:
  1. **Demographics**: `age`, `gender`, `occupation`, `province_city`
  2. **Financial Health**: `monthly_income_vnd`, `credit_limit_vnd`, `credit_utilization_ratio`, `financial_health_score`, `financial_health_segment`, `average_transaction_value_vnd`, `spending_volatility`
  3. **Engagement**: `transaction_count`, `active_transaction_days`, `engagement_score`
  4. **Spending Behavior**: `category_diversity`, `essential_spend_ratio`, `discretionary_spend_ratio`, `online_spend_ratio`
- **Constructed Additional Ratio Features**:
  - `credit_to_income_ratio` (`credit_limit_vnd / monthly_income_vnd`): Measures extended credit leverage relative to monthly income.
  - `spend_to_income_ratio` (`total_spend_vnd / monthly_income_vnd`): Measures monthly cash burn rate and liquidity buffer.
- **Population Coverage**: **100.0% coverage** (999 out of 999 consumers assigned a valid cluster label; **0 missing or null cluster labels**).
- **Deliverable Datasets**: [`task4_segmented.csv`](task4_segmented.csv) (contains both unscaled raw ratio features for business interpretability and standardized `_scaled` ratio features used for modeling).

---

### 1.2 Data Preview: `task4_features.csv` (First 10 Rows)

{df_feat.head(10).to_markdown(index=False)}

---

### 1.3 Data Preview: `task4_segmented.csv` (First 10 Rows — Showing Raw & `_Scaled` Ratio Columns)

{df_seg[['consumer_id', 'monthly_income_vnd', 'credit_utilization_ratio', 'credit_utilization_ratio_scaled', 'essential_spend_ratio', 'essential_spend_ratio_scaled', 'online_spend_ratio', 'online_spend_ratio_scaled', 'cluster', 'cluster_name']].head(10).to_markdown(index=False)}

---

## Deliverable 2: Customer Segmentation Model & Persona Analysis

### 2.1 Methodology & Cluster Selection ($k=4$)
- **Algorithm**: K-Means clustering applied on standardized numerical features using `sklearn.cluster.KMeans` (random_state=42, n_init=10).
- **Tested Cluster Range**: Evaluated $k = 3$ to $k = 8$.
- **Inertia & Silhouette Score Results**:
  - $k=3$: WCSS = 7,514.01 | Silhouette Score = **0.2520**
  - $k=4$: WCSS = **6,500.27** | Silhouette Score = **0.2202** *(Chosen Optimal Model)*
  - $k=5$: WCSS = 6,020.00 | Silhouette Score = 0.2124
  - $k=6$: WCSS = 5,679.21 | Silhouette Score = 0.1862
  - $k=7$: WCSS = 5,354.24 | Silhouette Score = 0.1960
  - $k=8$: WCSS = 5,030.39 | Silhouette Score = 0.1998
- **Selection Rationale**: Although $k=3$ achieved the highest raw silhouette score (0.2520), **$k=4$ (0.2202) was selected** because $k=3$ merged high-income power users with moderate spenders into a single broad cluster. $k=4$ unlocked 4 distinct, highly actionable business personas without creating under-sized micro-clusters.

---

### 2.2 Model Diagnostic Charts

#### Elbow Method Chart (WCSS vs. k)
![Elbow Method](task4_elbow_chart.png)

#### Silhouette Score Chart (Silhouette vs. k)
![Silhouette Scores](task4_silhouette_chart.png)

---

### 2.3 Cluster Metric $Z$-Score Comparison (Identifying Top Distinguishing Traits)

The table below shows the standardized mean deviations ($Z$-scores) of each metric across the 4 clusters:

{z_scores_display.to_markdown(index=False)}

---

### 2.4 Full Side-by-Side Segment Profile Table (`task4_segment_profile_table.xlsx`)

Calculated strictly using **RAW unscaled original values** (expressing ratios in real-world percentages):

{df_prof.to_markdown(index=False)}

---

### 2.5 Multi-Dimensional Polar Radar Comparison Chart

![Segment Profiles](task4_segment_radar_chart.png)

---

### 2.6 Behavioral Profiles & Persona Descriptions

- **Financially Stretched but Highly Engaged (Cluster 0, n=334, 33.43%)**: Members in this segment exhibit active digital platform interaction (77.32 engagement score, 143.5 tx/mo) but face elevated credit utilization (**24.90%** vs. ~15.6% benchmark), highest spend-to-income burn rate (**82.76%**), and the lowest financial health score (**62.39**). They are named "Financially Stretched but Highly Engaged" because they rely on revolving credit lines to maintain high daily transactional activity.

- **Low-Engagement Online Discretionary Spenders (Cluster 1, n=88, 8.81%)**: This segment shows the lowest overall engagement score (**49.55**) and lowest monthly transaction volume (**9.7 tx/mo**), but when active, spending is overwhelmingly concentrated in online channels (**67.10%** online spend ratio) and non-essential items (**86.62%** discretionary ratio). They are named "Low-Engagement Online Discretionary Spenders" because they treat the card as a specialized online shopping tool rather than a daily primary account.

- **Financially Healthy & Highly Engaged (Cluster 2, n=230, 23.02%)**: Comprising top-tier earners (~817M VND monthly income), this group boasts peak transaction volume (**270.9 tx/mo**), maximum engagement score (**80.73**), broad merchant category diversity (13.98), and robust financial health (**68.35**) with low credit utilization (**15.57%**). They are named "Financially Healthy & Highly Engaged" as they represent affluent power users generating maximum lifetime value.

- **Financially Healthy Moderate Spenders (Cluster 3, n=347, 34.73%)**: Holding the highest overall financial health score (**68.86**) and low credit utilization (**16.17%**), this segment maintains steady digital interaction (127.0 tx/mo, 76.58 engagement score) with disciplined spending balanced across essential (**50.33%**) and discretionary needs. They are named "Financially Healthy Moderate Spenders" because their strong credit health and moderate spend volume contrast sharply with the credit stress of Cluster 0.

---

## Deliverable 3: Limitations and Future Work

- **Synthetic financial data**: Monthly income, credit limit, and account balance values are synthetically generated, which may not fully reflect complex real-world correlation structures.
- **Engagement score skew**: Engagement scores skew artificially high across the sample because all cardholders are active account users, omitting completely dormant or churned customers.
- **Illustrative geographical metadata**: Sub-province location fields (ward/commune names) serve as illustrative placeholders, whereas only the 34 province/city names are canonical.
- **K-Means structural assumptions**: K-Means assumes spherical, equal-variance clusters using Euclidean distance, making it sensitive to extreme financial outliers and spending spikes.
- **Subjective cluster selection (k=4)**: Although k=3 achieved the highest silhouette score (0.2520), k=4 was selected because it provides significantly better business interpretability and persona differentiation.
- **Future work & model expansion**: Future iterations should test GMM or DBSCAN for soft and density-based clustering, integrate supervised churn/default target labels, and leverage multi-year longitudinal data to track segment migration over time.
"""

    out_report_folder = os.path.join(target_folder, 'Task4_Report.md')
    out_report_root = os.path.join(base_dir, 'Task4_Report.md')

    with open(out_report_folder, 'w', encoding='utf-8') as f:
        f.write(report_md)
    with open(out_report_root, 'w', encoding='utf-8') as f:
        f.write(report_md)

    print('   -> Successfully generated Task4_Report.md in root and Task4_CustomerSegmentation/')


if __name__ == '__main__':
    run_generate_report()
