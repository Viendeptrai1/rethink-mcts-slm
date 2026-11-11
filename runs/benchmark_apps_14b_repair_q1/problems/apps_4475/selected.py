import sys

def min_product(a, b, x, y, n):
    # Calculate the maximum possible reduction for a and b
    max_reduce_a = a - x
    max_reduce_b = b - y
    
    # If we can reduce both a and b within the limit of n
    if max_reduce_a + max_reduce_b <= n:
        # Reduce both a and b as much as possible
        reduce_a = max_reduce_a
        reduce_b = max_reduce_b
    else:
        # We need to distribute the reductions between a and b
        total_reduce = n
        # Calculate the potential reduction in a and b
        potential_reduce_a = min(max_reduce_a, total_reduce)
        potential_reduce_b = min(max_reduce_b, total_reduce)
        
        # If reducing a more helps, do that first
        if (a - potential_reduce_a) * (b - (total_reduce - potential_reduce_a)) < (a - (total_reduce - potential_reduce_b)) * (b - potential_reduce_b):
            reduce_a = potential_reduce_a
            reduce_b = total_reduce - potential_reduce_a
        else:
            reduce_a = total_reduce - potential_reduce_b
            reduce_b = potential_reduce_b
    
    # Calculate the new values of a and b
    new_a = a - reduce_a
    new_b = b - reduce_b
    
    # Return the product of the new values
    return new_a * new_b

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