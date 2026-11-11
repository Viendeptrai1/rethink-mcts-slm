import math

def min_packages(n, k):
    return n // math.gcd(n, k)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        n = int(data[index])
        k = int(data[index + 1])
        results.append(min_packages(n, k))
        index += 2
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()