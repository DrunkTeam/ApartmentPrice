#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Upgrade pip to the latest version
pip install --upgrade pip
pip install poetry==1.8.1

if poetry install; then
    echo "Requirements installed"
else
    echo "Error installing requirements"
    exit 1
fi