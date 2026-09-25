import sys

def min_packages(n, k):
    for i in range(min(n, k), 0, -1):
        if n % i == 0:
            return n // i

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
        results.append(str(min_packages(n, k)))
    
    print('\n'.join(results))

if __name__ == "__main__":
    main()