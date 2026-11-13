def min_nop_instructions(program):
    total_nops = 0
    current_address = 0
    
    for char in program:
        if char.isupper():
            # Calculate the number of NOPs needed to align with the next multiple of 4
            nops_needed = (4 - (current_address % 4)) % 4
            total_nops += nops_needed
            current_address += nops_needed + 1  # Add 1 for the instruction itself
        else:
            current_address += 1  # Move to the next parameter
    
    return total_nops

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(min_nop_instructions(input))