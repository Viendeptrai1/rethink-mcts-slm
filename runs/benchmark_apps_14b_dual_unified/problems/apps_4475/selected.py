import sys

def min_product(a, b, x, y, n):
    # Calculate the maximum possible reduction in a and b
    max_reduce_a = a - x
    max_reduce_b = b - y
    
    # If we can reduce both a and b within the limit of n
    if max_reduce_a + max_reduce_b <= n:
        # Reduce both a and b to their minimum values
        return x * y
    
    # If we can only reduce a within the limit of n
    if max_reduce_a <= n:
        # Reduce a to its minimum value and reduce b accordingly
        return (a - n) * b
    
    # If we can only reduce b within the limit of n
    if max_reduce_b <= n:
        # Reduce b to its minimum value and reduce a accordingly
        return a * (b - n)
    
    # If we can reduce both a and b but not fully to their minimum values
    # Calculate the optimal reduction
    total_reduce = n
    if (a - x) * (b - y) > (a - y) * (b - x):
        # Reduce a more than b
        reduce_a = min(max_reduce_a, total_reduce // 2)
        reduce_b = total_reduce - reduce_a
    else:
        # Reduce b more than a
        reduce_b = min(max_reduce_b, total_reduce // 2)
        reduce_a = total_reduce - reduce_b
    
    return (a - reduce_a) * (b - reduce_b)

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
        results.append(min_product(a, b, x, y, n))
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()