FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# set work directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 1. Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the rest of the application
COPY . .

# 3. Install the current project in editable mode
RUN pip install --no-cache-dir -e .

EXPOSE 5000

CMD [ "python" , "app.py" ]