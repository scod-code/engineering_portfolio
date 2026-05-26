FROM jenkins/jenkins:latest

USER root

# Install Python and build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv build-essential && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Create a dedicated virtual environment for Python packages
RUN python3 -m venv /opt/venv

# Make the venv the default Python environment
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade packaging tools inside the venv
RUN pip install --no-cache-dir \
    --default-timeout=1500 \
    setuptools wheel

# Install Python dependencies inside the venv
RUN pip install --no-cache-dir \
    --default-timeout=1500 \
    scikit-learn \
    ipython \
    tensorflow \
    fastapi \
    uvicorn \
    prometheus-client \
    requests \
    pydantic \
    scikit-optimize \
    optuna \
    opencv-python-headless \
    opencv-contrib-python-headless \
    torch \
    pytest  

# Allow Jenkins user to access the venv
RUN chown -R jenkins:jenkins /opt/venv

USER jenkins