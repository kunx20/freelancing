
# Sales Report Automation

A beginner-friendly Python project that validates sales data from a CSV file
and generates a formatted Excel sales report.

## Features

- Reads sales records from a CSV file
- Detects missing and invalid values
- Removes exact duplicate records
- Calculates revenue for each sale and product
- Generates a formatted Excel workbook with summary and detail sheets

## Technologies

- Python
- CSV module
- OpenPyXL

## Requirements

- Python 3.8 or newer
- OpenPyXL

## Installation

Install the required package:

```bash
python -m pip install openpyxl
```

On Windows, if the `python` command is not available, use:

```powershell
py -m pip install openpyxl
```

## Project Structure

```text
sales-report-automation/
├── csv_processor.py       # Validates sales.csv
├── sales_report.py        # Creates the Excel report
├── sales.csv              # Source sales data
├── validated_sales.csv    # Generated clean data
└── sales_report.xlsx      # Generated Excel report
```

## Input File Format

The input file must be named `sales.csv` and must be in the same directory as
the Python scripts. It must contain these columns:

```csv
Product,Quantity,Price
Laptop,2,40000
Mouse,5,500
```

- `Product` must not be empty.
- `Quantity` must be a positive whole number.
- `Price` must be a non-negative number.
- Exact duplicate records are skipped.

Invalid rows are reported in the terminal and are not written to
`validated_sales.csv`.

## How to Run

Open a terminal in the project directory:

```powershell
cd "D:\ desktop\freelancing\sales-report-automation"
```

Run the validation step first:

```bash
python csv_processor.py
```

Then generate the Excel report:

```bash
python sales_report.py
```

Alternatively, use `py` instead of `python` on Windows:

```powershell
py csv_processor.py
py sales_report.py
```

Run both commands from the project directory because the scripts use relative
file paths.

## Generated Report

The project creates:

- `validated_sales.csv`, containing only valid, non-duplicate records.
- `sales_report.xlsx`, containing:
  - **Summary**: total revenue, total quantity sold, valid sales records, and
    product-level totals.
  - **Sales Details**: each valid sale with product, quantity, unit price, and
    calculated revenue.

Revenue is calculated as:

```text
Revenue = Quantity × Price
```

## Troubleshooting

- **`FileNotFoundError`**: Confirm that `sales.csv` or
  `validated_sales.csv` is in the project directory and that the terminal is
  open in that directory.
- **`ModuleNotFoundError: No module named 'openpyxl'`**: Install the dependency
  with `python -m pip install openpyxl` or `py -m pip install openpyxl`.
- **`python is not recognized`**: Install Python, enable **Add Python to PATH**
  during installation, or use the `py` command.

## Limitations

- Designed for a simple CSV structure
- Uses local files and sample sales data
- Does not connect to a live business database
- Existing generated files are overwritten when the scripts run

## Future Improvements

- Add graphical charts
- Support more input formats
- Add automated tests
