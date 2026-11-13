def min_packages(t, test_cases):
    results = []
    for n, k in test_cases:
        for package_size in range(k, 0, -1):
            if n % package_size == 0:
                num_packages = n // package_size
                results.append(num_packages)
                break
    return results

# Read input
t = int(input())
test_cases = [tuple(map(int, input().split())) for _ in range(t)]

# Solve and print results
results = min_packages(t, test_cases)
for result in results:
    print(result)