import sys
import math

def min_operations_to_equal(a, b):
    diff = abs(a - b)
    # We need to find the smallest n such that n*(n+1)/2 >= diff/2
    # This is equivalent to solving n*(n+1) >= diff
    n = math.ceil((-1 + math.sqrt(1 + 8 * diff)) / 2)
    return n

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    t = int(data[0])
    index = 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        index += 2
        results.append(min_operations_to_equal(a, b))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()