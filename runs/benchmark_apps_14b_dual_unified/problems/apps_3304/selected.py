import sys
import heapq

def max_victories(N, A, P, V):
    # Pair up dwarves and elves based on their strengths in descending order
    dwarves = sorted(enumerate(P), key=lambda x: -x[1])
    elves = sorted(enumerate(V), key=lambda x: -x[1])
    
    # Create a min-heap to keep track of the positions of dwarves
    heap = []
    for i in range(N):
        heapq.heappush(heap, (A[elves[i][0]], i))
    
    # Initialize the count of victories
    victories = 0
    
    # Try to match each elf with a dwarf
    for _, elf_strength in elves:
        while heap:
            dwarf_pos, dwarf_index = heapq.heappop(heap)
            if P[dwarf_index] < elf_strength:
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