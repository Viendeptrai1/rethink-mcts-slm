def min_time_to_deliver_candies(n, m, deliveries):
    # Calculate the shortest path between two stations considering the circular nature
    def shortest_path(start, end):
        if start <= end:
            return end - start
        else:
            return n - start + end

    # Initialize result list with maximum possible delivery time
    result = [2 * m] * n

    # Calculate time for each starting station
    for start_station in range(1, n + 1):
        total_time = 0
        visited = [False] * (n + 1)
        current_station = start_station

        # Greedily find minimum time path for each candy
        for _ in range(m):
            min_time = float('inf')
            min_candy_index = -1

            for i, (a_i, b_i) in enumerate(deliveries):
                if not visited[i]:
                    time = shortest_path(current_station, a_i) + shortest_path(a_i, b_i)
                    if time < min_time:
                        min_time = time
                        min_candy_index = i

            # If no unvisited candy found, break
            if min_candy_index == -1:
                break

            # Update total time and mark the candy as visited
            total_time += min_time
            visited[min_candy_index] = True
            current_station = deliveries[min_candy_index][1]

        result[start_station - 1] = total_time

    # Print the results
    print(" ".join(map(str, result)))

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
deliveries = [(int(data[i * 2 + 2]), int(data[i * 2 + 3])) for i in range(m)]

# Call the function with input data
min_time_to_deliver_candies(n, m, deliveries)