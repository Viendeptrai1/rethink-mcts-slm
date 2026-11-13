def max_victories(N, A, P, V):
    from collections import deque

    # Create a list of tuples (dwarf_strength, elf_strength, elf_index)
    dwarves = [(P[i], V[i], i) for i in range(N)]
    # Sort dwarves by their strength in descending order
    dwarves.sort(reverse=True, key=lambda x: x[0])

    # Create a deque for the elves, sorted by their strength in descending order
    elves = deque(sorted([(V[i], i) for i in range(N)], reverse=True, key=lambda x: x[0]))

    # Create a list to keep track of which elves are sitting down
    seated_elves = [False] * N

    # Create a list to keep track of the adversary for each elf
    adversary = [-1] * N

    # Assign adversaries to elves
    for i in range(N):
        adversary[i] = A[i] - 1

    victories = 0

    # Process each dwarf in order of strength
    for dwarf_strength, elf_strength, elf_index in dwarves:
        # If the elf is already seated, skip
        if seated_elves[elf_index]:
            continue

        # Start with the elf's adversary
        current_dwarf = adversary[elf_index]

        # If the adversary is not seated, sit the elf there
        if not seated_elves[current_dwarf]:
            seated_elves[current_dwarf] = True
            continue

        # Otherwise, find the next available dwarf
        while seated_elves[current_dwarf]:
            current_dwarf = (current_dwarf + 1) % N

        # Sit the elf at the found dwarf's position
        seated_elves[current_dwarf] = True

        # If the elf's strength is greater than the dwarf's strength, count it as a victory
        if elf_strength > dwarf_strength:
            victories += 1

    return victories

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N+1]))
P = list(map(int, data[N+1:2*N+1]))
V = list(map(int, data[2*N+1:3*N+1]))

# Calculate and print the result
print(max_victories(N, A, P, V))