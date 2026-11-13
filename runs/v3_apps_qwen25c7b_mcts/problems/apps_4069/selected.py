def min_absolute_value(X, K, D):
    if K % 2 == 0:
        return 0
    else:
        remainder = abs(X) % (2 * D)
        if remainder < D:
            return abs(X) - K * D + D
        else:
            return abs(X) - K * D

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
X = int(data[0])
K = int(data[1])
D = int(data[2])

result = min_absolute_value(X, K, D)
print(result)