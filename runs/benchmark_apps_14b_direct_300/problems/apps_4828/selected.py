def min_nop_instructions(machine_code):
    # Dictionary to store the length of each instruction
    instruction_lengths = {}
    # List to store the positions of instructions
    instruction_positions = []
    
    # Parse the machine code to determine instruction lengths and positions
    i = 0
    while i < len(machine_code):
        if machine_code[i].isupper():
            instruction = machine_code[i]
            if instruction not in instruction_lengths:
                # Count the number of parameters for this instruction
                param_count = 0
                j = i + 1
                while j < len(machine_code) and machine_code[j].islower():
                    param_count += 1
                    j += 1
                instruction_lengths[instruction] = param_count + 1
            instruction_positions.append(i)
        i += 1
    
    # Calculate the number of NOPs needed
    nop_count = 0
    for position in instruction_positions:
        # Calculate the remainder when the position is divided by 4
        remainder = position % 4
        if remainder != 0:
            # We need to add NOPs to make the position divisible by 4
            nop_count += (4 - remainder)
    
    return nop_count

# Read input from standard input
import sys
input = sys.stdin.read().strip()

# Output the result
print(min_nop_instructions(input))