FROM python:3.12-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set WORKDIR to root so 'app.main' is discoverable as a module
WORKDIR /

COPY requirements.txt .

# Install with --no-cache-dir to keep the image slim
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision ultralytics fastapi uvicorn[standard] gunicorn python-dotenv supabase PyJWT razorpay requests opencv-python-headless

# Copy your local folder into a folder named /app inside the container
COPY . /app

EXPOSE 80

# Run using the module path
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:80"]