# MP1 Data Pipeline

This project is a command-line data pipeline that loads, validates, cleans, and saves tabular data. `pipeline.py` coordinates the workflow: it parses the command-line arguments, checks that the input and config files exist, loads both, then passes the data through validation, processing, and output in that order. All cleaning choices (which columns to check, which steps to run, and the outlier method and threshold) live in `config/config.yaml`, so a new dataset only needs a new config, not code changes. The reusable code lives in the `src/` package. `data_loaders.py` loads CSV, JSON, and YAML files based on the file extension, and `data_validator.py` makes sure required columns exist and removes rows with non-numeric values in numeric columns. `data_processor.py` removes duplicates, missing values, and outliers (IQR or z-score) and builds a cleaning report, `data_output.py` saves the cleaned data as a CSV, and `utils.py` handles logging setup and file validation. Sample files for testing are in `fixtures/`, and cleaned results are written to `output/`, which is not committed to Git.

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
INFO     src.utils — Input file validated: fixtures/sample_data.csv
INFO     src.utils — Input file validated: config/config.yaml
INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
INFO     src.data_loaders — Loaded YAML file: config/config.yaml
WARNING  src.data_validator — Invalid numeric value in rating at row 94: 'not_available'
WARNING  src.data_validator — Invalid numeric value in rating at row 95: 'error'
WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
DEBUG    src.data_validator — Validation: 100 -> 98 rows
INFO     __main__ — Validation complete: 100 -> 98 rows
DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
INFO     __main__ — Processing complete: 98 -> 92 rows
DEBUG    src.data_output — Saved 92 rows to output/clean.csv
INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}
```
