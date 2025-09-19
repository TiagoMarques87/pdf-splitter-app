# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY pyproject.toml .
COPY src ./src
COPY assets ./assets

# Install the app in editable mode
RUN pip install -e .

# Default command: show help
CMD ["--help"]