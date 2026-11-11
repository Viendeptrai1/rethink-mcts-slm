def min_nop_insertions(machine_code):
    # Dictionary to store the length of each instruction
    instruction_lengths = {}
    
    # First pass: determine the length of each instruction
    i = 0
    while i < len(machine_code):
        if machine_code[i].isupper():
            instruction = machine_code[i]
            length = 1
            i += 1
            while i < len(machine_code) and machine_code[i].islower():
                length += 1
                i += 1
            instruction_lengths[instruction] = length
    
    # Second pass: calculate the number of NOPs needed
    nop_count = 0
    current_address = 0
    
    i = 0
    while i < len(machine_code):
        if machine_code[i].isupper():
            instruction = machine_code[i]
            length = instruction_lengths[instruction]
            if current_address % 4 != 0:
                nops_needed = (4 - (current_address % 4)) % 4
                nop_count += nops_needed
                current_address += nops_needed
            current_address += length
            i += length
        else:
            i += 1
    
    return nop_count

# Read input from stdin
import sys
input = sys.stdin.read().strip()

# Print the result
print(min_nop_insertions(input))