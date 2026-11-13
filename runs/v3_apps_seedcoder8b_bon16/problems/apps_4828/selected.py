def min_nop_instructions(machine_code):
    # Calculate the total memory required based on the machine code length
    total_memory = len(machine_code)
    
    # Calculate the number of 4-byte chunks required
    required_chunks = (total_memory + 3) // 4
    
    # The number of NOP instructions needed is the difference between
    # the required chunks and the current instruction positions
    # that do not satisfy the divisible by 4 requirement.
    nop_instructions = required_chunks * 4 - total_memory
    
    return nop_instructions

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(min_nop_instructions(input))