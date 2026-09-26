"""
Master Task 4 Customer Segmentation Pipeline
---------------------------------------------
Executes all 4 steps of the customer segmentation pipeline sequentially.
"""

import os
import sys
import time

# Ensure src module is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from step1_feature_engineering import run_feature_engineering
from step2_clustering import run_clustering
from step3_segment_profiling import run_segment_profiling
from step4_export_limitations import run_export_limitations


def main():
    print('=====================================================================')
    print('       STARTING TASK 4 CUSTOMER SEGMENTATION DATA PIPELINE           ')
    print('=====================================================================')
    start_time = time.time()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Step 1: Feature Engineering & Aggregation
    run_feature_engineering(base_dir)

    # Step 2: K-Means Clustering & Model Fitting
    run_clustering(base_dir, chosen_k=4)

    # Step 3: Segment Profiling & Visualization
    run_segment_profiling(base_dir)

    # Step 4: Export Limitations & Future Work
    run_export_limitations(base_dir)

    elapsed = time.time() - start_time
    print('=====================================================================')
    print(f' PIPELINE COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS!')
    print('=====================================================================')


if __name__ == '__main__':
    main()
