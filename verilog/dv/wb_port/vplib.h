#ifndef VREG_DEFINITIONS_H
#define VREG_DEFINITIONS_H

#define INSTRUCTION_ADDRESS 0x30000000
#define VREG_0  0x30000004
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


static inline void write_to_vreg(uint32_t vreg_address, void *values) {
    volatile uint32_t *reg = (volatile uint32_t *)vreg_address;
    uint32_t *typed_values = (uint32_t *)values;

    for (int i = 0; i < 32; i++) {
        reg[i] = typed_values[i];
    }
}

#endif