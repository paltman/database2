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

# Next, install Debian/Ubuntu packages specified on the command-line. We
# can't use Python because it may not be installed at this point!# CHANGEME:
# If you want to add PPAs and the like, this is a good place to add these.

# Disable interactive use by the Debian installer:
export DEBIAN_FRONTEND=noninteractive

# Update package cache and upgrade all packages to ensure we have latest
# packages.
apt-get update
apt-get upgrade --yes

# Use --no-install-recommends so we only install packages we actually need.
apt-get install --yes --no-install-recommends "$@"

# Install tools for test/dev
if [ "${DEV_MODE:-0}" == "1" ]
then
  apt-get install --yes --no-install-recommends curl git
  curl -v -O https://uploader.codecov.io/latest/linux/codecov
  chmod +x codecov
fi

# Clear the various apt caches once the packages are installed, just to save
# a little disk space. We do this in same Dockerfile line so that there are
# no intermediate layes where the cached files will still exist.
apt-get clean
rm -rf /var/lib/apt/lists/*
