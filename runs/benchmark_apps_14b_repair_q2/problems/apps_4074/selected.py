import sys

def main():
    import sys
    import math
    
    def min_packages(n, k):
        if n <= k:
            return 1
        else:
            return math.ceil(n / k)
    
    t = int(sys.stdin.readline())
    results = []
    
    for _ in range(t):
        n, k = map(int, sys.stdin.readline().split())
        results.append(min_packages(n, k))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()