def solve_polycarp_problems(n, k):
    if n < k:
        return "NO"
    if n % k != 0:
        return "NO"
    
    base = n // k
    remainder = n - base * k
    
    result = [base] * k
    for i in range(remainder):
        result[i] += 1
    
    for i in range(k - 1):
        if result[i] >= result[i + 1]:
            return "NO"
    
    return "YES\n" + " ".join(map(str, result))

# Input handling
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Output
print(solve_polycarp_problems(n, k))