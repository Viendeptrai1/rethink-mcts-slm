def count_nops(machine_code):
    nops_needed = 0
    current_address = 0
    
    for char in machine_code:
        if char.isupper():
            # Check if the current address is not divisible by 4
            if current_address % 4 != 0:
                # Calculate how many NOPs are needed
                nops_needed += (4 - (current_address % 4))
                # Move the current address to the next multiple of 4
                current_address = (current_address // 4 + 1) * 4
            # Move to the next address after the instruction
            current_address += 1
        else:
            # Move to the next address after the parameter
            current_address += 1
    
    return nops_needed

# Read input from standard input
import sys
input = sys.stdin.read().strip()

# Calculate and print the result
print(count_nops(input))