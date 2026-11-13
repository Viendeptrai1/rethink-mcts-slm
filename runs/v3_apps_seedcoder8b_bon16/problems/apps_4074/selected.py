def min_packages_to_buy_shovels(t, test_cases):
    results = []
    for n, k in test_cases:
        # Start with the largest possible package size and work downwards
        for package_size in range(k, 0, -1):
            # Check if n is divisible by package_size
            if n % package_size == 0:
                # If divisible, the number of packages needed is n divided by package_size
                results.append(n // package_size)
                break
    return results

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    t = int(data[0])
    test_cases = []
    
    for i in range(1, t * 2, 2):
        n = int(data[i])
        k = int(data[i + 1])
        test_cases.append((n, k))
    
    results = min_packages_to_buy_shovels(t, test_cases)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()