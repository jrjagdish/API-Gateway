# -------------------------------
# 1. Base Image
# -------------------------------
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# -------------------------------
# 2. Install system dependencies
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# 3. Install Python packages
# -------------------------------
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# -------------------------------
# 4. Copy project files
# -------------------------------
COPY . .

# -------------------------------
# 5. Expose API port
# (Render uses PORT variable automatically)
# -------------------------------
EXPOSE 8000

# -------------------------------
# 6. Run FastAPI with Gunicorn + Uvicorn worker
# -------------------------------
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
