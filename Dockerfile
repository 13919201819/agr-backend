FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set WORKDIR to root
WORKDIR /

COPY requirements.txt .

# Force install bcrypt here just to be 100% sure
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision ultralytics fastapi "uvicorn[standard]" gunicorn python-dotenv \
    supabase PyJWT razorpay requests opencv-python-headless bcrypt passlib[bcrypt]

# Copy your local 'app' folder into the container's root
COPY . .

EXPOSE 80

# This command looks for the 'app' folder and the 'main' file inside it
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]