import sys

def min_packages(n, k):
    # Find the largest package size that is less than or equal to n
    package_size = min(n, k)
    # Calculate the minimum number of packages needed
    return (n + package_size - 1) // package_size

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        index += 1
        k = int(data[index])
        index += 1
        results.append(min_packages(n, k))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()