import sys
from typing import List

def find_earliest_train(N: int, M: int, trains: List[List[int]]) -> int:
    # Initialize the earliest possible start time to a large value
    earliest_start_time = float('inf')
    
    # Iterate through all possible start times
    for start_time in range(86400):
        # Check if we can reach the last station within 1800 seconds
        current_time = start_time
        for i in range(N - 1):
            found = False
            for x, s, t, l in trains:
                if x == i + 1:
                    # Calculate the actual departure and arrival times
                    actual_departure = s + l
                    actual_arrival = t + l
                    
                    # Check if we can catch this train
                    if current_time >= actual_departure:
                        current_time = actual_arrival
                        found = True
                        break
            
            # If we couldn't catch any train at this station, move to the next start time
            if not found:
                break
        
        # If we reached the last station within 1800 seconds, update the earliest start time
        if current_time <= start_time + 1800:
            earliest_start_time = min(earliest_start_time, start_time)
    
    # Return the result
    return earliest_start_time if earliest_start_time != float('inf') else 'impossible'

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
result = find_earliest_train(N, M, trains)
print(result)