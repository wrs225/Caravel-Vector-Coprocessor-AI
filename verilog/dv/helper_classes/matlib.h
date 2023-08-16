#ifndef MATRIX_OPERATIONS_H
#define MATRIX_OPERATIONS_H

#include <stdint.h>
#include "vplib.h"

void matrix_mult(float **A, float **B, float **C, int M, int K, int N) {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j += 32) { // Stepping 32 at a time for B columns
            float sum[32] = {0}; // Initialize sum array

            for (int k = 0; k < K; k++) {
                float scalarA = A[i][k];
                float vectorB[32] = {0};

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

                float product[32] = {0};
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

#endif // MATRIX_OPERATIONS_H
