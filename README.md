# Vector Extension to Caravel Management SoC
Written for the EFabless AI Chip competition, this project adds basic vector instructions to the Caravel Management SoC.

All code, besides file paths are written using ChatGPT. This includes test cases, C libraries, blocks, etc. In our project, GPT4 served as a pair programmer which followed the instructions of a human that was aware of what the microarchitecture would look like.

All Prompts used to generate code are included in this repository. The prompts within a file may not be in the order we asked ChatGPT. As we would find bugs, we would go back to previous prompts and fix the implementation within those prompts. However, the files are separated by block and topic. We have found it is difficult to do complex things within a single, long prompt, as GPT4 reaches its token limit and forgets how to do things.

## Features
- [x] Integer Operations
- [x] (almost*) IEEE-754 compliant floating point adder and multiplier
- [x] Bitwise logical operations
- [x] Scalar instructions
- [x] 6 vector registers, each being 32 elements and 32 bits. Directly acessable over wishbone interface.
- [x] 6 scalar registers, each being 32 bits. Directly acessable over wishbone interface.
- [x] Predicate Instructions for vectored-conditionals
- [x] C-Library for wrapping wishbone loads/stores
- [x] Basic Machine Learning Library

*Our implementation has slightly different rounding logic, so your results may vary.

# ISA and Register Mapping 

The instructions supported on the processor are included in the table below. We had GPT4 generate an initial draft of the instructions, then we changed them as needed for our implementaton to make sense. Any of these instrucitons can be run by sending the instruciton over the wishbone address 0x30000000. The only exception to these instructions are the load/store instrucitons. Where instead writing to a vector or scalar register via sending a load/store instruciton over 0x30000000, you can just write or read from memory addresses: 
0x30000004 -> 0x30000380 for vector registers
0x30001000 -> 0x30001018 for scalar registers

Additionally, for predicate register instrucitons you do not need to actually set Ssrc to anything meaningful, as each element in the destination predicate register will have values written to it for anything valuable. It is reccomended you use the C library ```vplib``` to interact with the processor, as this abstracts away the low-level register reads and writes you would need to do.

## ISA

This ISA was written by GPT4. As stated above, VLOAD and VSTORE are memory-mapped using the wishbone bus. Additionally, the ```Ssrc``` register in the ```VPSET``` instruction can be assigned any arbitrary value, as the predicate registers for each index of the vector will always be 1. 

| Instruction	| Opcode	| Operand 1	    | Operand 2	   | Operand 3	| Description |
| ------------- | --------- | ------------- | ------------ | ---------- | ----------- |                                                                                     
| VLOAD	        | 0x00	    | Vdest	        | Saddr	       | Slen	    | Load a vector from memory into Vdest. The base address is in Saddr, and the length is in Slen.|
| VSTORE	    | 0x01	    | Vsrc	        | Saddr	       | Slen	    | Store a vector from Vsrc to memory. The base address is in Saddr, and the length is in Slen.|
| VADD	        | 0x02	    | Vdest	        | Vsrc1	       | Vsrc2	    | Add two vectors element-wise. Vsrc1 + Vsrc2 -> Vdest.|
| VSUB	        | 0x03	    | Vdest	        | Vsrc1	       | Vsrc2	    | Subtract two vectors element-wise. Vsrc1 - Vsrc2 -> Vdest.|
| VMUL	        | 0x04	    | Vdest	        | Vsrc1	       | Vsrc2	    | Multiply two vectors element-wise. Vsrc1 * Vsrc2 -> Vdest.|
| VSMUL	        | 0x05	    | Vdest	        | Vsrc	       | Ssrc	    | Multiply a vector by a scalar. Vsrc * Ssrc -> Vdest.|
| VSADD	        | 0x06	    | Vdest	        | Vsrc	       | Ssrc	    | Add a scalar to a vector. Vsrc + Ssrc -> Vdest.|
| VFADD	        | 0x07	    | Vdest	        | Vsrc1	       | Vsrc2	    | Add two floating-point vectors element-wise. Vsrc1 + Vsrc2 -> Vdest.|
| VFMUL	        | 0x08	    | Vdest	        | Vsrc1	       | Vsrc2	    | Multiply two floating-point vectors element-wise. Vsrc1 * Vsrc2 -> Vdest.|
| VFSMUL	    | 0x15	    | Vdest	        | Vsrc	       | Ssrc	    | Multiply a floating-point vector by a scalar. Vsrc * Ssrc -> Vdest.|
| VFSADD	    | 0x16	    | Vdest	        | Vsrc	       | Ssrc	    | Add a scalar to a floating-point vector. Vsrc + Ssrc -> Vdest.|
| VAND	        | 0x09	    | Vdest	        | Vsrc1	       | Vsrc2	    | Perform bitwise AND operation on two integer vectors. Vsrc1 AND Vsrc2 -> Vdest.|
| VOR	        | 0x0A	    | Vdest	        | Vsrc1	       | Vsrc2	    | Perform bitwise OR operation on two integer vectors. Vsrc1 OR Vsrc2 -> Vdest.|
| VXOR	        | 0x0B	    | Vdest	        | Vsrc1	       | Vsrc2	    | Perform bitwise XOR operation on two integer vectors. Vsrc1 XOR Vsrc2 -> Vdest.|
| VPSETZ	    | 0x0C	    | Pdest	        | Ssrc	       | -	        | Set predicate register Pdest to 1 for each element in Ssrc that is zero, and 0 otherwise.|
| VPSETN	    | 0x0D	    | Pdest	        | Ssrc	       | -	        | Set predicate register Pdest to 1 for each element in Ssrc that is non-zero, and 0 otherwise.|
| VPSET	        | 0x0E	    | Pdest	        | Ssrc	       | -	        | Set predicate register Pdest to 1 for each element in Ssrc.|
| VPSGE	        | 0x0F	    | Pdest	        | Ssrc1	       | Ssrc2	    | Set predicate register Pdest to 1 for each element in Ssrc1 that is signed greater than or equal to the corresponding element in Ssrc2, and 0 otherwise. |
| VPSLT	        | 0x18	    | Pdest	        | Ssrc1	       | Ssrc2	    | Set predicate register Pdest to 1 for each element in Ssrc1 that is signed less than the corresponding element in Ssrc2, and 0 otherwise.|
| VPUGE	        | 0x19	    | Pdest	        | Ssrc1	       | Ssrc2	    | Set predicate register Pdest to 1 for each element in Ssrc1 that is unsigned greater than or equal to the corresponding element in Ssrc2, and 0 otherwise.|
| VPULT	        | 0x1A	    | Pdest	        | Ssrc1	       | Ssrc2	    | Set predicate register Pdest to 1 for each element in Ssrc1 that is unsigned less than the corresponding element in Ssrc2, and 0 otherwise.|
| VFSUB	        | 0x10	    | Vdest	        | Vsrc1	       | Vsrc2	    | Subtract two floating-point vectors element-wise. Vsrc1 - Vsrc2 -> Vdest.|
| VPEQ	        | 0x14	    | Pdest	        | Psrc1	       | Psrc2	    | Set predicate register Pdest to 1 if Psrc1 is equal to Psrc2, and 0 otherwise.|
| VPNEQ	        | 0x17	    | Pdest	        | Psrc1	       | Psrc2	    | Set predicate register Pdest to 1 if Psrc1 is not equal to Psrc2, and 0 otherwise.|


## Register Mapping

As stated above, the addresses of the memory mapped registers are as follows:
```
#define INSTRUCTION_ADDRESS 0x30000000
#define VREG_0  0x30000004
#define VREG_1  0x30000084
#define VREG_2  0x30000104
#define VREG_3  0x30000184
#define VREG_4  0x30000204
#define VREG_5  0x30000284
#define VREG_6  0x30000304


#define SREG_0  0x30001000
#define SREG_1  0x30001004
#define SREG_2  0x30001008
#define SREG_3  0x3000100C
#define SREG_4  0x30001010
#define SREG_5  0x30001014
#define SREG_6  0x30001018
```
The stride between each VREG register is 32 * 4 bytes. The following 32 addresses after a VREG register are individual elements of the vector. This makes the vector register file to appear as memory acessable to the management core. 

Each register is dynamically typed, meaning you can store and conduct operations on signed/unsigned integers, booleans, and 32-bit floating point datatypes. 

Writing an instruction to ```INSTRUCTION_ADDRESS``` will send an instruction to the processor for execution.

# C++ Library

# Microarchitecture
## Top
The block diagram of the processor core is shown below. The microarchitecture was designed by a human and GPT4. GPT4 primarily described the functionality some of the blocks, while a human drew out the block diagram on pencil and paper. The architecture was designed to be as simple as possible, so an AI can feasibly implement it. The Control can be upgraded easily to support more advanced features such as chimes and scheduling. A counter is used to increment the register file addresses so the operations can be done on a vector of registers. Additional logic was added as a kludge to allow for dynamic reading/writing from the wishbone bus. Additionally, each queue can be assumed to be latency insensitive. 
![Block Diagram for Microarchitecture](img/VectorArchv1DiagramPretty.png)

##
# Testing Strategy

# Phyiscal Design 

# Performance

# Learnings
