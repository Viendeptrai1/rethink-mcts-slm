def max_elf_victories(N, A, P, V):
    # Create lists to store the next and previous positions in the circle
    next_dwarf = list(range(1, N + 1))
    prev_dwarf = list(range(1, N + 1))
    next_dwarf[-1] = 0
    prev_dwarf[0] = N - 1
    
    # Create a position map for elves and dwarves based on their strengths
    dwarf_strength = {strength: i + 1 for i, strength in enumerate(sorted(P, reverse=True))}
    elf_strength = {strength: i + 1 for i, strength in enumerate(sorted(V, reverse=True))}
    
    # Create a set of claimed dwarves
    claimed_dwarves = set()
    
    # Process each elf in order of decreasing strength
    victories = 0
    for elf in range(1, N + 1):
        elf_index = elf_strength[V[elf - 1]] - 1
        current_dwarf = A[elf_index]
        
        # If the chosen dwarf is not claimed, claim it
        if current_dwarf not in claimed_dwarves:
            claimed_dwarves.add(current_dwarf)
            victories += 1
        else:
            # Otherwise, find the next available dwarf
            while current_dwarf in claimed_dwarves:
                current_dwarf = next_dwarf[current_dwarf - 1]
            claimed_dwarves.add(current_dwarf)
    
    return victories

# Read input
N = int(input().strip())
A = list(map(int, input().strip().split()))
P = list(map(int, input().strip().split()))
V = list(map(int, input().strip().split()))

# Compute and print the result
print(max_elf_victories(N, A, P, V))