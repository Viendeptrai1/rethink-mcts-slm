import sys

def solve():
    s = sys.stdin.read().strip()
    if not s:
        print(0)
        return

    # Map each uppercase instruction to its parameter count
    params = {}
    i = 0
    n = len(s)
    while i < n:
        if s[i].isupper():
            instr = s[i]
            j = i + 1
            while j < n and s[j].islower():
                j += 1
            count = j - i - 1
            params[instr] = count
            i = j
        else:
            # Should not happen based on problem statement
            i += 1

    # Simulate execution and count NOPs
    current_addr = 0
    total_nops = 0
    i = 0
    n = len(s)
    
    while i < n:
        if s[i].isupper():
            instr = s[i]
            param_count = params[instr]
            
            # Calculate how many bytes this instruction + parameters will occupy
            total_bytes = 1 + param_count
            
            # We need the next instruction to start at an address divisible by 4
            # current_addr is where this instruction starts
            # After this instruction, the next address will be current_addr + total_bytes
            # We need (current_addr + total_bytes) % 4 == 0
            
            remainder = (current_addr + total_bytes) % 4
            if remainder != 0:
                nops_needed = 4 - remainder
                total_nops += nops_needed
                current_addr += nops_needed
            
            current_addr += total_bytes
            i += 1 + param_count
        else:
            # This case should not be reached given the problem constraints
            i += 1

    print(total_nops)

if __name__ == "__main__":
    solve()