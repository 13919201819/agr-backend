FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set WORKDIR to the root of the container
WORKDIR /

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies including the missing bcrypt
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision ultralytics fastapi "uvicorn[standard]" gunicorn python-dotenv \
    supabase PyJWT razorpay requests opencv-python-headless bcrypt passlib[bcrypt]

# Copy your entire local folder into a folder named /app in the container
# This makes your structure /app/main.py, /app/api, etc.
COPY . /app

EXPOSE 80

# This ensures that when uvicorn looks for "app.main", 
# it finds the /app folder we just created.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]