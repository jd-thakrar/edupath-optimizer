#!/bin/bash
# Install scipy first with binary-only flag to avoid compilation
pip install --only-binary scipy "scipy>=1.14.1"
# Then install rest
pip install -r requirements.txt
