# Dockerfile for virtual_mayor with NVIDIA GPU Support

Here's a Dockerfile that will allow you to run the virtual_mayor repository on Ubuntu 22.04 with NVIDIA GPU support:

```dockerfile
# Use the official NVIDIA CUDA base image with Ubuntu 22.04
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Clone the virtual_mayor repository
RUN git clone https://github.com/danindiana/virtual_mayor.git /app
WORKDIR /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install specific versions of torch with CUDA support
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Set the entrypoint (modify this based on how you want to run the application)
ENTRYPOINT ["python3"]
CMD ["app.py"]  # Replace with the appropriate main script if different
```

## Building and Running the Container

1. Build the Docker image:
```bash
docker build -t virtual-mayor .
```

2. Run the container with NVIDIA GPU support:
```bash
docker run --gpus all -it --rm virtual-mayor
```

## Notes:

1. This Dockerfile uses the official NVIDIA CUDA base image which includes all necessary CUDA runtime libraries.

2. The `--gpus all` flag is required when running the container to enable GPU access.

3. You may need to adjust:
   - The CUDA version (12.2.0 in this example) based on your GPU's compatibility
   - The entrypoint/CMD based on how the application should be launched
   - Any additional system dependencies that might be needed by the project

4. Make sure you have the NVIDIA Container Toolkit installed on your host system:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```
