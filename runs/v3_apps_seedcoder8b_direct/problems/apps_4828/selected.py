def min_nop_instructions(machine_code):
    # Initialize the number of NOP instructions needed
    nop_count = 0
    # Start at the first memory address
    current_address = 0
    
    # Iterate over each character in the machine code
    for char in machine_code:
        # Check if the current address is not aligned to a 4-byte boundary
        if current_address % 4 != 0:
            # Calculate how many NOPs are needed to align to the next 4-byte boundary
            nop_count += 4 - (current_address % 4)
            # Align the current address to the next 4-byte boundary
            current_address += 4 - (current_address % 4)
        
        # Move to the next memory address
        current_address += 1
    
    return nop_count

# Read input from standard input
import sys
input = sys.stdin.read().strip()
# Call the function and print the result
print(min_nop_instructions(input))