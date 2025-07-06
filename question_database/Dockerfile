# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install flask sqlalchemy flask-sqlalchemy

# Expose port 5000
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
