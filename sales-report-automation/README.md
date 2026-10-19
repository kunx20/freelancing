
# Sales Report Automation

A beginner-friendly Python project that validates sales data
from CSV files and generates an Excel sales report.

## Features

- Reads sales records from a CSV file
- Detects missing and invalid values
- Identifies exact duplicate records
- Calculates product revenue
- Generates a formatted Excel workbook

## Technologies

- Python
- CSV module
- OpenPyXL

## Requirements

- Python 3
- OpenPyXL

## Installation

Install the required package:

```bash
python -m pip install openpyxl
```

## How to Run

Place `sales.csv` in the project folder.

First, validate the data:

```bash
python csv_processor.py
```

Then generate the Excel report:

```bash
python sales_report.py
```

The project creates `validated_sales.csv` and
`sales_report.xlsx`.

## Sample Calculation

Revenue = Quantity × Price

## Limitations

- Designed for a simple CSV structure
- Uses sample sales data
- Does not connect to a live business database

## Future Improvements

- Add graphical charts
- Support more input formats
- Add automated tests
