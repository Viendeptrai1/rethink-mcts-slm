import sys

def min_packages(n, k):
    # Start checking from the largest possible package size down to 1
    for i in range(k, 0, -1):
        if n % i == 0:
            return n // i

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
        index += 2
        results.append(min_packages(n, k))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()