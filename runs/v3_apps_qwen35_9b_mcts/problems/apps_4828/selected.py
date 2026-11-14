import sys

def solve():
    code = sys.stdin.read().strip()
    if not code:
        print(0)
        return

    # Map each uppercase letter to its parameter count
    params = {}
    i = 0
    n = len(code)
    while i < n:
        if code[i].isupper():
            char = code[i]
            j = i + 1
            while j < n and code[j].islower():
                j += 1
            count = j - i - 1
            params[char] = count
            i = j
        else:
            i += 1

    # Simulate memory layout
    nop_count = 0
    current_offset = 0  # Current byte offset in memory

    for char in code:
        if char.isupper():
            # This is an instruction
            # Check alignment: instruction must start at offset % 4 == 0
            if current_offset % 4 != 0:
                needed = 4 - (current_offset % 4)
                nop_count += needed
                current_offset += needed
            
            # Execute instruction: 1 byte for opcode
            current_offset += 1
            # Add parameters
            p_count = params[char]
            current_offset += p_count
        else:
            # This is a parameter, just consume 1 byte
            current_offset += 1

    print(nop_count)

if __name__ == "__main__":
    solve()