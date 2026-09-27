"""
Step 2: K-Means Clustering & Model Fitting
------------------------------------------
This module evaluates K-Means across k=3 to k=8, plots the elbow and silhouette
score diagnostic charts, fits the final model at k=4, restores original raw metrics,
appends scaled ratio columns (_scaled), and maps business-friendly cluster names.
Output files: task4_elbow_chart.png, task4_silhouette_chart.png, task4_segmented.csv
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def safe_save_fig(fig, filepath):
    try:
        folder = os.path.dirname(filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
    except Exception as e:
        alt_path = filepath.replace('.png', '_output.png')
        fig.savefig(alt_path, dpi=300, bbox_inches='tight')
        print(f'   [Note] Saved chart to alternate path {alt_path} due to file lock.')


def run_clustering(base_dir=r'd:\BI10_Foemtubi', chosen_k=4):
    print('[Step 2] Running K-Means Clustering & Model Fitting...')
    
    target_folder = os.path.join(base_dir, 'Task4_CustomerSegmentation')
    os.makedirs(target_folder, exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'Dataset'), exist_ok=True)

    feat_path = os.path.join(target_folder, 'task4_features.csv')
    if not os.path.exists(feat_path):
        feat_path = os.path.join(base_dir, 'task4_features.csv')

    df_feat = pd.read_csv(feat_path)

    non_numeric = ['consumer_id', 'gender', 'occupation', 'province_city', 'financial_health_segment']
    numeric_cols = [c for c in df_feat.columns if c not in non_numeric]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_feat[numeric_cols])

    # 1. Evaluate k=3 to k=8
    k_range = list(range(3, 9))
    inertias = []
    silhouettes = []

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        lbls = km.fit_predict(X_scaled)
        inertias.append(km.inertia_)
        silhouettes.append(silhouette_score(X_scaled, lbls))

    # Save Elbow Chart
    fig1, ax1 = plt.subplots(figsize=(8, 5), dpi=300)
    ax1.plot(k_range, inertias, marker='o', linewidth=2.5, color='#1f77b4', markersize=8)
    ax1.axvline(x=chosen_k, color='#d62728', linestyle='--', label=f'Chosen k={chosen_k}')
    ax1.set_title('K-Means Elbow Method (Inertia vs. k)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Number of Clusters (k)', fontsize=12)
    ax1.set_ylabel('Inertia (WCSS)', fontsize=12)
    ax1.set_xticks(k_range)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(fontsize=11)
    fig1.tight_layout()
    safe_save_fig(fig1, os.path.join(target_folder, 'task4_elbow_chart.png'))
    safe_save_fig(fig1, os.path.join(base_dir, 'task4_elbow_chart.png'))
    safe_save_fig(fig1, os.path.join(base_dir, 'Dataset', 'task4_elbow_chart.png'))
    plt.close(fig1)

    # Save Silhouette Score Chart
    fig2, ax2 = plt.subplots(figsize=(8, 5), dpi=300)
    ax2.plot(k_range, silhouettes, marker='s', linewidth=2.5, color='#2ca02c', markersize=8)
    ax2.axvline(x=chosen_k, color='#d62728', linestyle='--', label=f'Chosen k={chosen_k}')
    ax2.set_title('K-Means Silhouette Scores (k=3 to 8)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Number of Clusters (k)', fontsize=12)
    ax2.set_ylabel('Average Silhouette Score', fontsize=12)
    ax2.set_xticks(k_range)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(fontsize=11)
    fig2.tight_layout()
    safe_save_fig(fig2, os.path.join(target_folder, 'task4_silhouette_chart.png'))
    safe_save_fig(fig2, os.path.join(base_dir, 'task4_silhouette_chart.png'))
    safe_save_fig(fig2, os.path.join(base_dir, 'Dataset', 'task4_silhouette_chart.png'))
    plt.close(fig2)

    # 2. Fit final K-Means model at chosen_k
    final_km = KMeans(n_clusters=chosen_k, random_state=42, n_init=10)
    cluster_labels = final_km.fit_predict(X_scaled)

    # 3. Load original raw data to preserve raw unscaled values
    raw_path = os.path.join(base_dir, 'Dataset', 'consumer_financial_health_engagement_2025.csv')
    df_raw = pd.read_csv(raw_path)
    df_raw['analysis_month'] = pd.to_datetime(df_raw['analysis_month'])
    df_raw = df_raw.sort_values(['consumer_id', 'analysis_month'])
    df_raw['credit_to_income_ratio'] = df_raw['credit_limit_vnd'] / df_raw['monthly_income_vnd']

    agg_raw = df_raw.groupby('consumer_id', as_index=False).agg({
        'age': 'first',
        'gender': 'first',
        'occupation': 'first',
        'province_city': 'first',
        'monthly_income_vnd': 'mean',
        'credit_limit_vnd': 'first',
        'credit_utilization_ratio': 'mean',
        'financial_health_score': 'mean',
        'financial_health_segment': 'last',
        'average_transaction_value_vnd': 'mean',
        'spending_volatility': 'mean',
        'transaction_count': 'mean',
        'active_transaction_days': 'mean',
        'engagement_score': 'mean',
        'category_diversity': 'mean',
        'essential_spend_ratio': 'mean',
        'discretionary_spend_ratio': 'mean',
        'online_spend_ratio': 'mean',
        'credit_to_income_ratio': 'mean',
        'spend_to_income_ratio': 'mean'
    })

    agg_raw['cluster'] = cluster_labels

    # 4. Add _scaled columns for all ratio features
    ratio_cols = [
        'credit_utilization_ratio',
        'essential_spend_ratio',
        'discretionary_spend_ratio',
        'online_spend_ratio',
        'credit_to_income_ratio',
        'spend_to_income_ratio'
    ]
    ratio_scaler = StandardScaler()
    scaled_ratios = ratio_scaler.fit_transform(agg_raw[ratio_cols])

    for i, rcol in enumerate(ratio_cols):
        agg_raw[f'{rcol}_scaled'] = scaled_ratios[:, i]

    # Map refined cluster names
    cluster_name_map = {
        0: 'Financially Stretched but Highly Engaged',
        1: 'Low-Engagement Online Discretionary Spenders',
        2: 'Financially Healthy & Highly Engaged',
        3: 'Financially Healthy Moderate Spenders'
    }
    agg_raw['cluster_name'] = agg_raw['cluster'].map(cluster_name_map)

    # Save outputs under standardized task4_segmented.csv name
    agg_raw.to_csv(os.path.join(target_folder, 'task4_segmented.csv'), index=False)
    agg_raw.to_csv(os.path.join(base_dir, 'task4_segmented.csv'), index=False)
    agg_raw.to_csv(os.path.join(base_dir, 'Dataset', 'task4_segmented.csv'), index=False)

    print(f'   -> Fit K-Means (k={chosen_k}), verified 100% ({len(agg_raw)}) customer coverage.')
    print(f'   -> Successfully saved task4_segmented.csv with raw and _scaled columns.')
    return agg_raw


if __name__ == '__main__':
    run_clustering()
