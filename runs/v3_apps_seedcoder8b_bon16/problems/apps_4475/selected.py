def min_product_after_operations(t, test_cases):
    results = []
    
    for i in range(t):
        a, b, x, y, n = test_cases[i]
        
        # Calculate how much we can reduce each variable
        reduce_a = a - x
        reduce_b = b - y
        
        # Determine which pair to reduce first to minimize the product
        if reduce_a >= reduce_b:
            # Reduce 'a' by the smaller or equal amount of what's available
            operations_used = min(n, reduce_a)
            a -= operations_used
            b -= max(0, n - operations_used)
        else:
            # Reduce 'b' by the smaller or equal amount of what's available
            operations_used = min(n, reduce_b)
            b -= operations_used
            a -= max(0, n - operations_used)
        
        # Calculate the minimum product
        min_product = a * b
        results.append(min_product)
    
    return results

# Example usage:
# Reading input from standard input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
test_cases = []
index = 1
for _ in range(t):
    a = int(data[index])
    b = int(data[index + 1])
    x = int(data[index + 2])
    y = int(data[index + 3])
    n = int(data[index + 4])
    test_cases.append((a, b, x, y, n))
    index += 5

results = min_product_after_operations(t, test_cases)

for result in results:
    print(result)