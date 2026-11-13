import sys
from typing import List

def find_earliest_train_time(N: int, M: int, trains: List[List[int]]) -> int:
    # Initialize the maximum delay needed
    max_delay = 1800
    
    # Sort trains based on their departure time
    trains.sort(key=lambda x: x[1])
    
    # Iterate through the sorted trains to find the earliest valid booking time
    for i in range(M):
        X, S, T, L = trains[i]
        current_delay = T - S + L
        
        # Check if the current delay is sufficient
        if current_delay >= max_delay:
            return S
        
        # Check for overlapping trains and adjust the delay accordingly
        for j in range(i + 1, M):
            X_next, S_next, T_next, L_next = trains[j]
            if X == X_next:
                continue
            
            # If there's an overlap, calculate the effective delay
            if S <= S_next <= T:
                current_delay += T_next - S_next + L_next
                break
        
        # Update the maximum delay needed
        max_delay -= current_delay
    
    return "impossible"

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])

trains = []
index = 2
for _ in range(M):
    X = int(data[index])
    S = int(data[index + 1])
    T = int(data[index + 2])
    L = int(data[index + 3])
    trains.append([X, S, T, L])
    index += 4

# Find and print the result
result = find_earliest_train_time(N, M, trains)
print(result)