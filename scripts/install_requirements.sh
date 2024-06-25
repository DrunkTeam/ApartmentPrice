#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Determine the OS and activate the virtual environment accordingly
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
elif [[ "$OSTYPE" == "msys" ]]; then
    source venv/Scripts/activate
elif [[ "$OSTYPE" == "win32" ]]; then
    venv\Scripts\activate
else
    echo "Unknown OS type: $OSTYPE"
    exit 1
fi

# Upgrade pip to the latest version
pip install --upgrade pip

# Install requirements
if pip install -r requirements.txt; then
    echo "Requirements installed in virtual environment"
else
    echo "Error installing requirements"
    exit 1
fi