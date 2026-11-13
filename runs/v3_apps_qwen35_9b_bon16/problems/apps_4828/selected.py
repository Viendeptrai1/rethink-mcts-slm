import sys

def solve():
    try:
        code = sys.stdin.read().strip()
    except Exception:
        return

    if not code:
        print(0)
        return

    # Map each uppercase instruction to its number of parameters
    params = {}
    current_start = 0
    i = 0
    while i < len(code):
        if code[i].isupper():
            instr = code[i]
            if instr not in params:
                # Count consecutive lowercase letters as parameters
                j = i + 1
                while j < len(code) and code[j].islower():
                    j += 1
                count = j - i - 1
                params[instr] = count
                i = j
            else:
                # Known instruction, skip its parameters
                count = params[instr]
                i += 1 + count
        else:
            # Should not happen based on problem statement (starts with uppercase)
            i += 1

    # Now simulate the program with NOP insertion
    nop_count = 0
    current_addr = 0  # This tracks the logical address where the next instruction will be placed
    
    for instr in code:
        if instr.isupper():
            # This is an instruction
            if current_addr % 4 != 0:
                # Need to pad with NOPs to reach next multiple of 4
                remainder = current_addr % 4
                needed = 4 - remainder
                nop_count += needed
                current_addr += needed
            
            # Execute instruction: current_addr is now divisible by 4
            # The instruction itself takes 1 byte
            current_addr += 1
            
            # Add its parameters
            num_params = params[instr]
            current_addr += num_params
        else:
            # This should not happen as we only iterate over instructions and their params are handled by logic above
            # But if we were iterating character by character, we'd skip params here.
            pass

    print(nop_count)

if __name__ == "__main__":
    solve()