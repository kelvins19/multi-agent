#!/usr/bin/env python
"""
Run script for the travel agent system.
This script should be run from the project root directory.
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import and run the main function
from src.main import main
import asyncio

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main()) 