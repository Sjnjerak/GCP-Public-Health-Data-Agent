# GCP Public Health Data Agent

This project aims to build an AI-powered data analyst for the CDC's National Health and Nutrition Examination Survey (NHANES) dataset. The goal is to create a system that can take a natural language question, query the NHANES data in BigQuery, and return an answer with a visualization and a written insight.

## Project Status

This project is currently in **Week 2: Module 1 - Foundational Data Exploration**.

### Completed
- **Week 1: Module 0 - Project Setup & Git Initialization**
  - The Google Cloud project has been created and the necessary APIs have been enabled.
  - The local development environment is set up with a virtual environment and the required packages.
  - The project is version-controlled with Git and pushed to this GitHub repository.
  - A data pipeline has been created to download the NHANES data, convert it to CSV, and upload it to BigQuery.

### Next Steps
- Manually explore the NHANES dataset to find an interesting relationship to focus on.
- Build a simple agent that translates a natural language question into a BigQuery SQL query.

## Data Pipeline

The `0_data_preparation` directory contains a Python-based data pipeline that automates the process of downloading, converting, and uploading the NHANES data to Google BigQuery.

To run the pipeline, first install the required packages:
```bash
pip install -r 0_data_preparation/requirements.txt
```

Then, run the pipeline script:
```bash
python 0_data_preparation/run_pipeline.py
```

This will download the data for the configured years, convert it to CSV, and upload it to the `nhanes_data` dataset in the `public-health-agent` BigQuery project.