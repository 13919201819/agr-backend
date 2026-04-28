# Step 1: Use a small Python base
FROM python:3.12-slim

# Step 2: Install system libraries for OpenCV/YOLO
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set WORKDIR to root (/) NOT (/app)
WORKDIR /

# Step 4: Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision ultralytics fastapi uvicorn[standard] gunicorn python-dotenv supabase PyJWT razorpay requests opencv-python-headless

# Step 5: Copy your whole project into a folder named 'app'
# This creates the structure /app/main.py and /app/api/
COPY . /app

# Step 6: Expose port 80
EXPOSE 80

# Step 7: Start the server
# By running from /, 'app.main:app' will correctly find the /app folder
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:80"]