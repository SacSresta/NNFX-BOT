# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /application

# Copy the current directory contents into the container at /application
COPY . /application

# Update the package list and install dependencies for TA_Lib and awscli
RUN apt-get update -y && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev \
    libssl-dev \
    libatlas-base-dev \
    wget \
    awscli

# Install TA_Lib from source
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run application.py when the container launches
CMD ["python3", "app.py"]
