"""
Task 4 Customer Segmentation Root Pipeline Entry Point
------------------------------------------------------
Run this script to re-execute the entire Task 4 segmentation pipeline end-to-end.
"""

import os
import sys

# Add src to sys.path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.append(src_path)

from run_all import main

if __name__ == '__main__':
    main()
