import sys

def find_earliest_train(N, M, trains):
    # Sort trains by their planned departure time
    trains.sort(key=lambda x: x[1])
    
    # Initialize the earliest time to a large value
    earliest_time = float('inf')
    
    # Iterate over each train
    for i in range(M):
        X, S, T, L = trains[i]
        
        # Calculate the actual departure and arrival times
        actual_departure = S + L
        actual_arrival = T + L
        
        # Check if this train can be part of a journey that meets the condition
        if actual_arrival >= 1800:
            earliest_time = min(earliest_time, actual_departure)
    
    # If no valid train was found, return "impossible"
    if earliest_time == float('inf'):
        return "impossible"
    
    return earliest_time

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
    trains.append((X, S, T, L))
    index += 4

# Find and print the earliest time
result = find_earliest_train(N, M, trains)
print(result)