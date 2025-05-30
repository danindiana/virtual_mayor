To ensure the **virtual_mayor** repository runs smoothly in Docker with NVIDIA GPU support, we need to address a few additional steps. Here's a complete guide:

---

### **1. Verify NVIDIA Drivers & CUDA on Host**
Before running the container, ensure your **Ubuntu 22.04 host** has:
- **NVIDIA drivers** installed (`nvidia-smi` should work).
- **Docker** with **NVIDIA Container Toolkit** (for `--gpus all` support).

#### **Check GPU & Drivers**
```bash
nvidia-smi
```
If this fails, install drivers:
```bash
sudo ubuntu-drivers autoinstall
sudo reboot
```

#### **Install NVIDIA Container Toolkit**
```bash
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

---

### **2. Update the Dockerfile for Missing Dependencies**
The repository may need additional packages. Here's an **updated Dockerfile**:

```dockerfile
# Use NVIDIA CUDA base image
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    portaudio19-dev \  # For audio support (if needed)
    && rm -rf /var/lib/apt/lists/*

# Clone the repo
RUN git clone https://github.com/danindiana/virtual_mayor.git /app
WORKDIR /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA 12.1
RUN pip3 install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install additional audio libraries (if needed)
RUN pip3 install --no-cache-dir pyaudio

# Set entrypoint (modify based on main script)
ENTRYPOINT ["python3"]
CMD ["app.py"]  # Replace with the correct script if different
```

---

### **3. Build & Run the Container**
#### **Build:**
```bash
docker build -t virtual-mayor .
```

#### **Run with GPU & Port Forwarding (if web app):**
```bash
docker run --gpus all -it --rm -p 5000:5000 virtual-mayor
```
- `--gpus all` → Enables GPU access.
- `-p 5000:5000` → Only needed if running a web server.

---

### **4. Debugging Common Issues**
#### **Issue: CUDA not detected**
- **Fix:** Ensure `nvidia-smi` works on the host and the correct CUDA version is used in the Dockerfile.

#### **Issue: Missing Python dependencies**
- **Fix:** Check `requirements.txt` and manually install missing packages in the Dockerfile.

#### **Issue: Audio not working**
- **Fix:** Add `--device /dev/snd` to the `docker run` command if audio is needed.

---

### **5. Final Checks**
- ✅ `nvidia-smi` works on the host.
- ✅ Docker is installed (`docker --version`).
- ✅ NVIDIA Container Toolkit is installed (`nvidia-ctk --version`).
- ✅ The correct `CMD` in Dockerfile matches the main script (`app.py` or similar).

---

### **Summary**
1. **Host Setup**: NVIDIA drivers + Docker + NVIDIA Container Toolkit.
2. **Dockerfile**: Includes CUDA, Python, and project dependencies.
3. **Run**: `docker run --gpus all` with optional port forwarding.

If you encounter issues, check:
- The project’s `README.md` for extra setup steps.
- Logs (`docker logs <container_id>`) for missing dependencies.
