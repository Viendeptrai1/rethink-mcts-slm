def min_time_to_deliver_candies(n, m, candies):
    from collections import defaultdict, deque

    # Create adjacency list for the circular railway network
    adj = defaultdict(list)
    for i in range(1, n):
        adj[i].append(i + 1)
    adj[n].append(1)

    # Create a list to store the number of candies that need to be delivered to each station
    delivery_count = [0] * (n + 1)
    for a, b in candies:
        delivery_count[b] += 1

    # Function to calculate the minimum time starting from a given station
    def calculate_min_time(start_station):
        visited = [False] * (n + 1)
        queue = deque([(start_station, 0)])  # (current_station, current_time)
        total_time = 0
        remaining_candies = m

        while remaining_candies > 0:
            current_station, current_time = queue.popleft()

            if not visited[current_station]:
                visited[current_station] = True
                total_time = current_time

                # Deliver candies at the current station
                if delivery_count[current_station] > 0:
                    remaining_candies -= delivery_count[current_station]
                    delivery_count[current_station] = 0

                # Add the next station to the queue
                next_station = adj[current_station][0]
                queue.append((next_station, current_time + 1))

        return total_time

    # Calculate the minimum time for each starting station
    min_times = []
    for start_station in range(1, n + 1):
        min_times.append(calculate_min_time(start_station))

    return min_times

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
candies = [(int(data[i * 2 + 2]), int(data[i * 2 + 3])) for i in range(m)]

# Get the result
result = min_time_to_deliver_candies(n, m, candies)

# Print the result
print(" ".join(map(str, result)))