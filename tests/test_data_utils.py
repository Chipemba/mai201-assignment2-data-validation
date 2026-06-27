import os
import pandas as pd
import pytest

from src.data_utils import load_csv, clean_phone, validate_email


def test_load_csv_success(tmp_path):
    """
    Test that load_csv successfully loads a valid CSV file.
    """
    file_path = tmp_path / "sample.csv"
    file_path.write_text("name,age\nAlice,30\nBob,25\n")

    df = load_csv(file_path)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["name", "age"]


def test_load_csv_file_not_found():
    """
    Test that load_csv raises FileNotFoundError for missing files.
    """
    with pytest.raises(FileNotFoundError):
        load_csv("missing_file.csv")


def test_load_csv_empty_file(tmp_path):
    """
    Test that load_csv raises ValueError for an empty file.
    """
    file_path = tmp_path / "empty.csv"
    file_path.write_text("")

    with pytest.raises(ValueError):
        load_csv(file_path)


def test_clean_phone_standard_formats():
    """
    Test clean_phone with common valid phone number formats.
    """
    assert clean_phone("(123) 456-7890") == "1234567890"
    assert clean_phone("123-456-7890") == "1234567890"
    assert clean_phone("123.456.7890") == "1234567890"
    assert clean_phone("123 456 7890") == "1234567890"


def test_clean_phone_with_country_code():
    """
    Test clean_phone removes leading country code 1.
    """
    assert clean_phone("+1 (123) 456-7890") == "1234567890"
    assert clean_phone("1-123-456-7890") == "1234567890"


def test_clean_phone_invalid_inputs():
    """
    Test clean_phone returns None for invalid inputs.
    """
    assert clean_phone(None) is None
    assert clean_phone("") is None
    assert clean_phone("abc") is None
    assert clean_phone("12345") is None
    assert clean_phone("123456789012345") is None


def test_validate_email_valid_emails():
    """
    Test validate_email returns True for valid email addresses.
    """
    assert validate_email("user@example.com") is True
    assert validate_email("first.last@example.co.uk") is True
    assert validate_email("user+test@gmail.com") is True
    assert validate_email("student_123@school.edu") is True


def test_validate_email_invalid_emails():
    """
    Test validate_email returns False for invalid email addresses.
    """
    assert validate_email("invalid-email") is False
    assert validate_email("user@") is False
    assert validate_email("@example.com") is False
    assert validate_email("user@example") is False
    assert validate_email("user example@example.com") is False


def test_validate_email_edge_cases():
    """
    Test validate_email handles empty and None values.
    """
    assert validate_email(None) is False
    assert validate_email("") is False
    assert validate_email("   ") is False