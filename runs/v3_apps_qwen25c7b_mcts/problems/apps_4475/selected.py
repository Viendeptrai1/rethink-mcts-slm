import sys

def min_product(a, b, x, y, n):
    max_reduction_a = max(0, a - x)
    max_reduction_b = max(0, b - y)
    
    if n >= (max_reduction_a + max_reduction_b):
        return x * y
    
    if max_reduction_a > max_reduction_b:
        a -= n
    else:
        b -= n
    
    return a * b

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []
    
    for _ in range(t):
        a = int(data[index])
        b = int(data[index + 1])
        x = int(data[index + 2])
        y = int(data[index + 3])
        n = int(data[index + 4])
        index += 5
        
        result = min_product(a, b, x, y, n)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()