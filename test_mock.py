#!/usr/bin/env python
"""
Test script for the mock data.
This script should be run from the project root directory.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import and run the test function
from src.test_mock_data import main

if __name__ == "__main__":
    main() 