"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample.csv --output cleaned_data.csv --config config.yaml
    python pipeline.py --input fixtures/sample.csv --output cleaned_data.csv --config config.yaml --verbose
"""

import argparse
import logging
import sys
from pathlib import Path
from pprint import pprint

import pandas as pd

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath).is_file():
        logger.error(f"Input file not found: {filepath}")
        return False
    logger.info(f"Input file validated: {filepath}")
    return True


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

    # The processor works on tables, so the input must load as a DataFrame
    if not isinstance(data, pd.DataFrame):
        logger.error(f"Input must be a CSV file for processing: {args.input}")
        sys.exit(1)

    # Keep a copy of the original data for the cleaning report
    df_original = data.copy()

    # Process the data
    try:
        df_clean = process_data(data, config)
    except ValueError:
        sys.exit(1)

    # Create the output
    report = create_cleaning_report(df_original, df_clean)
    print("\nCleaning report:")
    pprint(report, sort_dicts=False)

    logger.info(
        f"Processing complete: {len(df_original)} -> {len(df_clean)} rows"
    )

    df_clean.to_csv(args.output, index=False)
    logger.info(f"Saved cleaned data to {args.output}")


if __name__ == "__main__":
    main()
