#ifndef VREG_DEFINITIONS_H
#define VREG_DEFINITIONS_H

#define INSTRUCTION_ADDRESS 0x30000000
#define VREG_0  0x30000004
#define VREG_1  0x30000084
#define VREG_2  0x30000104
#define VREG_3  0x30000184
#define VREG_4  0x30000204
#define VREG_5  0x30000284
#define VREG_6  0x30000304
#define VREG_7  0x30000384
#define VREG_8  0x30000404
#define VREG_9  0x30000484
#define VREG_10 0x30000504
#define VREG_11 0x30000584
#define VREG_12 0x30000604
#define VREG_13 0x30000684
#define VREG_14 0x30000704
#define VREG_15 0x30000784
#define VREG_16 0x30000804
#define VREG_17 0x30000884
#define VREG_18 0x30000904
#define VREG_19 0x30000984
#define VREG_20 0x30000A04
#define VREG_21 0x30000A84
#define VREG_22 0x30000B04
#define VREG_23 0x30000B84
#define VREG_24 0x30000C04
#define VREG_25 0x30000C84
#define VREG_26 0x30000D04
#define VREG_27 0x30000D84
#define VREG_28 0x30000E04
#define VREG_29 0x30000E84
#define VREG_30 0x30000F04
#define VREG_31 0x30000F84

#define SREG_0  0x30001000
#define SREG_1  0x30001004
#define SREG_2  0x30001008
#define SREG_3  0x3000100C
#define SREG_4  0x30001010
#define SREG_5  0x30001014
#define SREG_6  0x30001018
#define SREG_7  0x3000101C
#define SREG_8  0x30001020
#define SREG_9  0x30001024
#define SREG_10 0x30001028
#define SREG_11 0x3000102C
#define SREG_12 0x30001030
#define SREG_13 0x30001034
#define SREG_14 0x30001038
#define SREG_15 0x3000103C
#define SREG_16 0x30001040
#define SREG_17 0x30001044
#define SREG_18 0x30001048
#define SREG_19 0x3000104C
#define SREG_20 0x30001050
#define SREG_21 0x30001054
#define SREG_22 0x30001058
#define SREG_23 0x3000105C
#define SREG_24 0x30001060
#define SREG_25 0x30001064
#define SREG_26 0x30001068
#define SREG_27 0x3000106C
#define SREG_28 0x30001070
#define SREG_29 0x30001074
#define SREG_30 0x30001078
#define SREG_31 0x3000107C



static inline void write_to_vreg(uint32_t vreg_address, void *values) {
    uint32_t *typed_values = (uint32_t *)values;

    for (int i = 0; i < 32; i++) {
        (*(volatile uint32_t *)(vreg_address + i * 4)) = typed_values[i];
    }
}

static inline void read_from_vreg(uint32_t vreg_address, void *values) {
    uint32_t *typed_values = (uint32_t *)values;

    for (int i = 0; i < 32; i++) {
        typed_values[i] = (*(volatile uint32_t *)(vreg_address + i * 4));
    }
}


static inline int compare_arrays(const void *array1, const void *array2, unsigned int size) {
    const uint8_t *bytes1 = (const uint8_t *)array1;
    const uint8_t *bytes2 = (const uint8_t *)array2;

    for (unsigned int i = 0; i < size; i++) {
        if (bytes1[i] != bytes2[i]) {
            return 0; // Return 0 if any corresponding elements are not equal
        }
    }

    return 1; // Return 1 if all corresponding elements are equal
}


static inline void addvectors(uint32_t destination_vector, uint32_t source1, uint32_t source2) {
    destination_vector = (destination_vector - VREG_0) / (32 * 4);
    source1 = (source1 - VREG_0) / (32 * 4);
    source2 = (source2 - VREG_0) / (32 * 4);

    uint32_t instruction = (0x00000002 << 27) | (destination_vector << 21) | (source1 << 16) | (source2 << 11);
    (*(volatile uint32_t *)INSTRUCTION_ADDRESS) = instruction;
}

static inline void vpset(uint32_t pdest) {
    pdest = (pdest - VREG_0) / (32 * 4);

    uint32_t instruction = (0x0000000E << 27) | (pdest << 21) | (pdest << 16);
    (*(volatile uint32_t *)INSTRUCTION_ADDRESS) = instruction;
}



#endif