#!/usr/bin/env python
"""
Run script for the travel agent system.
This script should be run from the project root directory.
"""

import os
import sys
import asyncio

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the main function
from src.main import main

if __name__ == "__main__":
    asyncio.run(main()) 