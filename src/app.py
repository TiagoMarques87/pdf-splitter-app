import sys
import json
import logging
import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from datetime import datetime


# ---------------- Logging Configuration ---------------- #
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


# ---------------- Utility Functions ---------------- #
def get_current_date() -> str:
  """Return the current date in 'Mon-YYYY' format."""
  return datetime.now().strftime('%b-%Y')


def get_employees_names(json_path: Path) -> list[str]:
  """
  Load and return employee names from a JSON file.

  Args:
    json_path (Path): Path to the employees.json file.

  Returns:
    list[str]: Sorted list of employee names.

  Raises:
    FileNotFoundError: If the file does not exist.
    ValueError: If the JSON structure is invalid.
  """
  if not json_path.exists():
    raise FileNotFoundError(f'Employees file not found: {json_path}')

  with json_path.open('r', encoding='utf-8') as file:
    data = json.load(file)

  if 'employees' not in data or not isinstance(data['employees'], list):
    raise ValueError("Invalid employees.json format. Expected {'employees': [...]}")

  return sorted(data['employees'])


def split_pdf(
  file_path: Path, output_folder: Path, current_date: str, employees: list[str]
) -> None:
  """
  Split a PDF file into multiple single-page PDF files.

  Args:
    file_path (Path): Path to the input PDF file.
    output_folder (Path): Folder to save the split PDF files.
    current_date (str): The current date in 'Mon-YYYY' format.
    employees (list[str]): List of employee names.
  """
  output_folder.mkdir(parents=True, exist_ok=True)

  try:
    with file_path.open('rb') as infile:
      input_pdf = PdfReader(infile)

      if len(employees) != len(input_pdf.pages):
        raise ValueError(
          f'Mismatch: {len(input_pdf.pages)} pages vs {len(employees)} employees'
        )

      for i, page in enumerate(input_pdf.pages):
        output_pdf = PdfWriter()
        output_pdf.add_page(page)

        output_file = output_folder / f'{employees[i]}_{current_date}.pdf'
        with output_file.open('wb') as f:
          output_pdf.write(f)

        logging.info(f'Generated: {output_file}')

  except Exception as e:
    logging.error(f'❌ Error splitting PDF: {e}', exc_info=True)
    raise


# ---------------- Main Function ---------------- #
def main(input_file: str, output_folder: str, employees_file: str) -> int:
  """
  Main function to run the application.

  Args:
    input_file (str): Path to the input PDF file.
    output_folder (str): Path to the folder for output PDF files.
    employees_file (str): Path to the employees.json file.

  Returns:
    int: Exit status code (0 = success, 1 = failure).
  """
  try:
    current_date = get_current_date()
    employees = get_employees_names(Path(employees_file))
    number_employees = len(employees)

    logging.info('Welcome to the PDF Splitter Application')
    logging.info('========================================\n')
    logging.info(f'📝 Input File      : {input_file}')
    logging.info(f'📁 Output Folder   : {output_folder}')
    logging.info(f'👥 Employees Count : {number_employees}\n')
    logging.info(f'Generating {number_employees} single-page PDF files...\n')

    split_pdf(Path(input_file), Path(output_folder), current_date, employees)

    logging.info('✅ PDF files generated successfully!')
    return 0

  except Exception as e:
    logging.error(f'❌ Application failed: {e}')
    return 1


# ---------------- CLI Entry Point ---------------- #
def cli() -> None:
  """
  Entry point for console_scripts

  Args:
    None

  Returns:
    None
  """
  parser = argparse.ArgumentParser(
    prog='pdf-splitter-app',
    description='Split a PDF file into single-page files named after employees.',
  )
  parser.add_argument('input_file', help='Path to the input PDF file.', type=str)
  parser.add_argument(
    'output_folder', help='Path to the folder for output files.', type=str
  )
  parser.add_argument(
    '--employees-file',
    default='assets/employees.json',
    help='Path to the employees.json file (default: assets/employees.json).',
    type=str,
  )
  args = parser.parse_args()

  sys.exit(main(args.input_file, args.output_folder, args.employees_file))


if __name__ == '__main__':
  cli()
