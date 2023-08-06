# Vector Extension to Caravel Management SoC
Written for the EFabless AI Chip competition, this project adds vector instructions to the Caravel Management SoC.

All code, besides one line of verilog and file paths are written using ChatGPT. This includes test cases, C libraries, blocks, etc. 

All Prompts used to generate code are included in this repository. The prompts within a file may not be in the order we asked ChatGPT. As we would find bugs, we would go back to previous prompts and fix the implementation within those prompts. However, the files are separated by block and topic. We have found it is difficult to do complex things within a single, long prompt, as GPT4 reaches its token limit and forgets how to do things.

# Features
- [x] Integer Operations
- [x] (almost*) IEEE-754 compliant floating point adder and multiplier
- [x] Bitwise logical operations
- [ ] Scalar instructions
- [x] Register files directly accessable through wishbone interface
- [ ] Predicate Instructions for vectored-conditionals
- [ ] C-Library for wrapping Wishbone calls
- [x] Tested using randomized UVM

# Nice to Add in the Future if We Have Time
- [ ] Support for Chimes 


# Instruction Set

# Register Mapping

# C++ Library

# Microarchitecture

# Testing Strategy

# Performance

# Learnings