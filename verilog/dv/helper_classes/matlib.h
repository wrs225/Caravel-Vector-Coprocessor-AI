#ifndef MATRIX_OPERATIONS_H
#define MATRIX_OPERATIONS_H

#include <stdint.h>
#include "vplib.h"

// Define the maximum size for K
#define MAX_K 32

void matrix_mult(float A[][MAX_K], float B[][MAX_K], float C[][MAX_K], int M, int K, int N) {
    float paddedRow[MAX_K] = {0};
    float paddedColumn[MAX_K] = {0};
    float results[MAX_K] = {0};

    for (int i = 0; i < M; i++) {
        // Copy row i of matrix A to paddedRow and write to VREG_0
        for (int idx = 0; idx < K; idx++) {
            paddedRow[idx] = A[i][idx];
        }
        write_to_vreg(VREG_0, paddedRow);

        for (int j = 0; j < N; j++) {
            // Extract column j of matrix B to paddedColumn and write to VREG_1
            for (int idx = 0; idx < K; idx++) {
                paddedColumn[idx] = B[idx][j];
            }
            write_to_vreg(VREG_1, paddedColumn);

            // Multiply the vectors
            vfmul(VREG_2, VREG_0, VREG_1);

            // Read the results and sum them up to get the dot product
            float sum = 0;
            read_from_vreg(VREG_2, results);

            for (int k = 0; k < K; k++) {
                sum += results[k];
            }

            C[i][j] = sum;
        }
    }
}

#endif // MATRIX_OPERATIONS_H
