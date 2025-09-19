import pytest
from pathlib import Path
from pypdf import PdfWriter
from app import get_employees_names, split_pdf, get_current_date

def test_get_employees_names_valid(tmp_path):
  """Should return sorted employee names when JSON is valid"""
  json_file = tmp_path / "employees.json"
  json_file.write_text('{"employees": ["Charlie", "Alice"]}', encoding="utf-8")

  employees = get_employees_names(json_file)
  assert employees == ["Alice", "Charlie"]


def test_get_employees_names_invalid(tmp_path):
  """Should raise ValueError when JSON is missing 'employees' key"""
  json_file = tmp_path / "employees.json"
  json_file.write_text('{"wrong_key": []}', encoding="utf-8")

  with pytest.raises(ValueError):
    get_employees_names(json_file)


def test_split_pdf_creates_expected_files(tmp_path):
  """Should create one PDF per employee with correct naming"""
  # --- Arrange ---
  employees = ["Alice", "Bob", "Charlie"]
  current_date = get_current_date()
  input_pdf = tmp_path / "input.pdf"

  # Create a dummy PDF with 3 pages
  writer = PdfWriter()
  for _ in employees:
    writer.add_blank_page(width=72, height=72)  # small blank page
  with input_pdf.open("wb") as f:
    writer.write(f)

  output_folder = tmp_path / "output"

  # --- Act ---
  split_pdf(input_pdf, output_folder, current_date, employees)

  # --- Assert ---
  generated_files = list(output_folder.glob("*.pdf"))
  assert len(generated_files) == len(employees)

  expected_filenames = {
    f"{name}_{current_date}.pdf" for name in employees
  }
  actual_filenames = {f.name for f in generated_files}

  assert expected_filenames == actual_filenames
