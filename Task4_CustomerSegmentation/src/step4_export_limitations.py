"""
Step 4: Export Task 4 Limitations & Future Work
-----------------------------------------------
This module exports the Task 4 Limitations and Future Work documentation to markdown.
Output file: Task4_Limitations_and_Future_Work.md
"""

import os


def run_export_limitations(base_dir=r'd:\BI10_Foemtubi'):
    print('[Step 4] Exporting Task 4 Limitations and Future Work Markdown...')
    
    target_folder = os.path.join(base_dir, 'Task4_CustomerSegmentation')
    os.makedirs(target_folder, exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'Dataset'), exist_ok=True)

    content = """# Task 4 — Limitations and Future Work

- **Synthetic financial data**: Monthly income, credit limit, and account balance values are synthetically generated, which may not fully reflect complex real-world correlation structures.
- **Engagement score skew**: Engagement scores skew artificially high across the sample because all cardholders are active account users, omitting completely dormant or churned customers.
- **Illustrative geographical metadata**: Sub-province location fields (ward/commune names) serve as illustrative placeholders, whereas only the 34 province/city names are canonical.
- **K-Means structural assumptions**: K-Means assumes spherical, equal-variance clusters using Euclidean distance, making it sensitive to extreme financial outliers and spending spikes.
- **Subjective cluster selection (k=4)**: Although k=3 achieved the highest silhouette score (0.2520), k=4 was selected because it provides significantly better business interpretability and persona differentiation.
- **Future work & model expansion**: Future iterations should test GMM or DBSCAN for soft and density-based clustering, integrate supervised churn/default target labels, and leverage multi-year longitudinal data to track segment migration over time.
"""

    md_target = os.path.join(target_folder, 'Task4_Limitations_and_Future_Work.md')
    md_path = os.path.join(base_dir, 'Task4_Limitations_and_Future_Work.md')
    md_ds = os.path.join(base_dir, 'Dataset', 'Task4_Limitations_and_Future_Work.md')

    with open(md_target, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    with open(md_ds, 'w', encoding='utf-8') as f:
        f.write(content)

    print('   -> Successfully saved Task4_Limitations_and_Future_Work.md')


if __name__ == '__main__':
    run_export_limitations()
