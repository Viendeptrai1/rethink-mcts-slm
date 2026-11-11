import sys
import heapq

def max_victories(N, A, P, V):
    # Create a list of tuples (dwarf_strength, elf_strength, elf_index)
    dwarves = [(P[i], V[i], i) for i in range(N)]
    
    # Sort the dwarves by their strength in descending order
    dwarves.sort(reverse=True)
    
    # Create a min-heap to keep track of the elves' strengths
    elf_heap = []
    
    # Initialize the number of victories
    victories = 0
    
    # Iterate over the sorted dwarves
    for dwarf_strength, elf_strength, elf_index in dwarves:
        # If the heap is empty or the current elf is stronger than the weakest elf in the heap
        if not elf_heap or elf_strength > elf_heap[0][0]:
            # Add the current elf to the heap
            heapq.heappush(elf_heap, (elf_strength, elf_index))
            # Increment the number of victories
            victories += 1
        else:
            # If the current elf is weaker, replace the weakest elf in the heap
            heapq.heapreplace(elf_heap, (elf_strength, elf_index))
    
    return victories

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N+1]))
P = list(map(int, data[N+1:2*N+1]))
V = list(map(int, data[2*N+1:3*N+1]))

# Calculate and print the maximum number of victories
print(max_victories(N, A, P, V))