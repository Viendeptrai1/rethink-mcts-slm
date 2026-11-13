def max_victories(N, A, D, E):
    # Create a list of (adversary, strength) pairs for elves
    elves = [(A[i], E[i]) for i in range(N)]
    # Sort elves based on their strength in descending order
    elves.sort(key=lambda x: x[1], reverse=True)
    
    # Initialize the list of occupied dwarfs
    occupied = [False] * N
    
    # Initialize the count of victories
    victories = 0
    
    # Iterate over sorted elves
    for adv, str in elves:
        # Find the leftmost unoccupied dwarf with strength greater than or equal to the elf's strength
        for j in range(N):
            if not occupied[j]:
                if D[j] >= str:
                    occupied[j] = True
                    victories += 1
                    break
                elif D[(j + 1) % N] < str:
                    occupied[j] = True
                    victories += 1
                    break
    
    return victories

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Parse input
N = int(data[0])
A = list(map(int, data[1:N+1]))
D = list(map(int, data[N+1:2*N+1]))
E = list(map(int, data[2*N+1:]))

# Calculate the maximum number of victories
result = max_victories(N, A, D, E)

# Print the result
print(result)