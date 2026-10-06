"""
Data Processing Pipeline

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys
from pprint import pprint

import pandas as pd

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data processing pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to input file")
    parser.add_argument(
        "--config", "-c", required=True, help="Path to YAML configuration file"
    )
    parser.add_argument("--output", "-o", required=True, help="Path to output file")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        f"Arguments parsed: input={args.input}, config={args.config}, "
        f"output={args.output}"
    )

    # Validate both files before loading anything
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # Load the input data and the configuration
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # The pipeline works on tables, so the input must load as a DataFrame
    if not isinstance(data, pd.DataFrame):
        logger.error(f"Input must be a CSV file for processing: {args.input}")
        sys.exit(1)

    # Read validation settings from the config
    validation = config.get("validation", {})
    required_columns = validation.get("required_columns", [])
    numeric_columns = validation.get("numeric_columns", [])

    # Validate the data
    try:
        df_valid = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validation complete: {len(data)} -> {len(df_valid)} rows")

    # Keep a copy of the validated data for the cleaning report
    df_original = df_valid.copy()

    # Process the data
    try:
        df_clean = process_data(df_valid, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df_clean)
    logger.info(
        f"Processing complete: {len(df_original)} -> {len(df_clean)} rows"
    )

    # Save the output
    output_path = save_data(df_clean, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    print("\nCleaning report:")
    pprint(report, sort_dicts=False)


if __name__ == "__main__":
    main()
