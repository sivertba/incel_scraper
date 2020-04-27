# Use Ubuntu 18.04 as a base image
FROM ubuntu:18.04

#Make a HYPSO user
RUN adduser --disabled-password --gecos '' hypso && \
    usermod -aG sudo hypso && \
    echo "hypso ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set the locale
RUN apt-get clean && apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8

# Install necessary software to run and test python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python-autopep8 \
    python3-pytest
#    pylint

# Set aliases
RUN echo -e '#!/bin/bash\npip3 "$@"' > /usr/bin/pip && \
    chmod +x /usr/bin/pip && \
    echo -e '#!/bin/bash\npython3 "$@"' > /usr/bin/python && \
    chmod +x /usr/bin/python && \
    echo -e '#!/bin/bash\npytest-3 "$@"' > /usr/bin/pytest && \
    chmod +x /usr/bin/pytest


# Install necessary modules for python via pip
RUN pip install numpy scipy matplotlib pandas sympy nose


USER hypso
WORKDIR /home/hypso/
