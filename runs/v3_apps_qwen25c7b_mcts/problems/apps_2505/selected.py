MOD = 998244353

def sum_of_f(N, points):
    points.sort()
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    
    def count_subsets(start_x, end_x, start_y, end_y):
        return ((end_x - start_x + 1) * (end_y - start_y + 1)) % MOD
    
    total_sum = 0
    for i in range(N):
        for j in range(i+1, N):
            left = min(x_coords[i], x_coords[j])
            right = max(x_coords[i], x_coords[j])
            bottom = min(y_coords[i], y_coords[j])
            top = max(y_coords[i], y_coords[j])
            total_sum += count_subsets(left, right, bottom, top)
            total_sum %= MOD
    
    return total_sum

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
points = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]

# Calculate and print result
result = sum_of_f(N, points)
print(result)