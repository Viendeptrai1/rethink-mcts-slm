import sys

def earliest_train_journey(N, M, trains):
    # Sort trains by their planned departure time
    trains.sort(key=lambda x: x[1])
    
    # Iterate over each train to find the earliest possible start time
    for X, S, T, L in trains:
        # Calculate the latest possible arrival time to still qualify for the refund
        latest_arrival = T + 1800
        
        # Check if there exists a train that can reach the destination in time
        for i in range(M):
            X2, S2, T2, L2 = trains[i]
            if X2 == X + 1:
                # Calculate the earliest possible arrival time of the next train
                earliest_next_arrival = max(S2 + L2, latest_arrival)
                
                # Check if the next train can reach the destination in time
                if earliest_next_arrival <= T2 + L2:
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

# Find the earliest train journey
result = earliest_train_journey(N, M, trains)

# Print the result
print(result)