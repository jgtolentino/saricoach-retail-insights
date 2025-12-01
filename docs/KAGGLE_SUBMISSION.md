# Kaggle Submission Guide

## Overview

This project is designed to run entirely within a Kaggle Notebook environment without external network access.

## Steps

1.  **Upload Dataset**: Upload the `data/processed/` CSVs as a Kaggle Dataset.
2.  **Copy Code**: Copy the `saricoach/` package and `notebooks/01_demo_saricoach.ipynb` content into the Kaggle notebook.
3.  **Run**: Execute the notebook cells. The system defaults to `csv` backend, reading from the input dataset.

## Verification

The notebook demonstrates the full agent pipeline:
1.  Loading data from CSVs.
2.  Planner deciding on a flow.
3.  Data Analyst building feature frames.
4.  Coach generating recommendations.
