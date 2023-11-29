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

# if [ "${DJANGO_DEBUG:-off}" == "on" ]
# then
#     source /venv/bin/activate
#     python manage.py migrate
# fi

exec gunicorn --reload --workers=2 --threads=4 --worker-class=gthread \
     --log-file=- --bind 0.0.0.0:${PORT-8000} \
     --worker-tmp-dir=/dev/shm database2.wsgi
