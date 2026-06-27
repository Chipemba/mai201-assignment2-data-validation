import json
import re
from pathlib import Path

import pandas as pd
import great_expectations as gx


DATA_PATH = Path("customer_data.csv")
RESULTS_PATH = Path("validation_results.json")
HTML_REPORT_PATH = Path("great_expectations_validation_report.html")


def create_html_report(results_json: dict) -> None:
    """
    Create a simple HTML validation report that can be opened in a browser
    and screenshotted for the assignment report.
    """
    rows = []

    for result in results_json["results"]:
        expectation_type = result["expectation_config"]["type"]
        kwargs = result["expectation_config"]["kwargs"]
        success = result["success"]

        column = kwargs.get("column", "TABLE")
        unexpected_count = result.get("result", {}).get("unexpected_count", "N/A")
        element_count = result.get("result", {}).get("element_count", "N/A")

        status = "PASS" if success else "FAIL"

        rows.append(
            f"""
            <tr>
                <td>{expectation_type}</td>
                <td>{column}</td>
                <td>{status}</td>
                <td>{unexpected_count}</td>
                <td>{element_count}</td>
            </tr>
            """
        )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Great Expectations Validation Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            .summary {{
                margin-bottom: 20px;
                padding: 15px;
                background-color: #f8f8f8;
                border: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <h1>Great Expectations Validation Report</h1>

        <div class="summary">
            <p><strong>Expectation Suite:</strong> customer_data_expectations</p>
            <p><strong>Dataset:</strong> customer_data.csv</p>
            <p><strong>Overall Success:</strong> {results_json["success"]}</p>
            <p><strong>Total Expectations Evaluated:</strong> {len(results_json["results"])}</p>
        </div>

        <table>
            <tr>
                <th>Expectation</th>
                <th>Column</th>
                <th>Status</th>
                <th>Unexpected Count</th>
                <th>Element Count</th>
            </tr>
            {''.join(rows)}
        </table>
    </body>
    </html>
    """

    HTML_REPORT_PATH.write_text(html, encoding="utf-8")


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError("customer_data.csv was not found in the project root.")

    df = pd.read_csv(DATA_PATH)

    context = gx.get_context()

    data_source = context.data_sources.add_pandas("customer_data_source")
    data_asset = data_source.add_dataframe_asset(name="customer_data_asset")
    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "customer_data_batch"
    )

    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    suite = gx.ExpectationSuite(name="customer_data_expectations")

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(column="customer_id")
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(column="customer_id")
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="age",
            min_value=0,
            max_value=120,
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchRegex(
            column="email",
            regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="salary",
            mostly=0.95,
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="country",
            value_set=["USA", "Canada", "UK", "Australia"],
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToMatchStrftimeFormat(
            column="signup_date",
            strftime_format="%Y-%m-%d",
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=500,
            max_value=1000,
        )
    )

    # Add expectation suite to the DataContext
    try:
        context.suites.add(suite)
    except Exception:
        context.suites.delete("customer_data_expectations")
        context.suites.add(suite)

    # Create validation definition
    validation_definition = gx.ValidationDefinition(
        data=batch_definition,
        suite=suite,
        name="customer_data_validation",
    )

    # Add validation definition to the DataContext
    try:
        context.validation_definitions.add(validation_definition)
    except Exception:
        context.validation_definitions.delete("customer_data_validation")
        context.validation_definitions.add(validation_definition)

    # Run validation
    results = validation_definition.run(batch_parameters={"dataframe": df})

    results = validation_definition.run(batch_parameters={"dataframe": df})

    results_json = results.to_json_dict()

    RESULTS_PATH.write_text(json.dumps(results_json, indent=2), encoding="utf-8")
    create_html_report(results_json)

    print("Validation complete.")
    print(f"Overall success: {results_json['success']}")
    print(f"Saved JSON results to: {RESULTS_PATH}")
    print(f"Saved HTML report to: {HTML_REPORT_PATH}")


if __name__ == "__main__":
    main()