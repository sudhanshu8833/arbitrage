#!/bin/bash

# Set the virtual environment path to the present working directory
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate the virtual environment
source "${script_dir}/env/bin/activate"

python3 "${script_dir}/UI_tk.py"

