FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# This sets the PYTHONPATH so that 'from app.api' works 
# even if you are already inside the app folder
ENV PYTHONPATH=/

RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision ultralytics fastapi "uvicorn[standard]" gunicorn python-dotenv supabase PyJWT razorpay requests opencv-python-headless

EXPOSE 80

# We use 0.0.0.0 to make it reachable externally
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]