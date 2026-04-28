FROM python:3.12-slim

# Install system dependencies for OpenCV/YOLO
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set WORKDIR to root (/) so 'app.main' works as a module
WORKDIR /

COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision ultralytics fastapi "uvicorn[standard]" gunicorn python-dotenv supabase PyJWT razorpay requests opencv-python-headless

# Copy everything into the 'app' folder
COPY . /app

EXPOSE 80

# FORCE the host and port here. 
# We use 'app.main:app' because your file is in app/main.py and the object is named app.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]