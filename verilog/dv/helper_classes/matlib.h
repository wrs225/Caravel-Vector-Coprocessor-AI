#ifndef MATRIX_OPERATIONS_H
#define MATRIX_OPERATIONS_H

#include <stdint.h>
#include "vplib.h"

void matrix_mult(float **A, float **B, float **C, int M, int K, int N) {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            float sum = 0;

            for (int chunk_start = 0; chunk_start < K; chunk_start += 32) {
                float paddedRow[32] = {0};
                float paddedColumn[32] = {0};
                float results[32] = {0};

                // Copy a chunk of row i of matrix A to paddedRow and write to VREG_0
                for (int idx = chunk_start; idx < chunk_start + 32 && idx < K; idx++) {
                    paddedRow[idx - chunk_start] = A[i][idx];
                }
                write_to_vreg(VREG_0, paddedRow);

                // Extract a chunk of column j of matrix B to paddedColumn and write to VREG_1
                for (int idx = chunk_start; idx < chunk_start + 32 && idx < K; idx++) {
                    paddedColumn[idx - chunk_start] = B[idx][j];
                }
                write_to_vreg(VREG_1, paddedColumn);

                // Multiply the vectors
                vfmul(VREG_2, VREG_0, VREG_1);

                // Read the results and add them to the current sum
                read_from_vreg(VREG_2, results);
                for (int idx = 0; idx < 32 && chunk_start + idx < K; idx++) {
                    sum += results[idx];
                }
            }

            C[i][j] = sum;
        }
    }
}

#endif // MATRIX_OPERATIONS_H
