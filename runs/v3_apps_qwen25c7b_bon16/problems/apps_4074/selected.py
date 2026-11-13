import sys

def min_packages(n, k):
    return (n - 1) // k + 1

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    
    results = []
    for _ in range(t):
        n = int(data[index])
        k = int(data[index + 1])
        index += 2
        
        result = min_packages(n, k)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()