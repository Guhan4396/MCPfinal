#!/bin/bash

# Download and install Miniforge
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh" -O miniforge.sh
chmod +x miniforge.sh
bash ./miniforge.sh -b -p $HOME/conda

# Add conda to path
export PATH="$HOME/conda/bin:$PATH"

# Create and activate conda environment
conda create -n myenv python=3.9 -y
source $HOME/conda/bin/activate myenv

# Install Python dependencies using conda
conda install -y pandas=2.0.3 numpy=1.24.3 scikit-learn=1.3.0 -c conda-forge

# Install Node dependencies and build Next.js
pnpm install
pnpm run build 