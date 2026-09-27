"""
Step 1: Feature Engineering & Monthly Aggregation
-------------------------------------------------
This module loads the raw monthly 2025 consumer financial health dataset,
computes ratio features, aggregates monthly metrics to consumer level,
and standardizes ratio columns using StandardScaler.
Output file: task4_features.csv
"""

import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def run_feature_engineering(base_dir=r'd:\BI10_Foemtubi'):
    print('[Step 1] Running Feature Engineering & Monthly Aggregation...')
    raw_path = os.path.join(base_dir, 'Dataset', 'consumer_financial_health_engagement_2025.csv')
    df_raw = pd.read_csv(raw_path)
    
    # Parse dates and ensure chronological order
    df_raw['analysis_month'] = pd.to_datetime(df_raw['analysis_month'])
    df_raw = df_raw.sort_values(['consumer_id', 'analysis_month'])

    # Construct monthly additional ratio features
    df_raw['credit_to_income_ratio'] = df_raw['credit_limit_vnd'] / df_raw['monthly_income_vnd']

    # Aggregate per consumer_id across 2025
    agg_dict = {
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
    }

    df_agg = df_raw.groupby('consumer_id', as_index=False).agg(agg_dict)

    # Standardize ratio features
    ratio_cols = [
        'credit_utilization_ratio',
        'essential_spend_ratio',
        'discretionary_spend_ratio',
        'online_spend_ratio',
        'credit_to_income_ratio',
        'spend_to_income_ratio'
    ]

    scaler = StandardScaler()
    df_scaled = df_agg.copy()
    df_scaled[ratio_cols] = scaler.fit_transform(df_agg[ratio_cols])

    # Save output dataset
    out_root = os.path.join(base_dir, 'task4_features.csv')
    out_dataset = os.path.join(base_dir, 'Dataset', 'task4_features.csv')
    
    df_scaled.to_csv(out_root, index=False)
    df_scaled.to_csv(out_dataset, index=False)
    
    print(f'   -> Successfully generated task4_features.csv ({len(df_scaled)} consumers, {len(df_scaled.columns)} columns)')
    return df_scaled


if __name__ == '__main__':
    run_feature_engineering()
