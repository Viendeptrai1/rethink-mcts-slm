def count_returnable_rooms(t, test_cases):
    results = []
    for n, s in test_cases:
        count = 0
        for i in range(n):
            if s[i] != '-' and s[(i + 1) % n] != '-':
                count += 1
        results.append(count)
    return results

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
test_cases = []

index = 1
for _ in range(t):
    n = int(data[index])
    s = data[index + 1]
    index += 2
    test_cases.append((n, s))

# Process and print results
results = count_returnable_rooms(t, test_cases)
for result in results:
    print(result)