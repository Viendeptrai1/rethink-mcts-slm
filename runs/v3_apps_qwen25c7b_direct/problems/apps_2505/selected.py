MOD = 998244353

def sum_of_f(N, points):
    points.sort()
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    
    def count_subsets(start_x, end_x, start_y, end_y):
        return (end_x - start_x + 1) * (end_y - start_y + 1)
    
    total_sum = 0
    
    for i in range(N):
        for j in range(i, N):
            for k in range(N):
                for l in range(k, N):
                    if x_coords[i] <= x_coords[j] and y_coords[k] <= y_coords[l]:
                        total_sum += count_subsets(x_coords[i], x_coords[j], y_coords[k], y_coords[l])
    
    return total_sum % MOD

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

# Calculate and print result
result = sum_of_f(N, points)
print(result)