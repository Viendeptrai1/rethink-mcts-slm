def min_packages(t, test_cases):
    results = []
    for n, k in test_cases:
        min_packages = float('inf')
        for i in range(1, k + 1):
            if n % i == 0:
                packages_needed = n // i
                if packages_needed < min_packages:
                    min_packages = packages_needed
        results.append(min_packages)
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    test_cases = []
    index = 1
    for _ in range(t):
        n = int(data[index])
        k = int(data[index + 1])
        test_cases.append((n, k))
        index += 2
    
    results = min_packages(t, test_cases)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()