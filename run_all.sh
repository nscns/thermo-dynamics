#!/usr/bin/env bash
set -e
echo "Installing requirements..."
python -m pip install -r requirements.txt
echo "Running auto runner (no input)..."
python auto_run.py
echo "Done. Plots are in ./plots"
