# Use Ubuntu 18.04 as a base image
FROM ubuntu:18.04

# Install general tools and libraries
RUN dpkg --add-architecture i386 && apt-get update && apt-get install -y \
    build-essential \
    apt-utils \
    sudo \
    locales \
    git

#Make a incel user
RUN adduser --disabled-password --gecos '' incel && \
    usermod -aG sudo incel && \
    echo "incel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Set the locale
RUN apt-get clean && apt-get update && apt-get install -y locales && \
    locale-gen en_US.UTF-8

# Make non-interactive installation
ARG DEBIAN_FRONTEND=noninteractive

# Install necessary software to run and test python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python-autopep8 \
    python3-pytest \
    pylint

# Set aliases
RUN echo -e '#!/bin/bash\npip3 "$@"' > /usr/bin/pip && \
    chmod +x /usr/bin/pip && \
    echo -e '#!/bin/bash\npython3 "$@"' > /usr/bin/python && \
    chmod +x /usr/bin/python && \
    echo -e '#!/bin/bash\npytest-3 "$@"' > /usr/bin/pytest && \
    chmod +x /usr/bin/pytest


# Install necessary modules for python via pip
RUN pip3 install numpy scipy matplotlib pandas sympy nose

# partitioning to reduce re-build time
RUN pip3 install autopep8 pep8 pylint

# partitioning to reduce re-build time
RUN pip3 install selenium beautifulsoup4

# partitioning to reduce re-build time
RUN pip3 install requests lxml

USER incel
WORKDIR /home/incel/
