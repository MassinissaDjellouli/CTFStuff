# Use Ubuntu as the base
FROM ubuntu:24.04

# Install cross-compilation toolchain and build essentials
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gcc-aarch64-linux-gnu \
    g++-aarch64-linux-gnu \
    binutils-aarch64-linux-gnu \
    make \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /src

# Copy faketypes.c into the container
COPY faketypes.c /src/faketypes.c
COPY faketypes.h /src/faketypes.h

# Compile faketypes.c into object file for AArch64
RUN aarch64-linux-gnu-gcc -g -c faketypes.c -o faketypes.o

# By default, just keep the shell open
CMD ["sleep", "infinity"]
