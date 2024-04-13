FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any system dependencies required for Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    cmake \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for CMAKE_ARGS
ENV CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"

# Copy the current directory contents into the container at /usr/src/app
COPY ./predictor/llm/ .

# mount volume instead of copy models
# COPY ./models/llama/llama-2-7b.Q2_K.gguf ./models/

# Install Python packages
RUN pip install --no-cache-dir llama-cpp-python
RUN pip install -r requirements.txt

EXPOSE 5000

# Command to run when starting the container
CMD ["python", "./main.py"]