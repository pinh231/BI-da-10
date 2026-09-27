"""
================================================================================
BI10 Round 01 — Task 3: Customer Engagement Analysis
Main Analysis Script
================================================================================

DESCRIPTION:
    This script performs the complete Task 3 analysis pipeline from raw data
    to final charts and statistics. It is fully reproducible: running this
    script from the project root will regenerate all outputs exactly.

HOW TO RUN:
    From /Users/lelinh/Documents/BI10, run:
        python3 task3/TASK_3/run_task3_analysis.py

INPUTS (read-only, never modified):
    BI10_ROUND01_DATASET/consumer_financial_health_engagement_2025.csv
        → 10,992 rows × 30 columns (customer-month grain)
    BI10_ROUND01_DATASET/consumer_transactions_2025.csv
        → 1,852,394 rows × 28 columns (transaction grain)

OUTPUTS PRODUCED:
    DATA/customer_level_analysis.csv        → 999-row customer analytical table
    DATA/analysis_stats.json                → All computed statistics
    03_ENGAGEMENT/fig_3_1_*.png             → Task 3.1: Engagement distribution
    04_CHANNEL/fig_3_2_*.png                → Task 3.2: Channel adoption charts
    05_CATEGORY/fig_3_3_*.png               → Task 3.3: Category diversity charts
    06_FREQUENCY_RECENCY/fig_3_4_*.png      → Task 3.4: Frequency & recency charts
    07_HEALTH_LOW_ENGAGEMENT/fig_3_5_*.png  → Task 3.5: Health × Engagement matrix
    08_CROSS_ANALYSIS/fig_3_6_*.png         → Phase 3.6: Correlation heatmap

ANALYSIS STEPS:
    Step 1 → Load both datasets
    Step 2 → Build customer-level analytical table (one row per customer)
    Step 3 → Task 3.1: Engagement score distribution + segment counts
    Step 4 → Task 3.2: Channel adoption + digital spend analysis
    Step 5 → Task 3.3: Category diversity + correlation with engagement
    Step 6 → Task 3.4: Frequency & recency analysis
    Step 7 → Task 3.5: High Health + Low Engagement group identification
    Step 8 → Phase 3.6: Cross-metric correlation matrix
    Final  → Save all stats to JSON

IMPORTANT NOTES:
    - matplotlib uses the 'Agg' (non-interactive) backend → charts are saved
      as PNG files, NOT displayed on screen. This allows the script to run
      in any environment (no GUI required).
    - Absolute VND monetary values are SYNTHETIC and are NOT used.
      Only ratios (online_spend_ratio, spend_to_income_ratio, etc.) are used.
    - No original dataset files are modified. All outputs go to task3/TASK_3/.

REQUIREMENTS:
    pandas, numpy, matplotlib, seaborn
    Install: pip install pandas numpy matplotlib seaborn
================================================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for file saving
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
BASE = '/Users/lelinh/Documents/BI10'
DATA = f'{BASE}/BI10_ROUND01_DATASET'
OUT  = f'{BASE}/task3/TASK_3'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 150,
})
PALETTE = sns.color_palette("Set2")

print("=" * 60)
print("STEP 1 — LOADING DATA")
print("=" * 60)
df_month = pd.read_csv(f'{DATA}/consumer_financial_health_engagement_2025.csv')
df_trans  = pd.read_csv(f'{DATA}/consumer_transactions_2025.csv')
df_trans['activity_datetime'] = pd.to_datetime(df_trans['activity_datetime'])
print(f"  df_month: {df_month.shape}, df_trans: {df_trans.shape}")

# ─────────────────────────────────────────────
# STEP 2 — BUILD CUSTOMER-LEVEL ANALYTICAL TABLE
# ─────────────────────────────────────────────
print("\nSTEP 2 — BUILDING CUSTOMER-LEVEL TABLE")

cust = df_month.groupby('consumer_id').agg(
    age=('age', 'first'),
    gender=('gender', 'first'),
    occupation=('occupation', 'first'),
    province_city=('province_city', 'first'),
    months_observed=('analysis_month', 'count'),
    engagement_score=('engagement_score', 'mean'),
    financial_health_score=('financial_health_score', 'mean'),
    category_diversity_avg=('category_diversity', 'mean'),
    category_diversity_max=('category_diversity', 'max'),
    transaction_count_monthly_avg=('transaction_count', 'mean'),
    transaction_count_total=('transaction_count', 'sum'),
    active_days_avg=('active_transaction_days', 'mean'),
    online_spend_ratio_avg=('online_spend_ratio', 'mean'),
    spend_to_income_ratio_avg=('spend_to_income_ratio', 'mean'),
    credit_utilization_avg=('credit_utilization_ratio', 'mean'),
    spending_volatility_avg=('spending_volatility', 'mean'),
    engagement_segment_mode=('engagement_segment', lambda x: x.mode()[0]),
    financial_health_segment_mode=('financial_health_segment', lambda x: x.mode()[0]),
).reset_index()

# True yearly recency from transactions
reference_date = pd.to_datetime('2025-12-31')
last_txn = df_trans.groupby('consumer_id')['activity_datetime'].max().reset_index()
last_txn.columns = ['consumer_id', 'last_transaction_date']
last_txn['recency_days'] = (reference_date - last_txn['last_transaction_date']).dt.days
cust = cust.merge(last_txn[['consumer_id', 'recency_days']], on='consumer_id', how='left')

# Channel adoption
channels = ['POS', 'E-commerce', 'Mobile App', 'QR Payment', 'Recurring Payment']
for ch in channels:
    users = set(df_trans[df_trans['transaction_channel'] == ch]['consumer_id'].unique())
    col = 'uses_' + ch.replace(' ', '_').replace('-', '_')
    cust[col] = cust['consumer_id'].isin(users).astype(int)
cust['num_channels_used'] = cust[['uses_POS','uses_E_commerce','uses_Mobile_App','uses_QR_Payment','uses_Recurring_Payment']].sum(axis=1)

# Engagement quartile label (for scatter coloring)
cust['eng_quartile'] = pd.qcut(cust['engagement_score'], q=4, labels=['Q1 (Low)','Q2','Q3','Q4 (High)'])

print(f"  Customer table: {cust.shape}")
cust.to_csv(f'{OUT}/DATA/customer_level_analysis.csv', index=False)
print(f"  Saved customer_level_analysis.csv")

N = len(cust)

# ─────────────────────────────────────────────
# PHASE 3.1 — ENGAGEMENT SCORE DISTRIBUTION
# ─────────────────────────────────────────────
print("\nSTEP 3 — PHASE 3.1: ENGAGEMENT DISTRIBUTION")

es = cust['engagement_score']
es_stats = {
    'N': N, 'mean': es.mean(), 'median': es.median(),
    'std': es.std(), 'min': es.min(), 'max': es.max(),
    'p10': es.quantile(0.10), 'p25': es.quantile(0.25),
    'p75': es.quantile(0.75), 'p90': es.quantile(0.90),
}

# Cutoff: use the boundaries already present in the data (verified)
cutoffs = {'Very High Engagement (≥80)': (80, 100), 'High Engagement (60–79.9)': (60, 80),
           'Moderate Engagement (40–59.9)': (40, 60), 'Low Engagement (<40)': (0, 40)}
seg_counts = {}
for label, (lo, hi) in cutoffs.items():
    cnt = ((es >= lo) & (es < hi)).sum()
    seg_counts[label] = {'n': int(cnt), 'pct': round(100*cnt/N, 2)}
# Fix the top bucket
seg_counts['Very High Engagement (≥80)']['n'] = int((es >= 80).sum())
seg_counts['Very High Engagement (≥80)']['pct'] = round(100*(es >= 80).sum()/N, 2)

for k,v in seg_counts.items():
    print(f"  {k}: n={v['n']}, {v['pct']}%")

# Chart 3.1a — Histogram
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
seg_colors = {'Very High Engagement (≥80)': '#2ecc71', 'High Engagement (60–79.9)': '#3498db',
              'Moderate Engagement (40–59.9)': '#f39c12', 'Low Engagement (<40)': '#e74c3c'}
cust['eng_label'] = pd.cut(cust['engagement_score'],
    bins=[0,40,60,80,100], labels=['Low (<40)','Moderate (40–60)','High (60–80)','Very High (≥80)'], right=False)
order = ['Low (<40)','Moderate (40–60)','High (60–80)','Very High (≥80)']
color_list = ['#e74c3c','#f39c12','#3498db','#2ecc71']

sns.histplot(data=cust, x='engagement_score', bins=40, color='#3498db', alpha=0.8, ax=axes[0])
axes[0].axvline(es_stats['mean'], color='red', linestyle='--', linewidth=1.5, label=f"Mean: {es_stats['mean']:.1f}")
axes[0].axvline(es_stats['median'], color='orange', linestyle='--', linewidth=1.5, label=f"Median: {es_stats['median']:.1f}")
axes[0].axvline(80, color='#2ecc71', linestyle=':', linewidth=1.5, label='Cutoff: 80 (Very High)')
axes[0].axvline(60, color='#e74c3c', linestyle=':', linewidth=1.5, label='Cutoff: 60 (High)')
axes[0].set_title('Fig 3.1a: Engagement Score Distribution\n(Customer-Level Yearly Average, n=999)', fontweight='bold')
axes[0].set_xlabel('Engagement Score (Yearly Average)')
axes[0].set_ylabel('Number of Customers')
axes[0].legend(fontsize=9)

seg_ns = [seg_counts[k]['n'] for k in cutoffs]
seg_labels = list(cutoffs.keys())
bars = axes[1].barh(seg_labels, seg_ns, color=['#2ecc71','#3498db','#f39c12','#e74c3c'])
for bar, (k,v) in zip(bars, seg_counts.items()):
    axes[1].text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                 f"{v['n']} ({v['pct']}%)", va='center', fontsize=10)
axes[1].set_title('Fig 3.1b: Customer Count by Engagement Segment', fontweight='bold')
axes[1].set_xlabel('Number of Customers')
axes[1].set_xlim(0, max(seg_ns)*1.25)
plt.tight_layout()
plt.savefig(f'{OUT}/03_ENGAGEMENT/fig_3_1_engagement_distribution.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_1_engagement_distribution.png")

# ─────────────────────────────────────────────
# PHASE 3.2 — CHANNEL ADOPTION
# ─────────────────────────────────────────────
print("\nSTEP 4 — PHASE 3.2: CHANNEL ADOPTION")

ch_adoption = {}
ch_txn_share = df_trans['transaction_channel'].value_counts()
ch_spend_share = df_trans.groupby('transaction_channel')['spend_amount_vnd'].sum()
total_txns = len(df_trans)
total_spend = ch_spend_share.sum()

for ch in channels:
    n_cust = int(df_trans[df_trans['transaction_channel'] == ch]['consumer_id'].nunique())
    ch_adoption[ch] = {
        'customers': n_cust, 'adoption_pct': round(100*n_cust/N, 1),
        'txn_share': round(100*ch_txn_share.get(ch,0)/total_txns, 2),
        'spend_share': round(100*ch_spend_share.get(ch,0)/total_spend, 2),
    }
    print(f"  {ch}: {n_cust} customers ({ch_adoption[ch]['adoption_pct']}%), txns={ch_adoption[ch]['txn_share']}%, spend={ch_adoption[ch]['spend_share']}%")

avg_osr = cust['online_spend_ratio_avg'].mean()
med_osr = cust['online_spend_ratio_avg'].median()
print(f"  Avg yearly online_spend_ratio: mean={avg_osr:.3f}, median={med_osr:.3f}")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
ch_names = list(ch_adoption.keys())
adoptions = [ch_adoption[c]['adoption_pct'] for c in ch_names]
txn_shares = [ch_adoption[c]['txn_share'] for c in ch_names]
spend_shares = [ch_adoption[c]['spend_share'] for c in ch_names]

bars0 = axes[0].bar(ch_names, adoptions, color=PALETTE[:5])
axes[0].set_title('Fig 3.2a: Channel Adoption Rate\n(% of 999 Customers Using Channel)', fontweight='bold')
axes[0].set_ylabel('Customer Adoption (%)')
axes[0].set_ylim(0, 115)
axes[0].tick_params(axis='x', rotation=30)
for bar, v in zip(bars0, adoptions):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{v}%", ha='center', fontsize=9)

bars1 = axes[1].bar(ch_names, txn_shares, color=PALETTE[:5])
axes[1].set_title('Fig 3.2b: Transaction Share by Channel\n(% of 1,852,394 Transactions)', fontweight='bold')
axes[1].set_ylabel('Transaction Share (%)')
axes[1].set_ylim(0, max(txn_shares)*1.2)
axes[1].tick_params(axis='x', rotation=30)
for bar, v in zip(bars1, txn_shares):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f"{v}%", ha='center', fontsize=9)

bars2 = axes[2].bar(ch_names, spend_shares, color=PALETTE[:5])
axes[2].set_title('Fig 3.2c: Spending Share by Channel\n(% of Total VND Spent)', fontweight='bold')
axes[2].set_ylabel('Spend Share (%)')
axes[2].set_ylim(0, max(spend_shares)*1.2)
axes[2].tick_params(axis='x', rotation=30)
for bar, v in zip(bars2, spend_shares):
    axes[2].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3, f"{v}%", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(f'{OUT}/04_CHANNEL/fig_3_2_channel_adoption.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_2_channel_adoption.png")

# Online spend ratio distribution
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(cust['online_spend_ratio_avg'], bins=40, color='#9b59b6', alpha=0.8, ax=ax)
ax.axvline(avg_osr, color='red', linestyle='--', linewidth=1.5, label=f"Mean: {avg_osr:.3f}")
ax.axvline(med_osr, color='orange', linestyle='--', linewidth=1.5, label=f"Median: {med_osr:.3f}")
ax.set_title('Fig 3.2d: Distribution of Yearly Average Online Spend Ratio\n(Online Spend / Total Spend, per Customer)', fontweight='bold')
ax.set_xlabel('Yearly Average Online Spend Ratio')
ax.set_ylabel('Number of Customers')
ax.legend()
plt.tight_layout()
plt.savefig(f'{OUT}/04_CHANNEL/fig_3_2_online_spend_distribution.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_2_online_spend_distribution.png")

# ─────────────────────────────────────────────
# PHASE 3.3 — CATEGORY DIVERSITY
# ─────────────────────────────────────────────
print("\nSTEP 5 — PHASE 3.3: CATEGORY DIVERSITY")

cd = cust['category_diversity_avg']
corr_cd = cd.corr(cust['engagement_score'])
print(f"  Category diversity: min={cd.min():.2f}, max={cd.max():.2f}, mean={cd.mean():.2f}, median={cd.median():.2f}")
print(f"  Correlation with engagement_score: {corr_cd:.4f}")

# Distribution of max category diversity (most meaningful for "breadth")
cd_max_counts = cust['category_diversity_max'].value_counts().sort_index()
print(f"  Distribution of max category_diversity per customer:")
for k,v in cd_max_counts.items():
    print(f"    {k}: {v} customers ({100*v/N:.1f}%)")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.histplot(cust['category_diversity_max'], bins=13, discrete=True, color='#1abc9c', alpha=0.8, ax=axes[0])
axes[0].set_title('Fig 3.3a: Distribution of Max Category Diversity\n(Broadest Month per Customer)', fontweight='bold')
axes[0].set_xlabel('Max Unique Spending Categories Used (in any month)')
axes[0].set_ylabel('Number of Customers')

sns.scatterplot(data=cust, x='category_diversity_avg', y='engagement_score', alpha=0.5, color='#1abc9c', ax=axes[1])
sns.regplot(data=cust, x='category_diversity_avg', y='engagement_score', scatter=False, color='red', ax=axes[1])
axes[1].set_title(f'Fig 3.3b: Category Diversity vs Engagement Score\n(r = {corr_cd:.3f})', fontweight='bold')
axes[1].set_xlabel('Average Category Diversity (monthly avg)')
axes[1].set_ylabel('Engagement Score (yearly avg)')
plt.tight_layout()
plt.savefig(f'{OUT}/05_CATEGORY/fig_3_3_category_diversity.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_3_category_diversity.png")

# Avg engagement by category diversity bucket
df_month['cd_group'] = pd.cut(df_month['category_diversity'], bins=[0,5,9,12,14], labels=['1–5','6–9','10–12','13–14'])
eng_by_cd = df_month.groupby('cd_group', observed=True)['engagement_score'].agg(['mean','count','std']).reset_index()
print("\n  Engagement by category diversity group:")
print(eng_by_cd.round(2).to_string(index=False))

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(eng_by_cd['cd_group'].astype(str), eng_by_cd['mean'], color='#1abc9c', alpha=0.85,
              yerr=eng_by_cd['std'], capsize=4)
ax.set_title('Fig 3.3c: Average Engagement Score by Category Diversity Group', fontweight='bold')
ax.set_xlabel('Category Diversity Range')
ax.set_ylabel('Average Engagement Score')
ax.set_ylim(50, 90)
for bar, row in zip(bars, eng_by_cd.itertuples()):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1, f"{row.mean:.1f}\n(n={row.count})", ha='center', fontsize=9)
plt.tight_layout()
plt.savefig(f'{OUT}/05_CATEGORY/fig_3_3c_engagement_by_cd_group.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_3c_engagement_by_cd_group.png")

# ─────────────────────────────────────────────
# PHASE 3.4 — FREQUENCY & RECENCY
# ─────────────────────────────────────────────
print("\nSTEP 6 — PHASE 3.4: FREQUENCY & RECENCY")

freq = cust['transaction_count_monthly_avg']
rec  = cust['recency_days']
corr_freq = freq.corr(cust['engagement_score'])
corr_rec  = rec.corr(cust['engagement_score'])
corr_active = cust['active_days_avg'].corr(cust['engagement_score'])

print(f"  Frequency (monthly avg txn count): min={freq.min():.1f}, max={freq.max():.1f}, mean={freq.mean():.1f}, median={freq.median():.1f}")
print(f"  Recency (days since last txn to 31-Dec): min={rec.min()}, max={rec.max()}, mean={rec.mean():.1f}, median={rec.median():.1f}")
print(f"  Corr frequency vs engagement: {corr_freq:.4f}")
print(f"  Corr recency vs engagement:   {corr_rec:.4f}")
print(f"  Corr active_days vs engagement: {corr_active:.4f}")

# Note: recency_days = -1 means last txn was on Dec 31 (reference date - 0 days → -1 due to inclusive counting)
n_recency_neg = (rec <= 0).sum()
print(f"  Customers with recency_days <= 0 (transacted on/after Dec 31): {n_recency_neg}")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Freq distribution
sns.histplot(freq, bins=40, color='#3498db', alpha=0.8, ax=axes[0,0])
axes[0,0].axvline(freq.mean(), color='red', linestyle='--', label=f"Mean: {freq.mean():.1f}")
axes[0,0].set_title('Fig 3.4a: Distribution of Monthly Transaction Frequency', fontweight='bold')
axes[0,0].set_xlabel('Avg Monthly Transactions per Customer')
axes[0,0].set_ylabel('Customers')
axes[0,0].legend()

# Recency distribution (clip negatives for display)
rec_display = rec.clip(lower=0)
sns.histplot(rec_display, bins=40, color='#e74c3c', alpha=0.8, ax=axes[0,1])
axes[0,1].axvline(rec_display.median(), color='orange', linestyle='--', label=f"Median: {rec_display.median():.0f}")
axes[0,1].set_title('Fig 3.4b: Distribution of Transaction Recency\n(Days Since Last Transaction to Dec 31, 2025)', fontweight='bold')
axes[0,1].set_xlabel('Recency (Days)')
axes[0,1].set_ylabel('Customers')
axes[0,1].legend()

# Freq vs engagement
sns.scatterplot(data=cust, x='transaction_count_monthly_avg', y='engagement_score', alpha=0.5, color='#3498db', ax=axes[1,0])
sns.regplot(data=cust, x='transaction_count_monthly_avg', y='engagement_score', scatter=False, color='red', ax=axes[1,0])
axes[1,0].set_title(f'Fig 3.4c: Frequency vs Engagement Score\n(r = {corr_freq:.3f})', fontweight='bold')
axes[1,0].set_xlabel('Avg Monthly Transaction Count')
axes[1,0].set_ylabel('Engagement Score')

# Recency vs engagement
sns.scatterplot(data=cust, x='recency_days', y='engagement_score', alpha=0.5, color='#e74c3c', ax=axes[1,1])
sns.regplot(data=cust, x='recency_days', y='engagement_score', scatter=False, color='darkred', ax=axes[1,1])
axes[1,1].set_title(f'Fig 3.4d: Recency vs Engagement Score\n(r = {corr_rec:.3f})', fontweight='bold')
axes[1,1].set_xlabel('Recency Days (lower = more recent)')
axes[1,1].set_ylabel('Engagement Score')

plt.tight_layout()
plt.savefig(f'{OUT}/06_FREQUENCY_RECENCY/fig_3_4_frequency_recency.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_4_frequency_recency.png")

# ─────────────────────────────────────────────
# PHASE 3.5 — HIGH HEALTH + LOW ENGAGEMENT
# ─────────────────────────────────────────────
print("\nSTEP 7 — PHASE 3.5: HIGH HEALTH + LOW ENGAGEMENT")

eng_p25 = cust['engagement_score'].quantile(0.25)  # ~74.77
fhs_p75 = cust['financial_health_score'].quantile(0.75)  # ~69.28
print(f"  Engagement P25: {eng_p25:.2f}")
print(f"  Health P75:     {fhs_p75:.2f}")

# Selected cutoffs: health >= 70 (above mean+0.8 SD → above-average) , engagement < 70 (below P25 after rounding)
HEALTH_CUT = 70
ENG_CUT    = 70

hd = cust[(cust['financial_health_score'] >= HEALTH_CUT) & (cust['engagement_score'] < ENG_CUT)]
rest = cust[~cust.index.isin(hd.index)]

print(f"\n  SELECTED CUTOFF: health>={HEALTH_CUT} AND engagement<{ENG_CUT}")
print(f"  Group size: {len(hd)} customers ({100*len(hd)/N:.1f}% of {N})")

# Profile comparison
compare_cols = ['engagement_score','financial_health_score','transaction_count_monthly_avg',
                'recency_days','category_diversity_avg','online_spend_ratio_avg','active_days_avg']
print(f"\n  Profile comparison (High Health + Low Engagement) vs (All Others):")
profile = pd.DataFrame({
    'HD Group': hd[compare_cols].mean(),
    'All Others': rest[compare_cols].mean(),
    'Overall': cust[compare_cols].mean()
}).round(3)
print(profile.to_string())

# Cutoff comparison table
print("\n  Cutoff sensitivity analysis:")
for hc, ec in [(75, 70), (70, 70), (70, 65), (65, 70)]:
    g = cust[(cust['financial_health_score'] >= hc) & (cust['engagement_score'] < ec)]
    print(f"    Health>={hc}, Eng<{ec}: {len(g)} customers ({100*len(g)/N:.1f}%)")

# Chart 3.5 — Health × Engagement scatter
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# All customers scatter
colors = np.where(
    (cust['financial_health_score'] >= HEALTH_CUT) & (cust['engagement_score'] < ENG_CUT),
    '#e74c3c', '#3498db')
axes[0].scatter(cust['financial_health_score'], cust['engagement_score'],
                c=colors, alpha=0.6, s=35)
axes[0].axhline(ENG_CUT, color='gray', linestyle='--', linewidth=1.2, label=f'Engagement cutoff = {ENG_CUT}')
axes[0].axvline(HEALTH_CUT, color='gray', linestyle=':', linewidth=1.2, label=f'Health cutoff = {HEALTH_CUT}')
red_patch = mpatches.Patch(color='#e74c3c', label=f'High Health + Low Engagement (n={len(hd)})')
blue_patch = mpatches.Patch(color='#3498db', label='All other customers')
axes[0].legend(handles=[red_patch, blue_patch], fontsize=9)
axes[0].set_title(f'Fig 3.5a: Financial Health × Engagement Matrix\n(n=999 customers)', fontweight='bold')
axes[0].set_xlabel('Financial Health Score (Yearly Avg)')
axes[0].set_ylabel('Engagement Score (Yearly Avg)')

# Group sizes 2x2 matrix
quadrant_data = {
    'High Health\nHigh Engagement': len(cust[(cust['financial_health_score'] >= HEALTH_CUT) & (cust['engagement_score'] >= ENG_CUT)]),
    'High Health\nLow Engagement\n★ Target Group': len(hd),
    'Low Health\nHigh Engagement': len(cust[(cust['financial_health_score'] < HEALTH_CUT) & (cust['engagement_score'] >= ENG_CUT)]),
    'Low Health\nLow Engagement': len(cust[(cust['financial_health_score'] < HEALTH_CUT) & (cust['engagement_score'] < ENG_CUT)]),
}
colors_quad = ['#2ecc71','#e74c3c','#f39c12','#95a5a6']
positions = [(0.25,0.75),(0.75,0.75),(0.25,0.25),(0.75,0.25)]
axes[1].set_xlim(0,1); axes[1].set_ylim(0,1)
axes[1].axhline(0.5, color='gray', linewidth=1); axes[1].axvline(0.5, color='gray', linewidth=1)
axes[1].set_xticks([0.25,0.75]); axes[1].set_xticklabels(['Low Health\n(< 70)','High Health\n(≥ 70)'])
axes[1].set_yticks([0.25,0.75]); axes[1].set_yticklabels(['Low Eng\n(< 70)','High Eng\n(≥ 70)'])
for (label, n), color, (px, py) in zip(quadrant_data.items(), colors_quad, positions):
    axes[1].add_patch(plt.Rectangle((px-0.24, py-0.24), 0.48, 0.48,
                      color=color, alpha=0.35, transform=axes[1].transAxes))
    axes[1].text(px, py, f"{label}\nn={n}\n({100*n/N:.1f}%)",
                ha='center', va='center', fontsize=9, fontweight='bold', transform=axes[1].transAxes)
axes[1].set_title('Fig 3.5b: Health × Engagement Quadrant Matrix\n(Customer Counts)', fontweight='bold')

plt.tight_layout()
plt.savefig(f'{OUT}/07_HEALTH_LOW_ENGAGEMENT/fig_3_5_health_engagement_matrix.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_5_health_engagement_matrix.png")

# ─────────────────────────────────────────────
# PHASE 3.6 — CROSS ANALYSIS
# ─────────────────────────────────────────────
print("\nSTEP 8 — PHASE 3.6: CROSS ANALYSIS")

cross_corrs = cust[['engagement_score','financial_health_score','transaction_count_monthly_avg',
                     'recency_days','category_diversity_avg','online_spend_ratio_avg','active_days_avg']].corr()
print("\n  Correlation matrix:")
print(cross_corrs.round(3).to_string())

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(cross_corrs, annot=True, fmt='.2f', cmap='RdYlGn', center=0,
            square=True, linewidths=0.5, ax=ax, annot_kws={'size': 10})
ax.set_title('Fig 3.6a: Correlation Matrix — Key Engagement Metrics', fontweight='bold')
plt.tight_layout()
plt.savefig(f'{OUT}/08_CROSS_ANALYSIS/fig_3_6_correlation_matrix.png', bbox_inches='tight')
plt.close()
print("  Saved fig_3_6_correlation_matrix.png")

# ─────────────────────────────────────────────
# WRITE STATS SUMMARY TO FILE FOR MD DOCS
# ─────────────────────────────────────────────
stats = {
    'N': N,
    'es_mean': round(es_stats['mean'], 2), 'es_median': round(es_stats['median'], 2),
    'es_std': round(es_stats['std'], 2), 'es_min': round(es_stats['min'], 2), 'es_max': round(es_stats['max'], 2),
    'es_p10': round(es_stats['p10'], 2), 'es_p25': round(es_stats['p25'], 2),
    'es_p75': round(es_stats['p75'], 2), 'es_p90': round(es_stats['p90'], 2),
    'seg_counts': seg_counts,
    'ch_adoption': ch_adoption,
    'avg_osr': round(avg_osr, 4), 'med_osr': round(med_osr, 4),
    'cd_mean': round(cd.mean(), 2), 'cd_median': round(cd.median(), 2),
    'cd_min': round(cd.min(), 2), 'cd_max': round(cd.max(), 2),
    'corr_cd': round(corr_cd, 4),
    'freq_mean': round(freq.mean(), 1), 'freq_median': round(freq.median(), 1),
    'freq_min': round(freq.min(), 1), 'freq_max': round(freq.max(), 1),
    'rec_mean': round(rec.mean(), 1), 'rec_median': round(rec.median(), 1),
    'rec_min': int(rec.min()), 'rec_max': int(rec.max()),
    'corr_freq': round(corr_freq, 4), 'corr_rec': round(corr_rec, 4), 'corr_active': round(corr_active, 4),
    'HEALTH_CUT': HEALTH_CUT, 'ENG_CUT': ENG_CUT,
    'hd_n': len(hd), 'hd_pct': round(100*len(hd)/N, 1),
    'fhs_mean': round(cust['financial_health_score'].mean(), 2),
    'fhs_std': round(cust['financial_health_score'].std(), 2),
    'cross_corrs': cross_corrs.round(3).to_dict(),
    'profile': profile.to_dict(),
    'eng_by_cd': eng_by_cd.round(2).to_dict(),
    'quadrant': quadrant_data,
}

import json
with open(f'{OUT}/DATA/analysis_stats.json', 'w') as f:
    json.dump(stats, f, indent=2, default=str)
print(f"\n  Saved analysis_stats.json")

print("\n" + "=" * 60)
print("ALL CHARTS AND DATA GENERATED SUCCESSFULLY")
print("=" * 60)
print(f"\nKey numbers summary:")
print(f"  Total customers: {N}")
print(f"  Engagement score: mean={stats['es_mean']}, median={stats['es_median']}, std={stats['es_std']}")
print(f"  Very High Engagement: {seg_counts['Very High Engagement (≥80)']['n']} ({seg_counts['Very High Engagement (≥80)']['pct']}%)")
print(f"  High Engagement:      {seg_counts['High Engagement (60–79.9)']['n']} ({seg_counts['High Engagement (60–79.9)']['pct']}%)")
print(f"  Moderate Engagement:  {seg_counts['Moderate Engagement (40–59.9)']['n']} ({seg_counts['Moderate Engagement (40–59.9)']['pct']}%)")
print(f"  Low Engagement:       {seg_counts['Low Engagement (<40)']['n']} ({seg_counts['Low Engagement (<40)']['pct']}%)")
print(f"  HD Group (health>={HEALTH_CUT} & eng<{ENG_CUT}): {len(hd)} customers ({100*len(hd)/N:.1f}%)")
