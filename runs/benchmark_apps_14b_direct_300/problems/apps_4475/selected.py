import sys

def min_product(a, b, x, y, n):
    # Calculate the maximum reduction possible for a and b
    max_reduce_a = a - x
    max_reduce_b = b - y
    
    # If total possible reductions are less than or equal to n, reduce fully
    if max_reduce_a + max_reduce_b <= n:
        return x * y
    
    # Otherwise, distribute reductions optimally
    if max_reduce_a > n:
        return (a - n) * b
    else:
        return a * (b - (n - max_reduce_a))

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