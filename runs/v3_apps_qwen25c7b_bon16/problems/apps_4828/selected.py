def min_nop_for_new_processor(code):
    total_nops = 0
    current_address = 0
    
    for char in code:
        if char.isupper():
            if current_address % 4 != 0:
                nops_needed = (4 - (current_address % 4)) % 4
                total_nops += nops_needed
            current_address += 1 + (char.lower() == 'n')
        else:
            current_address += 1
    
    return total_nops

# Example usage
if __name__ == "__main__":
    import sys
    input_code = sys.stdin.read().strip()
    print(min_nop_for_new_processor(input_code))