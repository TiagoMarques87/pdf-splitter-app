![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white) ![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white) ![docker compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![github actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

[![Build and Push Docker Image](https://github.com/TiagoMarques87/pdf-splitter-app/actions/workflows/build.yaml/badge.svg?branch=master)](https://github.com/TiagoMarques87/pdf-splitter-app/actions/workflows/build.yaml)

# PDF Splitter Application

`PDF Splitter App` is a simple command-line tool that splits a multi-page PDF into individual single-page PDFs and names each file after an employee. It’s designed for teams or organizations that generate bulk reports, pay slips, or other employee-specific documents and need them separated automatically.

The app is built in Python, packaged for easy installation, fully tested with pytest, and containerized with Docker so it can run consistently across different environments.

![Diagram](./images/diagram.png)

## 🛠️ Pre-requisites

The following tools are required:

- Python 3
- Docker
- Github CLI (gh)

For Mac, use [brew](https://formulae.brew.sh):

```bash
brew install python3
brew install docker
brew install gh
```

## 📦 Installation (local)

1. Clone the repo:

```bash
gh repo clone TiagoMarques87/pdf-splitter-app
```

2. Change to the repo directory:

```bash
cd pdf-splitter-app
```

## 🐍 Run with Python

1. Create a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

2. Install dependencies in editable mode:

```bash
pip install -e .
```

3. Run the application:

```bash
pdf-splitter-app <input_file> <output_dir> --employees-file <employees_file>
```

where:

- `<input_file>` is the path to the PDF file to be splitted.
- `<output_dir>` is the path to the directory where the splitted PDF files will be stored.
- *(optional)* `<employees_file>` is the path to a JSON file that contains the employees names. If no file is set the default value will point to [employees.json](./assets/employees.json).

Example:

```bash
pdf-splitter-app ~/Downloads/employess_payslip.pdf ~/Documents/payslip_output
```

1. Deactivate the virtual environment:

```bash
deactivate
```

To learn more on python read the official documentation. [Learn more](https://docs.python.org/3/)

## 🐳 Run with Docker

1. In the root of the repo, create a similar `.env` file:

```txt
# Path to input PDF file
INPUT_FILE=<path-to-input-file>

# Path to output directory
OUTPUT_DIR=<path-to-output-directory>
```

2. Build the Docker image:

```docker
docker compose build
```

3. Run the Docker container:

```docker
docker compose run --rm pdf-splitter input_file.pdf outputs
```

**Note:** Please be aware that, by default, the [employees.json](./assets/employees.json) file will be used. Ensure that you have updated it to fit your needs.

To learn more on Docker read the official documentation. [Learn more](https://docs.docker.com).

## 🧪 Tests (PyTest)

1. Install dev dependencies in editable mode:

```bash
pip install -e '.[dev]'
```

2. Run the tests:

```bash
pytest -v
```

To run a specific test, for example, the `test_split_pdf_creates_expected_files`:

```bash
pytest tests/test_app.py::test_split_pdf_creates_expected_files -v
```

To learn more on pytest read the official documentation. [Learn more](https://docs.pytest.org/en/stable/).

## 🧹 Linter (Ruff)

1. Check for errors:

```bash
ruff check
```

**Note:** To automatically fix solvable errors use the *`--fix`* flag.

2. Format the code:

```bash
ruff format
```

**Note:** To get a preview of what will be formated use the *`--diff`* flag.

To learn more on Ruff read the official documentation. [Learn more](https://docs.astral.sh/ruff/).

## 🔁 CI/CD (GitHub Actions)

This project uses GitHub Actions to build and publish Docker images to [GitHub Container Registry (GHCR)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

On every `push` to **master**, a new image is built and pushed with the tag latest.

You can also run the workflow `manually` and provide a custom tag (e.g. v1.0.0, dev).

Image location:

```bash
ghcr.io/tiagomarques87/pdf-splitter-app:<TAG>
```

Example

```bash
ghcr.io/tiagomarques87/pdf-splitter-app:latest
ghcr.io/tiagomarques87/pdf-splitter-app:v1.0.0
```

To learn more on GitHub Actions read the official documentation. [Learn more](https://docs.github.com/en/actions).
