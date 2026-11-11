def earliest_train_journey(N, M, trains):
    # Create a list to store the latest arrival time at each station
    latest_arrival = [-1] * (N + 1)
    latest_arrival[N] = 86400  # Ending point (end of the day)

    # Process each train in reverse order
    for X, S, T, L in reversed(trains):
        # Calculate the new departure and arrival times
        new_departure = S - L
        new_arrival = T - L

        # Update the latest arrival time at the source station
        if new_departure >= latest_arrival[X + 1] - 1800:
            latest_arrival[X] = min(latest_arrival[X], new_departure)

    # Check if it's possible to reach the first station within the required time
    if latest_arrival[1] == -1:
        return "impossible"
    else:
        return latest_arrival[1]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()

    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    index += 2

    trains = []
    for _ in range(M):
        X = int(data[index])
        S = int(data[index + 1])
        T = int(data[index + 2])
        L = int(data[index + 3])
        trains.append((X, S, T, L))
        index += 4

    result = earliest_train_journey(N, M, trains)
    print(result)

if __name__ == "__main__":
    main()