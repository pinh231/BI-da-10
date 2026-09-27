# TASK 3 — Customer Engagement Analysis
## BI10 Round 01 | Full Reproducible Package

---

## How to Reproduce All Outputs

### Step 1 — Requirements
Python 3.10+ and the following libraries:
```
pip install pandas numpy matplotlib seaborn
```

### Step 2 — Run the Analysis Script
From the `/Users/lelinh/Documents/BI10` directory, run:
```bash
python3 task3/TASK_3/run_task3_analysis.py
```

This single script will:
1. Load both raw datasets from `BI10_ROUND01_DATASET/`
2. Build the 999-row customer-level analytical table
3. Compute all Task 3 statistics (3.1 → 3.5 + cross-analysis)
4. Save 7 charts as `.png` files into the appropriate phase folders
5. Save `DATA/customer_level_analysis.csv` (999 rows × 27 columns)
6. Save `DATA/analysis_stats.json` (all computed statistics)

**Expected runtime:** ~30–60 seconds

---

## Output File Map

```
TASK_3/
│
├── README.md                          ← This file
├── run_task3_analysis.py              ← ⭐ MAIN ANALYSIS SCRIPT (run this)
│
├── 00_DATA_UNDERSTANDING/
│   └── PHASE_0_DATA_UNDERSTANDING.md  ← Data inspection findings
│
├── 01_DATA_PREPARATION/
│   └── PHASE_1_DATA_PREPARATION.md    ← Cleaning decisions
│
├── 02_ANALYTICAL_DATASET/
│   └── PHASE_2_CUSTOMER_ANALYTICAL_TABLE.md ← How customer table was built
│
├── 03_ENGAGEMENT/
│   ├── PHASE_3_1_ENGAGEMENT_ANALYSIS.md
│   └── fig_3_1_engagement_distribution.png  ← Task 3.1 charts
│
├── 04_CHANNEL/
│   ├── PHASE_4_CHANNEL_ADOPTION.md
│   ├── fig_3_2_channel_adoption.png          ← Task 3.2 charts (adoption + spend)
│   └── fig_3_2_online_spend_distribution.png
│
├── 05_CATEGORY/
│   ├── PHASE_5_CATEGORY_DIVERSITY.md
│   ├── fig_3_3_category_diversity.png        ← Task 3.3 scatter + histogram
│   └── fig_3_3c_engagement_by_cd_group.png
│
├── 06_FREQUENCY_RECENCY/
│   ├── PHASE_6_FREQUENCY_RECENCY.md
│   └── fig_3_4_frequency_recency.png         ← Task 3.4 frequency & recency charts
│
├── 07_HEALTH_LOW_ENGAGEMENT/
│   ├── PHASE_7_HEALTHY_LOW_ENGAGEMENT.md
│   └── fig_3_5_health_engagement_matrix.png  ← Task 3.5 quadrant matrix
│
├── 08_CROSS_ANALYSIS/
│   ├── PHASE_8_CROSS_ANALYSIS.md
│   └── fig_3_6_correlation_matrix.png        ← Correlation heatmap
│
├── FINAL/
│   ├── TASK_3_FINAL_REPORT.md         ← ⭐ Competition report content (English)
│   └── TASK_3_SLIDE_CONTENT.md        ← ⭐ 7-slide presentation content (English)
│
└── DATA/
    ├── customer_level_analysis.csv    ← 999 rows × 27 columns analytical dataset
    └── analysis_stats.json            ← All computed statistics (JSON)
```

---

## Script Section Map (run_task3_analysis.py)

| Script Section | Lines | Produces |
|---|---|---|
| STEP 1 — Load data | Top | df_month, df_trans |
| STEP 2 — Customer table | After load | customer_level_analysis.csv |
| STEP 3 — Phase 3.1 | Engagement | fig_3_1_*.png |
| STEP 4 — Phase 3.2 | Channel adoption | fig_3_2_*.png |
| STEP 5 — Phase 3.3 | Category diversity | fig_3_3_*.png |
| STEP 6 — Phase 3.4 | Frequency & Recency | fig_3_4_*.png |
| STEP 7 — Phase 3.5 | Healthy + Low Engagement | fig_3_5_*.png |
| STEP 8 — Phase 3.6 | Cross analysis | fig_3_6_*.png |
| Final | Save stats | analysis_stats.json |
