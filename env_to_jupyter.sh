#! /bin/bash

# Get the directory of the Bash script
script_dir=$(dirname -- "$(readlink -f -- "$BASH_SOURCE")")

# Check if the virtual environment exists
if [ ! -d "$script_dir/env" ]; then
    echo "Virtual environment not found in $script_dir/env. Please create the virtual environment first."
    exit 1
fi

# Activate the virtual environement
source "$script_dir/env/bin/activate"

# Install IPython kernel within the virtual environment
python -m ipykernel install --user --name=env
