from collections import deque

def max_victories(N, A, P, V):
    # Create a list of indices sorted by dwarves' strengths
    dwarves = sorted(range(N), key=lambda x: P[x])
    
    # Initialize variables
    visited = [False] * N
    victories = 0
    
    # Iterate over the sorted list of dwarves
    for d in dwarves:
        # Find the elf's adversary
        e = A[d] - 1
        
        # Check if the elf is already seated or if the positions are occupied
        if visited[e]:
            # Find the next available position for the elf
            start = (e + 1) % N
            while visited[start]:
                start = (start + 1) % N
            
            # Check if the position is between the elf's current position and its adversary's position
            if (d < start < e) or (e < start < d) or (start == d):
                return 0
        
        # Place the elf at the first available position
        visited[e] = True
        if V[e] > P[d]:
            victories += 1
    
    return victories

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N+1]))
P = list(map(int, data[N+1:2*N+1]))
V = list(map(int, data[2*N+1:]))

# Calculate and print the result
print(max_victories(N, A, P, V))