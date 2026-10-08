import sys

def min_nops_to_align(program):
    # Dictionary to store the length of each instruction
    instruction_lengths = {}
    
    # First pass: determine the length of each instruction
    i = 0
    while i < len(program):
        if program[i].isupper():
            opcode = program[i]
            length = 1  # Start with the opcode itself
            j = i + 1
            while j < len(program) and program[j].islower():
                length += 1
                j += 1
            instruction_lengths[opcode] = length
            i = j
        else:
            i += 1
    
    # Second pass: calculate the minimum number of NOPs needed
    nops_needed = 0
    current_address = 0
    
    i = 0
    while i < len(program):
        if program[i].isupper():
            opcode = program[i]
            length = instruction_lengths[opcode]
            
            # Calculate how many NOPs are needed to align the instruction
            if current_address % 4 != 0:
                nops_needed += (4 - (current_address % 4))
                current_address += (4 - (current_address % 4))
            
            # Move to the next instruction
            current_address += length
            i += length
        else:
            i += 1
    
    return nops_needed

# Read input from standard input
program = sys.stdin.read().strip()

# Output the result
print(min_nops_to_align(program))