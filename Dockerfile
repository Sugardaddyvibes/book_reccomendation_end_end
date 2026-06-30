FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip

# Install tensorflow from local .whl file (no internet download needed)
COPY tensorflow-2.16.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl .
RUN pip install --no-cache-dir tensorflow-2.16.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl

# Install remaining packages
RUN pip install --no-cache-dir matplotlib==3.8.4 --retries 10 --timeout 180
RUN pip install --no-cache-dir jupyter==1.0.0 --retries 10 --timeout 180
RUN pip install --no-cache-dir -r requirements.txt --retries 10 --timeout 180

EXPOSE 5000

CMD ["python", "app.py"]