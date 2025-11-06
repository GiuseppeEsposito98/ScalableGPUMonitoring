# Path to CUDA (adjust if not in default location)
CUDAPATH := /usr/local/cuda-11.6

# CUDA compiler
NVCC := $(CUDAPATH)/bin/nvcc

# Target executable
TARGET := outGPTV1

# Source file
SRC := outGPTV1.cu

# Compiler flags
NVCCFLAGS := -O3 -std=c++11 -arch=sm_86

# Default rule
all: $(TARGET)

# Build rule
$(TARGET): $(SRC)
	$(NVCC) $(NVCCFLAGS) -o $@ $<

# Clean rule
clean:
	rm -f $(TARGET)
