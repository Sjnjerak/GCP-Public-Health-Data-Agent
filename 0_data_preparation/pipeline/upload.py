# -*- coding: utf-8 -*-
"""
Uploads a CSV file to a Google BigQuery table.
"""
import sys
import argparse
from google.cloud import bigquery
from google.api_core import exceptions
from pipeline.config import GCP_PROJECT_ID, BIGQUERY_DATASET_ID

def upload_to_bigquery(csv_path, table_id):
    """Uploads a CSV file to BigQuery."""
    if not csv_path:
        return

    try:
        client = bigquery.Client(project=GCP_PROJECT_ID)
        dataset_ref = client.dataset(BIGQUERY_DATASET_ID)

        try:
            client.get_dataset(dataset_ref)
        except exceptions.NotFound:
            print(f"Creating dataset: '{BIGQUERY_DATASET_ID}'")
            client.create_dataset(dataset_ref)

        full_table_id = f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET_ID}.{table_id}"
        print(f"Uploading {csv_path} to BigQuery table: {full_table_id}")

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        with open(csv_path, "rb") as source_file:
            job = client.load_table_from_file(
                source_file, full_table_id, job_config=job_config
            )

        job.result()
        print(f"Successfully loaded {job.output_rows} rows into {full_table_id}")

    except exceptions.GoogleAPICallError as e:
        print(f"BigQuery API Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during BigQuery upload: {e}", file=sys.stderr)

def main():
    """Main function to upload a file."""
    parser = argparse.ArgumentParser(description="Upload a CSV file to BigQuery.")
    parser.add_argument("csv_path", help="The path to the input .csv file.")
    parser.add_argument("table_id", help="The BigQuery table ID.")
    args = parser.parse_args()

    upload_to_bigquery(args.csv_path, args.table_id)

if __name__ == "__main__":
    main()
