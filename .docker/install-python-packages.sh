#!/bin/bash

# Enable part of bash "strict mode", to reduce chance of bugs (see
# http://redsymbol.net/articles/unofficial-bash-strict-mode/). You should ALWAYS
# do this when writing a bash script.
#
# -e: Exit immediately if a command has non-zero exit code, i.e. fails somehow.
#      Otherwise bash is like a Python program that just swallows exceptions.
# -u: Exit with error message if code uses an undefined environment variable,
#     instead of silently continuing with an empty string.
# -o pipefail: Like -e, except for piped commands.
set -euo pipefail

source /venv/bin/activate

pip install --no-cache-dir --upgrade pip

cd /tmp

if [ "${DEV_MODE:-0}" == "1" ]
then
    # Extract dev requirements
    pip install --no-cache-dir --no-deps -r requirements-dev.txt
else
    # Extract only prod requirements
    pip install --no-cache-dir --no-deps -r requirements.txt
fi
