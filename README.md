# mai201-assignment2-data-validation
MAI201 MLOps Assignment 2: Data Validation and Testing with Great Expectations and pytest
# MAI201 MLOps Assignment 2: Data Validation & Testing

## Project Overview

This repository contains the work for **MAI201 MLOps Assignment 2: Data Validation & Testing**.

The purpose of this assignment is to practice data validation and unit testing in an MLOps workflow. The project uses **Great Expectations** to validate a messy customer dataset and **pytest** to test data utility functions.

No machine learning model training is required for this assignment.

---

## Dataset

The dataset used in this assignment is:

```text
customer_data.csv
```

The dataset contains customer records with the following columns:

| Column        | Description                 |
| ------------- | --------------------------- |
| `customer_id` | Unique customer identifier  |
| `age`         | Customer age                |
| `email`       | Customer email address      |
| `salary`      | Annual salary               |
| `country`     | Customer country            |
| `phone`       | Customer phone number       |
| `signup_date` | Date the customer signed up |

The dataset intentionally contains data quality issues such as:

* Missing values
* Duplicate customer records
* Out-of-range ages
* Invalid email formats
* Inconsistent phone number formats
* Negative or incorrectly formatted salary values
* Invalid country values
* Invalid signup dates

---

## Project Structure

```text
mai201-assignment2-data-validation/
│
├── customer_data.csv
├── assignment2_report.md
├── requirements.txt
├── pytest.ini
├── README.md
│
├── src/
│   ├── __init__.py
│   └── data_utils.py
│
├── tests/
│   └── test_data_utils.py
│
├── validation/
│   └── run_validation.py
│
├── screenshots/
│   ├── ge_validation_results.png
│   └── pytest_results.png
│
└── great_expectations_validation_report.html
```

---

## Tools Used

This project uses the following tools:

* **Python** for scripting
* **pandas** for reading and analyzing the dataset
* **Great Expectations** for data validation
* **pytest** for unit testing
* **Git and GitHub** for version control

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/mai201-assignment2-data-validation.git
cd mai201-assignment2-data-validation
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .mlopsa2env
.mlopsa2env\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv .mlopsa2env
source .mlopsa2env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Unit Tests

The project includes pytest unit tests for the following functions:

* `load_csv(filepath)`
* `clean_phone(phone)`
* `validate_email(email)`

To run the tests:

```bash
pytest -v
```

Expected result:

```text
All tests should pass.
```

---

## Running the Data Validation

The Great Expectations validation script is located in:

```text
validation/run_validation.py
```

To run the validation:

```bash
python validation/run_validation.py
```

This script validates `customer_data.csv` using the expectation suite:

```text
customer_data_expectations
```

The validation checks include:

* `customer_id` must not be null
* `customer_id` must be unique
* `age` must be between 0 and 120
* `email` must match a valid email format
* `salary` must be present in at least 95% of rows
* `country` must be one of USA, Canada, UK, or Australia
* `signup_date` must match the expected date format
* Table row count must be between 500 and 1000

The validation output is saved as:

```text
validation_results.json
great_expectations_validation_report.html
```

---

## Data Quality Findings

The validation identified several data quality issues in the dataset, including:

* Missing customer IDs
* Invalid age values
* Invalid email formats
* Missing salary values
* Invalid country values
* Invalid signup dates
* Row count outside the expected range

The full issue counts and screenshots are documented in:

```text
assignment2_report.md
```

---

## Assignment Report

The final assignment report is available in:

```text
assignment2_report.md
```

The report includes:

* A screenshot of the Great Expectations validation results
* A list of data quality issues with counts
* A screenshot of pytest execution showing all tests passing
* A reflection on which data quality issue would most impact ML model performance

---

## Author

Chipemba Bwacha  
MAI201 MLOps  
Assignment 2: Data Validation & Testing  
