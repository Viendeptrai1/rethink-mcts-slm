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
    
    # Try to match each elf with a dwarf
    for elf in elves:
        # Find the dwarf that the elf wants to fight
        desired_dwarf = A[elf - 1]
        # Check if the desired dwarf is available
        if not taken_dwarves[desired_dwarf - 1]:
            taken_dwarves[desired_dwarf - 1] = True
            victories += 1
        else:
            # If the desired dwarf is taken, find the next available dwarf
            start = (desired_dwarf % N) - 1
            for i in range(N):
                next_dwarf = (start + i) % N
                if not taken_dwarves[next_dwarf]:
                    taken_dwarves[next_dwarf] = True
                    victories += 1
                    break
    
    return victories

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N+1]))
P = list(map(int, data[N+1:2*N+1]))
V = list(map(int, data[2*N+1:]))

# Calculate and print the result
print(max_victories(N, A, P, V))