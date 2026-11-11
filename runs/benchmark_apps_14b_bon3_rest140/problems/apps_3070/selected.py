import sys
from collections import defaultdict

def find_earliest_train(N, M, trains):
    # Create a graph to store the earliest arrival time at each station
    earliest_arrival = [float('inf')] * (N + 1)
    earliest_arrival[1] = 0
    
    # Process each train
    for X, S, T, L in trains:
        # Calculate the actual departure and arrival times
        actual_departure = S + L
        actual_arrival = T + L
        
        # Update the earliest arrival time at the destination station
        if actual_departure >= earliest_arrival[X]:
            earliest_arrival[X + 1] = min(earliest_arrival[X + 1], actual_arrival)
    
    # Check if it's possible to reach the last station within the required time
    if earliest_arrival[N] == float('inf'):
        return "impossible"
    
    # Find the earliest time to book a train from station 1
    for X, S, T, L in trains:
        if S >= earliest_arrival[1] and S + L >= earliest_arrival[X] + 1800:
            return S
    
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
    trains.append((X, S, T, L))
    index += 4

# Find and print the result
result = find_earliest_train(N, M, trains)
print(result)