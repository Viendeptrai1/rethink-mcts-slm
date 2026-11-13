def solve(X, K, D):
    total_distance = K * D
    return min(abs(X), abs(X + total_distance), abs(X - total_distance))

X, K, D = map(int, input().split())
print(solve(X, K, D))