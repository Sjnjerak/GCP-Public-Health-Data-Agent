import pandas as pd
import argparse
import sys
import os

def convert_xpt_to_csv(input_path, output_path):
    """Converts a SAS XPT file to a CSV file, with error handling."""
    try:
        print(f"Reading XPT file: {input_path}...")
        # pandas can read the file path directly
        df = pd.read_sas(input_path, format='xport')

        print(f"Saving to CSV file: {output_path}...")
        df.to_csv(output_path, index=False)

        print(f"\nSuccessfully converted '{input_path}' to '{output_path}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'", file=sys.stderr)
        print("Please check that the file exists and the path is correct.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a SAS XPT file to a CSV file.",
        epilog="Example: python xpt_to_csv_converter.py DEMO.xpt -o nhanes_demo.csv",
    )
    parser.add_argument(
        "input_file",
        help="The path to the input .xpt file."
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        help="The path for the output .csv file. (Optional: defaults to input filename with .csv extension)"
    )

    args = parser.parse_args()

    if args.output_file:
        output_path = args.output_file
    else:
        # Create a default output filename by changing the extension
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        output_path = f"{base_name}.csv"

    convert_xpt_to_csv(args.input_file, output_path)
