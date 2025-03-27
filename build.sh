#!/bin/bash

# Install Python dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install Node dependencies and build Next.js
pnpm install
pnpm run build 