#!/bin/bash

# Get the directory of the Bash script
script_dir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

# Create a virtual environment in the same directory as the script
python3 -m venv "$script_dir/env"

# Activate the virtual environement
source "$script_dir/env/bin/activate"
pip install --upgrade pip

# Install requirements from the same directory as the script
python3 -m pip install -r "$script_dir/requirements.txt"

echo "Done!"
