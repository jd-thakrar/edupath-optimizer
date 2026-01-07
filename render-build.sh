#!/bin/bash
# Force pip to use pre-built wheels only (no compilation)
pip install --only-binary :all: -r requirements.txt
