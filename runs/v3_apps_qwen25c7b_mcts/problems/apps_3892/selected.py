import sys
from collections import defaultdict

def min_delivery_time(n, m, candies):
    def calculate_time(start_station):
        visited = [False] * (n + 1)
        current_station = start_station
        time = 0
        
        while True:
            if not visited[current_station]:
                visited[current_station] = True
                time += 1
            
            found_candy = False
            for i in range(m):
                if candies[i][0] == current_station:
                    candies[i][0] = -1
                    found_candy = True
                    break
            
            if not found_candy:
                return time
            
            if current_station == n:
                current_station = 1
            else:
                current_station += 1
    
    result = []
    for i in range(1, n + 1):
        result.append(calculate_time(i))
    
    return result

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

candies = []
index = 2
for _ in range(m):
    a = int(data[index])
    b = int(data[index + 1])
    candies.append([a, b])
    index += 2

# Calculate and print the result
result = min_delivery_time(n, m, candies)
print(" ".join(map(str, result)))