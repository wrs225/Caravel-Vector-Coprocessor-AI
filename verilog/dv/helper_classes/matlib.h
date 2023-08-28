#ifndef MATRIX_OPERATIONS_H
#define MATRIX_OPERATIONS_H

#include <stdint.h>
#include <math.h>
#include <string.h>
#include "vplib.h"

void matrix_mult(float **A, float **B, float **C, int M, int K, int N) {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j += 32) { // Stepping 32 at a time for B columns
            float sum[32]; // Initialize sum array

            for (int k = 0; k < K; k++) {
                float scalarA = A[i][k];
                float vectorB[32];

                // Load the current 32 elements of B into vectorB (with padding if needed)
                for (int idx = 0; idx < 32 && (j + idx) < N; idx++) {
                    vectorB[idx] = B[k][j + idx];
                }

                // Store scalarA directly to SREG_0
                *((float*)SREG_0) = scalarA;

                // Store vectorB in a vector register (VREG_0 for simplicity)
                write_to_vreg(VREG_0, vectorB);

                // Multiply vectorB by scalarA
                vfsmul(VREG_1, VREG_0, SREG_0); // Results will be stored in VREG_1

                float product[32];
                // Read the results of the multiplication
                read_from_vreg(VREG_1, product);

                // Element-wise addition of the product to sum array
                for (int idx = 0; idx < 32 && (j + idx) < N; idx++) {
                    sum[idx] += product[idx];
                }
            }

            // Store the 32-element sum in the current column of output C
            for (int idx = 0; idx < 32 && (j + idx) < N; idx++) {
                C[i][j + idx] = sum[idx];
            }
        }
    }
}


void relu(float* input_array, float* output_array, int total_elements) {
    // Create and set the zero vector outside the loop since it's constant
    float zero_vector[32];
    write_to_vreg(VREG_1, zero_vector);

    for (int i = 0; i < total_elements; i += 32) {
        // Calculate the number of elements left
        int elements_left = total_elements - i;
        int chunk_size = (elements_left > 32) ? 32 : elements_left;

        // Buffer for the current chunk of input data
        float chunk_data[32];

        // Load the data from input_array into chunk_data without memcpy
        for (int j = 0; j < chunk_size; j++) {
            chunk_data[j] = input_array[i + j];
        }

        // Write the current chunk to the co-processor
        write_to_vreg(VREG_0, chunk_data);

        // Enable predicate register for use in comparisons
        vpset(VREG_2);

        // Set predicate if VREG_0 < VREG_1
        vpslt(VREG_2, VREG_0, VREG_1);

        // Multiply the negative elements (identified by VREG_2) of VREG_0 by zero (from VREG_1) 
        // and store the result in VREG_2
        vfmul(VREG_2, VREG_0, VREG_1);

        // Read back the results from the co-processor from VREG_2
        read_from_vreg(VREG_2, chunk_data);

        // Store the data from chunk_data into output_array without memcpy
        for (int j = 0; j < chunk_size; j++) {
            output_array[i + j] = chunk_data[j];
        }
    }
}

#endif // MATRIX_OPERATIONS_H
