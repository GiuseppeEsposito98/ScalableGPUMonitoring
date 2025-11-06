// stress_test.cu
// Compile with: nvcc -O3 -std=c++17 -arch=sm_86 stress_test.cu -o stress_test

#include <cuda_runtime.h>
#include <cstdio>
#include <cstdlib>
#include <cmath>

#define CUDA_CHECK(call)                                                     \
    do {                                                                     \
        cudaError_t err = call;                                              \
        if (err != cudaSuccess) {                                            \
            fprintf(stderr, "CUDA error at %s:%d: %s\n", __FILE__, __LINE__, \
                    cudaGetErrorString(err));                                \
            exit(EXIT_FAILURE);                                              \
        }                                                                    \
    } while (0)

constexpr int N = 8192;               // Matrix dimension (N x N)
constexpr int TILE = 16;              // 16×16 threads per block = 256 threads
constexpr int ATOMIC_ARRAY_SIZE = 1024;
constexpr int SPECIAL_ITER = 256;    // Increased intensity
constexpr int ATOMIC_ITER = 4096;    // Increased intensity

// ------------------------------------------------------------
// Kernel 1: Simple GEMM (C = A * B)
// ------------------------------------------------------------
__global__ void __launch_bounds__(1024, 2) gemmKernel(const float* __restrict__ A,
                                                      const float* __restrict__ B,
                                                      float* __restrict__ C, int n) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    if (row >= n || col >= n) return;

    float sum = 0.0f;
    for (int k = 0; k < n; ++k) {
        sum += A[row * n + k] * B[k * n + col];
    }
    C[row * n + col] = sum;
}

// ------------------------------------------------------------
// Kernel 2: Intensive special functions (sin, exp, log)
// ------------------------------------------------------------
__global__ void __launch_bounds__(1024, 2) specialKernel(const float* __restrict__ in,
                                                         float* __restrict__ out, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n) return;

    float val = in[idx];
    #pragma unroll
    for (int i = 0; i < SPECIAL_ITER; ++i) {
        val = sinf(val);
        val = expf(val);
        val = logf(val + 1.0f);
    }
    out[idx] = val;
}

// ------------------------------------------------------------
// Kernel 3: Heavy atomic adds
// ------------------------------------------------------------
__global__ void __launch_bounds__(1024, 2) atomicKernel(float* __restrict__ atomicArray) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;
    for (int i = idx; i < ATOMIC_ARRAY_SIZE; i += stride) {
        float inc = 1.0f;
        #pragma unroll
        for (int j = 0; j < ATOMIC_ITER; ++j) {
            atomicAdd(&atomicArray[i], inc);
        }
    }
}

// ------------------------------------------------------------
// Host helper to launch all kernels in parallel streams
// ------------------------------------------------------------
int main() {
    const double testDurationSec = 10.0; // user‑defined duration

    // Allocate device memory
    float *d_A, *d_B, *d_C;
    float *d_specialIn, *d_specialOut;
    float *d_atomicArray;

    size_t matrixBytes = static_cast<size_t>(N) * N * sizeof(float);
    CUDA_CHECK(cudaMalloc(&d_A, matrixBytes));
    CUDA_CHECK(cudaMalloc(&d_B, matrixBytes));
    CUDA_CHECK(cudaMalloc(&d_C, matrixBytes));
    CUDA_CHECK(cudaMalloc(&d_specialIn, matrixBytes));
    CUDA_CHECK(cudaMalloc(&d_specialOut, matrixBytes));
    CUDA_CHECK(cudaMalloc(&d_atomicArray, ATOMIC_ARRAY_SIZE * sizeof(float)));

    // Initialize matrices with random data
    float *h_tmp = (float*)malloc(matrixBytes);
    for (size_t i = 0; i < static_cast<size_t>(N) * N; ++i) {
        h_tmp[i] = static_cast<float>(rand()) / RAND_MAX;
    }
    CUDA_CHECK(cudaMemcpy(d_A, h_tmp, matrixBytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_tmp, matrixBytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_specialIn, h_tmp, matrixBytes, cudaMemcpyHostToDevice));
    free(h_tmp);

    CUDA_CHECK(cudaMemset(d_atomicArray, 0, ATOMIC_ARRAY_SIZE * sizeof(float)));

    // Create high‑priority streams
    cudaStream_t streamGemm, streamSpecial, streamAtomic;
    CUDA_CHECK(cudaStreamCreateWithPriority(&streamGemm,    cudaStreamNonBlocking, -1));
    CUDA_CHECK(cudaStreamCreateWithPriority(&streamSpecial, cudaStreamNonBlocking, -1));
    CUDA_CHECK(cudaStreamCreateWithPriority(&streamAtomic,  cudaStreamNonBlocking, -1));

    // Kernel launch parameters
    dim3 blockDim(TILE, TILE);
    dim3 gridDim((N + blockDim.x - 1) / blockDim.x,
                 (N + blockDim.y - 1) / blockDim.y);
    dim3 specialBlock(1024);
    dim3 specialGrid((N * N + specialBlock.x - 1) / specialBlock.x);
    dim3 atomicBlock(256);
    dim3 atomicGrid((ATOMIC_ARRAY_SIZE + atomicBlock.x - 1) / atomicBlock.x);

    // Cache configuration
    CUDA_CHECK(cudaFuncSetCacheConfig(gemmKernel,    cudaFuncCachePreferL1));
    CUDA_CHECK(cudaFuncSetCacheConfig(specialKernel, cudaFuncCachePreferL1));
    CUDA_CHECK(cudaFuncSetCacheConfig(atomicKernel,  cudaFuncCachePreferL1));

    // Timing events
    cudaEvent_t startEvent, stopEvent;
    CUDA_CHECK(cudaEventCreate(&startEvent));
    CUDA_CHECK(cudaEventCreate(&stopEvent));
    CUDA_CHECK(cudaEventRecord(startEvent, streamGemm));

    while (true) {
        // Launch kernels concurrently
        gemmKernel<<<gridDim, blockDim, 0, streamGemm>>>(d_A, d_B, d_C, N);
        specialKernel<<<specialGrid, specialBlock, 0, streamSpecial>>>(d_specialIn, d_specialOut, N * N);
        atomicKernel<<<atomicGrid, atomicBlock, 0, streamAtomic>>>(d_atomicArray);

        // Non‑blocking timing check
        CUDA_CHECK(cudaEventRecord(stopEvent, 0));
        cudaError_t status = cudaEventQuery(stopEvent);
        if (status == cudaSuccess) {
            float ms = 0.0f;
            CUDA_CHECK(cudaEventElapsedTime(&ms, startEvent, stopEvent));
            if (ms / 1000.0f >= testDurationSec) break;
        }
    }

    // Ensure all work is finished before cleanup
    CUDA_CHECK(cudaDeviceSynchronize());

    // Cleanup
    CUDA_CHECK(cudaFree(d_A));
    CUDA_CHECK(cudaFree(d_B));
    CUDA_CHECK(cudaFree(d_C));
    CUDA_CHECK(cudaFree(d_specialIn));
    CUDA_CHECK(cudaFree(d_specialOut));
    CUDA_CHECK(cudaFree(d_atomicArray));

    CUDA_CHECK(cudaStreamDestroy(streamGemm));
    CUDA_CHECK(cudaStreamDestroy(streamSpecial));
    CUDA_CHECK(cudaStreamDestroy(streamAtomic));

    CUDA_CHECK(cudaEventDestroy(startEvent));
    CUDA_CHECK(cudaEventDestroy(stopEvent));

    printf("Stress test completed.\n");
    return 0;
}