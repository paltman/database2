# syntax = docker/dockerfile:1.3

# Transient Python Build Image
# ------------------------------------------------------------------------------
# Build up the Python dependencies
FROM python:3.12-slim-bookworm as python-build

ARG DEV_MODE

COPY .docker/install-system-packages.sh /tmp
RUN /tmp/install-system-packages.sh \
    apt-utils \
    build-essential \
    libpq-dev \
    git

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH VIRTUAL_ENV=/venv DEV_MODE=$DEV_MODE

RUN mkdir /app
WORKDIR /app

COPY .docker/install-python-packages.sh /tmp
COPY requirements.txt /tmp
COPY requirements-dev.txt /tmp
RUN /tmp/install-python-packages.sh


# Collect Built Static
# ------------------------------------------------------------------------------
# run collectstatic
FROM python:3.12-slim-bookworm as collectstatic-build

ARG DEV_MODE DATABASE_URL
ENV PATH=/venv/bin:$PATH DEV_MODE=$DEV_MODE DATABASE_URL=$DATABASE_URL

RUN mkdir /app
WORKDIR /app

# Install packages required for run management commands
# > libpq5 - postgres drivers
COPY .docker/install-system-packages.sh /tmp
RUN /tmp/install-system-packages.sh libpq5

COPY . .
COPY --from=python-build /venv /venv

ENV PATH=/venv/bin:$PATH VIRTUAL_ENV=/venv
RUN /venv/bin/python manage.py collectstatic --no-input


# Run Image
# ------------------------------------------------------------------------------
# The final image that is used to execute everything
FROM python:3.12-slim-bookworm as run-stage

ARG GITHUB_SHA
ARG DEV_MODE
ARG CODECOV_TOKEN
ENV PATH=/venv/bin:$PATH DEV_MODE=$DEV_MODE CODECOV_TOKEN=$CODECOV_TOKEN
ENV GITHUB_SHA=$GITHUB_SHA

RUN useradd --create-home database2
WORKDIR /home/database2

# Install packages required for run time
# > libpq5 - postgres drivers
# > libcairo2 libpango-1.0-0 libpangocairo-1.0 - locale tools
# > gettext - translations support
COPY .docker/install-system-packages.sh /tmp
RUN /tmp/install-system-packages.sh libpq5 libcairo2 libpango-1.0-0 libpangocairo-1.0 gettext tini

USER database2

# Copy over the code, virtualenv, and collected static changing it to be owned by our new user:
COPY --chown=database2:database2 . /home/database2
COPY --from=python-build --chown=database2:database2 /venv /venv
COPY --from=collectstatic-build --chown=database2:database2 /app/static /home/database2/static

# When Docker image is stopped, send a SIGINT (KeyboardInterrupt exception by
# default in Python) instead of SIGTERM. Really you should listen for SIGTERM,
# but not all programs do (see https://hynek.me/articles/docker-signals/).
STOPSIGNAL SIGINT

# If the program crashes, try to record a Python traceback (see
# https://docs.python.org/3/library/faulthandler.html).
ENV PYTHONFAULTHANDLER=true

ENV PYTHONDONTWRITEBYTECODE=1

ENV PATH=/venv/bin:$PATH VIRTUAL_ENV=/venv

EXPOSE 8000

# Entrypoint that handles signals correctly (see
# https://hynek.me/articles/docker-signals/ for details):
# 1. With tini as init script.
# 2. Use [] syntax so it doesn't get wrapped with "/bin/sh -c" that screws up
#    signal delivery.
# 3. "-g" kills all processes when the container is told to shut down, instead
#    of just the parent process. For details se
#     https://github.com/krallin/tini#process-group-killing
COPY .docker/entrypoint.sh /venv/bin
ENTRYPOINT ["/usr/bin/tini", "-g", "-s", "--"]

# By default run entrypoint.sh, if other arguments are given run those instead:
CMD ["/venv/bin/entrypoint.sh"]
