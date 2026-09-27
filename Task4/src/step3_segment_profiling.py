"""
Step 3: Segment Profiling & Radar Visualization
-----------------------------------------------
This module calculates cluster averages strictly using raw original values,
exports the formatted profile comparison table to Excel (task4_segment_profile_table.xlsx),
and plots a real 0-100% scale radar chart (task4_segment_radar_chart.png).
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import pi
import openpyxl


def safe_save_fig(fig, filepath):
    try:
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


def run_segment_profiling(base_dir=r'd:\BI10_Foemtubi'):
    print('[Step 3] Running Segment Profiling & Visualization...')
    segmented_csv_path = os.path.join(base_dir, 'task4_segmented.csv')
    df_fixed = pd.read_csv(segmented_csv_path)

    cluster_name_map = {
        0: 'Financially Stretched but Highly Engaged',
        1: 'Low-Engagement Online Discretionary Spenders',
        2: 'Financially Healthy & Highly Engaged',
        3: 'Financially Healthy Moderate Spenders'
    }

    # 1. Build Excel Profile Table using raw unscaled metrics
    summary_rows = []
    total_n = len(df_fixed)

    for c_id in sorted(df_fixed['cluster'].unique()):
        sub = df_fixed[df_fixed['cluster'] == c_id]
        n_cust = len(sub)
        pct_cust = n_cust / total_n * 100

        row = {
            'Cluster ID': c_id,
            'Cluster Name': cluster_name_map[c_id],
            'Cluster Size (n)': n_cust,
            'Cluster Size (%)': round(pct_cust, 2),
            'Financial Health Score': round(sub['financial_health_score'].mean(), 2),
            'Engagement Score': round(sub['engagement_score'].mean(), 2),
            'Essential Spend Ratio (%)': round(sub['essential_spend_ratio'].mean() * 100, 2),
            'Discretionary Spend Ratio (%)': round(sub['discretionary_spend_ratio'].mean() * 100, 2),
            'Online Spend Ratio (%)': round(sub['online_spend_ratio'].mean() * 100, 2),
            'Category Diversity (Count)': round(sub['category_diversity'].mean(), 2),
            'Credit Utilization Ratio (%)': round(sub['credit_utilization_ratio'].mean() * 100, 2),
            'Spending Volatility': round(sub['spending_volatility'].mean(), 2),
            'Spend to Income Ratio (%)': round(sub['spend_to_income_ratio'].mean() * 100, 2),
            'Credit to Income Ratio': round(sub['credit_to_income_ratio'].mean(), 2),
            'Monthly Income (VND)': round(sub['monthly_income_vnd'].mean(), 0),
            'Monthly Tx Count': round(sub['transaction_count'].mean(), 1)
        }
        summary_rows.append(row)

    profile_df = pd.DataFrame(summary_rows)

    excel_root = os.path.join(base_dir, 'task4_segment_profile_table.xlsx')
    excel_ds = os.path.join(base_dir, 'Dataset', 'task4_segment_profile_table.xlsx')

    with pd.ExcelWriter(excel_root, engine='openpyxl') as writer:
        profile_df.to_excel(writer, sheet_name='Segment_Profiles', index=False)
    with pd.ExcelWriter(excel_ds, engine='openpyxl') as writer:
        profile_df.to_excel(writer, sheet_name='Segment_Profiles', index=False)

    print(f'   -> Successfully saved task4_segment_profile_table.xlsx')

    # 2. Plot Real-Scale Radar Chart (0-100% scale)
    radar_metrics_raw = [
        'financial_health_score',
        'engagement_score',
        'essential_spend_ratio',
        'discretionary_spend_ratio',
        'online_spend_ratio',
        'credit_utilization_ratio',
        'category_diversity',
        'spend_to_income_ratio'
    ]

    radar_labels = [
        'Financial Health Score\n(0-100)',
        'Engagement Score\n(0-100)',
        'Essential Spend Ratio\n(%)',
        'Discretionary Spend Ratio\n(%)',
        'Online Spend Ratio\n(%)',
        'Credit Utilization Ratio\n(%)',
        'Category Diversity\n(% of 15 categories)',
        'Spend to Income Ratio\n(%)'
    ]

    radar_values_df = pd.DataFrame()
    means_fixed = df_fixed.groupby('cluster')[radar_metrics_raw].mean()

    radar_values_df['financial_health_score'] = means_fixed['financial_health_score']
    radar_values_df['engagement_score'] = means_fixed['engagement_score']
    radar_values_df['essential_spend_ratio'] = means_fixed['essential_spend_ratio'] * 100
    radar_values_df['discretionary_spend_ratio'] = means_fixed['discretionary_spend_ratio'] * 100
    radar_values_df['online_spend_ratio'] = means_fixed['online_spend_ratio'] * 100
    radar_values_df['credit_utilization_ratio'] = means_fixed['credit_utilization_ratio'] * 100
    radar_values_df['category_diversity'] = (means_fixed['category_diversity'] / 15.0) * 100
    radar_values_df['spend_to_income_ratio'] = means_fixed['spend_to_income_ratio'] * 100

    N = len(radar_labels)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    fig = plt.figure(figsize=(10, 8), dpi=300)
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(angles[:-1], radar_labels, size=10, fontweight='bold')
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ['20%', '40%', '60%', '80%', '100%'], color='grey', size=9)
    plt.ylim(0, 100)

    colors = ['#d62728', '#9467bd', '#2ca02c', '#1f77b4']

    for c_id in [0, 1, 2, 3]:
        vals = radar_values_df.loc[c_id].values.flatten().tolist()
        vals += vals[:1]
        ax.plot(angles, vals, linewidth=2, linestyle='-', label=f'Cluster {c_id}: {cluster_name_map[c_id]}', color=colors[c_id])
        ax.fill(angles, vals, color=colors[c_id], alpha=0.12)

    plt.title('Customer Segment Behavioral Profiles (Real % & Score Scale)', fontsize=14, fontweight='bold', pad=30)
    plt.legend(loc='upper right', bbox_to_anchor=(1.45, 1.15), fontsize=9, frameon=True)
    plt.tight_layout()

    radar_root = os.path.join(base_dir, 'task4_segment_radar_chart.png')
    radar_ds = os.path.join(base_dir, 'Dataset', 'task4_segment_radar_chart.png')
    safe_save_fig(fig, radar_root)
    safe_save_fig(fig, radar_ds)
    plt.close(fig)

    print(f'   -> Successfully saved task4_segment_radar_chart.png')
    return profile_df


if __name__ == '__main__':
    run_segment_profiling()
