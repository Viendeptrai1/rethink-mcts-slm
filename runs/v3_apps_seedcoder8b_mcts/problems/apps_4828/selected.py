def min_nop_instructions(machine_code):
    # Calculate the number of bytes used by the instructions
    num_bytes = len(machine_code)
    
    # Calculate the number of 4-byte chunks needed
    num_chunks = (num_bytes + 3) // 4
    
    # Calculate the total number of bytes needed to fit the instructions in 4-byte chunks
    total_bytes_needed = num_chunks * 4
    
    # Calculate the number of NOP instructions needed to align the program
    nop_instructions_needed = total_bytes_needed - num_bytes
    
    return nop_instructions_needed

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(min_nop_instructions(input))