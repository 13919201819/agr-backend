# Step 1: Use a small Python base
FROM python:3.11-slim

# Step 2: Install system libraries for OpenCV/YOLO
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Step 3: Install Python dependencies (CPU-optimized)
COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision ultralytics fastapi uvicorn gunicorn

# Step 4: Copy your code
COPY . .

# Step 5: Start the server on Port 80
EXPOSE 80
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:80"]