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
- [x] Basic Machine Learning Library(You need to provide the )

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

# C Library
Header files are provided to interface with the vector operations as well as basic machine learning functionality. These files were also generated by GPT4. ```vplib.h``` contains macros for the VREG and SREG addresses. It also provides functions that abstract away writing to these addresses directly and functions to call each of the instructions in the ISA. A test bench is also provided to verify the functionality of vector addition.

```matlib.h``` provides functions to compute matrix multiplications and the Rectified Linear Unit (ReLU) commonly used in machine learning applications. Due to the gcc configuration used for verification which does not support float operations, we were unable to test these functions.

# Microarchitecture
## Top
The block diagram of the processor core is shown below. The microarchitecture was designed by a human and GPT4. GPT4 primarily described the functionality some of the blocks, while a human drew out the block diagram on pencil and paper. The architecture was designed to be as simple as possible, so an AI can feasibly implement it. 

The Control can be upgraded easily to support more advanced features such as chimes and scheduling. A counter is used to increment the register file addresses so the operations can be done on a vector of registers. 

Additional logic was added as a kludge to allow for dynamic reading/writing from the wishbone bus. 

Each address line piped into an AND gate is assumed to be an address comparison. Additionally, each queue can be assumed to be latency insensitive. Each blue wire can be assumed to come from the control unit.

They say pictures are worth 1000 words, so a copy of the block diagram is included below.

![Block Diagram for Microarchitecture](img/VectorArchv1DiagramPretty.png)

## Wishbone Converter
Besides top, GPT4 also designed a wishbone to latency insensitive converter. This block is responsible for regulating wishbone transactions between the bus and our latency insensitive interfaces. 

If a valid register address is sent to the converter via wishbone, it will copy the corresponding load or store instruction over to the instruction queue and send the address/data to the load queue. If the instruction is a store, it will wait for the data to come back through the store queue.

If the transaction is sent to the ```INSTRUCTION_ADDRESS```, the transaction will be sent over to the instruction queue. 

## Control Unit. 
Currently, the control unit is based on a decoder which simpy decodes an instruction. In the future, the control's implementation can be changed to support multi-instruction caravans. 

# Testing Strategy
We use [Pymtl 3](https://github.com/pymtl/pymtl3) to validate the functionality of our design. To do this, we first must construct a Python wrapper class for each Verilog module. Then, Python unit test functions can be written and run with [pytest](https://docs.pytest.org/en/7.4.x/). We use GPT4 to generate these Python test files, which cover the expected functionality for each operation as well as edge cases. Prompts for each module can be found in the prompts_tests directory.

# Phyiscal Design 
Before pushing the design through the OpenLane flow, we pushed the SystemVerilog through sv2v. We then used ChatGPT to make any required modifications to the Verilog such as adding power pins.

We originally decided to make our vector register file contain 32 vector and scalar registers. However, after trying to push it through OpenLane we quickly discovered that having 4Kb of registers was far too large for the tools. Thus we scaled our design to only have 6 vector and scalar registers. 

We tried making macros for both the vector and scalar register files, but we encountered issues with the tool when running LVS. There seemed to be an issue with connecting power to macros that are on lower levels on the top layer of the hierarchy. Instead of dealing with the problem further, we just decided to push the design through the flow flat. 

We also encountered an issue with Verilog sv2v generated for the fp_addsub unit which caused Yosys to hang and run forever, eating an infinite amount of memory. ChatGPT was able to fix this and and the resulting logic passed all test cases.

The design also failed to meet timing for a clock period of 25ns with a slack of about -4.1ns. If you run the design at 30ns it should be fine. We tried pushing the design through at 20ns, but for some reason the tool insisted on a 25ns lcock period. 

# Learnings
When working on this project, we learned a lot about the performance of ChatGPT when generating hardware. Originally, we tried to create a SHA-256 hardware accelerator with clever prompt engineering, but we quickly found that ChatGPT struggled to create a complex block from scratch. Thus, we demoted it to junior engineer and decided on a more holistic approach to hardware generation. Will read *Computer Architecture: A Quantitative Approach* over the summer to brush up on his comparch skills, and was inspired by the vector processor. He wanted to implement a vector processor for the Caravel that can be used in conjunction with the management SoC. It was from our experience with this project that we learned the following:

Don't expect ChatGPT to do everything for you. You, as the designer, should have some idea of the hardware you would like to generate. Otherwise ChatGPT will make a bunch of mistakes and write suboptimal code. We tried having ChatGPT make a SHA-256 accelerator from single prompts, but it ended up being a disaster. For less generic hardware such as the decoder or wishbone converter, we needed to take a more manual approach and prompt chatgpt more precisely. For things like register files, it was easier because ChatGPT may have seen similar source code in its training.

Use a different method for testing your Verilog than iverilog. We decided to use PyMTL3 to test our design and it was very fruitful. Because ChatGPT is better at generating Python than Verilog, it became trivially easy to use GPT4 to generate test cases for our design. This allowed us to have a feedback loop of generating test cases alongside hardware to verify its functionality. This enabled us to generate a larger project in a shorter amount of time.

The management SoC does not support floating point instructions. We thought there was an FPU implemented on the Management Core, but it turns out that was not synthesized. If you want to use the floating-point portions of this project, you will need to add an additional C library to compile floating point instructions in software



Copyright 2023 William Salcedo & Courtney McBeth
