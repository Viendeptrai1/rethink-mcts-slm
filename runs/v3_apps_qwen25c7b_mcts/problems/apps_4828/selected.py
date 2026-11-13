def min_nops(program):
    # Define the mapping of instructions to their parameter counts
    instruction_params = {
        'A': 3,
        'B': 2,
        'C': 0,
        'D': 4,
        'E': 1,
        'F': 2,
        'G': 1
    }
    
    nops = 0
    current_address = 0
    
    for char in program:
        if char.isupper():
            # Calculate the number of NOPs needed to align the next instruction
            padding = (current_address + 3) & ~3 - current_address
            nops += padding
            current_address += padding
        
        # Move to the next instruction or parameter
        current_address += 1
    
    return nops

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(min_nops(input))