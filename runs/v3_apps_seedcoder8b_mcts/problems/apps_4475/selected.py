def min_product_after_operations(t, test_cases):
    results = []
    for case in test_cases:
        a, b, x, y, n = case
        # Calculate the maximum possible reductions for a and b
        max_reduce_a = a - x
        max_reduce_b = b - y
        
        # Determine the number of operations to be applied to each
        if max_reduce_a + max_reduce_b <= n:
            # If we can reduce both a and b fully, do so
            a -= max_reduce_a
            b -= max_reduce_b
        else:
            # If we can't reduce both fully, prioritize reducing the one with the larger potential reduction
            if max_reduce_a > max_reduce_b:
                # Reduce a as much as possible
                a -= min(max_reduce_a, n)
                # Use the remaining operations to reduce b
                b -= max(0, n - max_reduce_a)
            else:
                # Reduce b as much as possible
                b -= min(max_reduce_b, n)
                # Use the remaining operations to reduce a
                a -= max(0, n - max_reduce_b)
        
        # Calculate the minimum product
        results.append(a * b)
    
    return results

# Read input
t = int(input())
test_cases = [tuple(map(int, input().split())) for _ in range(t)]

# Solve and print results
results = min_product_after_operations(t, test_cases)
for result in results:
    print(result)