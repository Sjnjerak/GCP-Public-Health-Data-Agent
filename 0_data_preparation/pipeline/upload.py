# -*- coding: utf-8 -*-
"""
Uploads a CSV file to a Google BigQuery table.
"""
import sys
import argparse
from google.cloud import bigquery
from google.api_core import exceptions
from pipeline.config import GCP_PROJECT_ID, BIGQUERY_DATASET_ID

def upload_to_bigquery(csv_path, table_id, column_metadata=None):
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

        if column_metadata:
            print(f"Updating column descriptions for {full_table_id}...")
            try:
                table = client.get_table(full_table_id)
                new_schema = []
                schema_changed = False
                for field in table.schema:
                    description = field.description
                    if field.name in column_metadata and "description" in column_metadata[field.name]:
                        new_description = column_metadata[field.name]["description"]
                        if description != new_description:
                            description = new_description
                            schema_changed = True

                    new_field = bigquery.SchemaField.from_api_repr(field.to_api_repr())
                    new_field._description = description
                    new_schema.append(new_field)

                if schema_changed:
                    table.schema = new_schema
                    client.update_table(table, ["schema"])
                    print("Successfully updated table schema with descriptions.")
                else:
                    print("No schema description changes needed.")

            except Exception as e:
                print(
                    f"Could not update table schema for {full_table_id}: {e}", file=sys.stderr
                )

    except exceptions.GoogleAPICallError as e:
        print(f"BigQuery API Error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during BigQuery upload: {e}", file=sys.stderr)
