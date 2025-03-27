#!/bin/bash

# Exit on error
set -e

echo "Starting build process..."

# Download Miniforge (using specific version)
echo "Downloading Miniforge..."
curl -fsSL "https://github.com/conda-forge/miniforge/releases/download/23.11.0-0/Mambaforge-Linux-x86_64.sh" > miniforge.sh || {
    echo "Failed to download Miniforge"
    exit 1
}

# Verify the download
echo "Verifying download..."
if [ ! -s miniforge.sh ]; then
    echo "Downloaded file is empty"
    exit 1
fi

# Make installer executable and run it
echo "Installing Miniforge..."
chmod +x miniforge.sh
bash ./miniforge.sh -b -p $HOME/conda || {
    echo "Failed to install Miniforge"
    exit 1
}

# Add conda to path
echo "Setting up conda..."
export PATH="$HOME/conda/bin:$PATH"

# Verify conda installation
if ! command -v conda &> /dev/null; then
    echo "conda command not found after installation"
    exit 1
fi

# Install dependencies using conda
echo "Installing Python dependencies..."
conda install -y python=3.9 pandas=2.0.3 numpy=1.24.3 scikit-learn=1.3.0 -c conda-forge || {
    echo "Failed to install Python dependencies"
    exit 1
}

# Install Node dependencies
echo "Installing Node dependencies..."
pnpm install || {
    echo "Failed to install Node dependencies"
    exit 1
}

# Build Next.js
echo "Building Next.js application..."
pnpm run build || {
    echo "Failed to build Next.js application"
    exit 1
}

echo "Build process completed successfully" 