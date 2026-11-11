import sys

def earliest_train_journey(N, M, trains):
    # Sort trains by their planned departure times
    trains.sort(key=lambda x: x[1])
    
    # Iterate through each train to find the earliest possible start time
    for X, S, T, L in trains:
        # Calculate the latest possible arrival time to still get the refund
        latest_arrival = S + 1800
        
        # Check if there exists a train that can reach the destination in time
        found = False
        for i in range(M):
            X2, S2, T2, L2 = trains[i]
            if X2 == X + 1:
                # Calculate the actual arrival time considering the delay
                actual_arrival = max(S2 + L2, latest_arrival)
                if actual_arrival <= T2 + L2:
                    found = True
                    break
        
        # If no such train is found, return the current train's departure time
        if not found:
            return S
    
    # If no valid start time is found, return "impossible"
    return "impossible"

# Read input from stdin
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

# Get the result
result = earliest_train_journey(N, M, trains)

# Print the result
print(result)