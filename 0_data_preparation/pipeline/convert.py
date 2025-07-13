# -*- coding: utf-8 -*-
"""
Converts a SAS XPT file to a CSV file.
"""
import os
import sys
import pandas as pd
import argparse
from pipeline.config import CSV_DIR

def convert_xpt_to_csv(xpt_path, column_metadata=None):
    """Converts an XPT file to CSV, optionally applying metadata."""
    if not xpt_path or not os.path.exists(xpt_path):
        print(f"Error: Input file not found at '{xpt_path}'", file=sys.stderr)
        return None

    base_name = os.path.basename(xpt_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    csv_path = os.path.join(CSV_DIR, f"{file_name_without_ext}.csv")

    try:
        print(f"Reading XPT file: {xpt_path}...")
        df = pd.read_sas(xpt_path, format="xport")

        if column_metadata:
            print("Applying column and value descriptions...")
            # Create a copy of the columns to iterate over
            for col in df.columns.copy():
                if col in column_metadata:
                    # Apply value replacements
                    if 'values' in column_metadata[col] and column_metadata[col]['values']:
                        df[col] = df[col].replace(column_metadata[col]['values'])
                    # Rename column to its description if available
                    if 'description' in column_metadata[col] and column_metadata[col]['description']:
                        df.rename(columns={col: column_metadata[col]['description']}, inplace=True)

        print(f"Saving to CSV file: {csv_path}...")
        df.to_csv(csv_path, index=False)
        print(f"Successfully converted '{xpt_path}' to '{csv_path}'")
        return csv_path
    except Exception as e:
        print(f"Error converting {xpt_path}: {e}", file=sys.stderr)
        return None

def main():
    """Main function to convert a file."""
    parser = argparse.ArgumentParser(description="Convert a single XPT file to CSV.")
    parser.add_argument("xpt_path", help="The path to the input .xpt file.")
    args = parser.parse_args()

    convert_xpt_to_csv(args.xpt_path)

if __name__ == "__main__":
    main()
