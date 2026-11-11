import heapq

def max_victories(N, A, P, V):
    # Sort dwarves and elves by strength in descending order
    dwarves = sorted(enumerate(P), key=lambda x: -x[1])
    elves = sorted(enumerate(V), key=lambda x: -x[1])
    
    # Min-heap to manage available seats
    available_seats = list(range(1, N + 1))
    heapq.heapify(available_seats)
    
    # Dictionary to map dwarf index to its original position
    dwarf_pos = {dwarf[0]: idx for idx, dwarf in enumerate(dwarves)}
    
    victories = 0
    
    for elf_idx, elf_strength in elves:
        preferred_seat = A[elf_idx]
        
        # Find the actual seat index
        preferred_seat_index = dwarf_pos[preferred_seat - 1]
        
        # Check if the preferred seat is available
        while available_seats and available_seats[0] != preferred_seat:
            # If the preferred seat is not available, find the next available seat
            current_seat = heapq.heappop(available_seats)
            current_dwarf_index = dwarf_pos[current_seat - 1]
            
            # Compare strengths and determine the winner
            if V[elf_idx] > P[current_dwarf_index]:
                victories += 1
        
        # If the preferred seat is available, check it
        if available_seats and available_seats[0] == preferred_seat:
            heapq.heappop(available_seats)
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