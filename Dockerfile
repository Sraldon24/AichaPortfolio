# Use an official Python runtime as a parent image
FROM python:3.13.1-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Install node dependencies and build CSS (if package.json exists, otherwise skip)
# We handle this conditionally or ensure package.json is created before build
RUN if [ -f package.json ]; then npm install && npm run build:css; fi

# Expose port
EXPOSE 8000

# Default command
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --config gunicorn.conf.py --bind 0.0.0.0:8000 portfolio_core.wsgi:application"]
