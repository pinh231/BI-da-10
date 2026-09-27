# Task 4 — Limitations and Future Work

- **Synthetic financial data**: Monthly income, credit limit, and account balance values are synthetically generated, which may not fully reflect complex real-world correlation structures.
- **Engagement score skew**: Engagement scores skew artificially high across the sample because all cardholders are active account users, omitting completely dormant or churned customers.
- **Illustrative geographical metadata**: Sub-province location fields (ward/commune names) serve as illustrative placeholders, whereas only the 34 province/city names are canonical.
- **K-Means structural assumptions**: K-Means assumes spherical, equal-variance clusters using Euclidean distance, making it sensitive to extreme financial outliers and spending spikes.
- **Subjective cluster selection (k=4)**: Although k=3 achieved the highest silhouette score (0.2520), k=4 was selected because it provides significantly better business interpretability and persona differentiation.
- **Future work & model expansion**: Future iterations should test GMM or DBSCAN for soft and density-based clustering, integrate supervised churn/default target labels, and leverage multi-year longitudinal data to track segment migration over time.
