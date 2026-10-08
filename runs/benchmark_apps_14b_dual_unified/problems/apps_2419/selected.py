import sys
import math

def min_operations(a, b):
    diff = abs(a - b)
    # Find the smallest k such that k * (k + 1) / 2 >= diff
    k = math.ceil((-1 + math.sqrt(1 + 8 * diff)) / 2)
    # Check if the exact match can be achieved with k operations
    if k * (k + 1) // 2 == diff:
        return k
    else:
        return k + 1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        index += 1
        b = int(data[index])
        index += 1
        results.append(min_operations(a, b))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()