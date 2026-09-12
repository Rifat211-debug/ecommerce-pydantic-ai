# Build the Application
FROM python:3.13-slim
WORKDIR /app

# Install backend dependencies
COPY requirements.txt .
RUN pip install --n--cache-dir -r requirements.txt

# Copy source code (backend + frontend)
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]