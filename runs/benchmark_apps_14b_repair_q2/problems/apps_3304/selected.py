import sys
from typing import List

def max_victories(N: int, A: List[int], P: List[int], V: List[int]) -> int:
    # Sort dwarves by their strength in descending order
    dwarves = sorted(range(1, N + 1), key=lambda x: P[x - 1], reverse=True)
    # Sort elves by their strength in descending order
    elves = sorted(range(1, N + 1), key=lambda x: V[x - 1], reverse=True)
    
    # Create a list to keep track of which dwarves are taken
    taken_dwarves = [False] * N
    
    victories = 0
    
    # Try to assign each elf to a dwarf
    for elf in elves:
        # Find the preferred dwarf for this elf
        preferred_dwarf = A[elf - 1]
        
        # Check if the preferred dwarf is available
        if not taken_dwarves[preferred_dwarf - 1]:
            taken_dwarves[preferred_dwarf - 1] = True
            victories += 1
            continue
        
        # If the preferred dwarf is taken, find the next available dwarf
        current_dwarf = preferred_dwarf
        for _ in range(N):
            current_dwarf = (current_dwarf % N) + 1
            if not taken_dwarves[current_dwarf - 1]:
                taken_dwarves[current_dwarf - 1] = True
                victories += 1
                break
    
    return victories

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N + 1]))
P = list(map(int, data[N + 1:2 * N + 1]))
V = list(map(int, data[2 * N + 1:]))

# Calculate and print the result
print(max_victories(N, A, P, V))