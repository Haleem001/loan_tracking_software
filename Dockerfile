FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY loan_tracker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY loan_tracker/ /app/loan_tracker/

# Set environment variables
ENV PYTHON_VERSION=3.12.0

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "loan_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
