def toy_train(n, m, candies):
    # Initialize the distance matrix with infinity
    dist = [[float('inf')] * n for _ in range(n)]
    
    # Distance from a station to itself is 0
    for i in range(n):
        dist[i][i] = 0
    
    # Set the direct travel distances between stations
    for i in range(n):
        dist[i][(i + 1) % n] = 1
        dist[(i + 1) % n][i] = 1
    
    # Floyd-Warshall algorithm to find shortest paths between all pairs of stations
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Calculate the minimum time for each starting station
    min_time = [0] * n
    for start in range(n):
        total_time = 0
        for a, b in candies:
            # Calculate the shortest path from a to b
            total_time += dist[a - 1][b - 1]
        min_time[start] = total_time
    
    # Print the result
    print(" ".join(map(str, min_time)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
candies = []

index = 2
for _ in range(m):
    a = int(data[index])
    b = int(data[index + 1])
    candies.append((a, b))
    index += 2

# Call the function with the input data
toy_train(n, m, candies)