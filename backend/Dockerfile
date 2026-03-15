FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /app/uploads /app/logs

ENV PYTHONUNBUFFERED=1

# Azure Container Apps will route to whatever you set as targetPort (often 5000),
# but binding to $PORT is safest.
EXPOSE 5000

# Use gunicorn and bind on all interfaces. Uses PORT if provided by platform.
CMD ["sh", "-lc", "gunicorn -b 0.0.0.0:${PORT:-5000} app:app"]
