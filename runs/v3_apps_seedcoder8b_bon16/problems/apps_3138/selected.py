def count_matching_ranges(n, numbers):
    from collections import defaultdict
    
    # This will store the number of ways to achieve each product result
    product_count = defaultdict(int)
    
    # This will store the number of ways to achieve each sum result
    sum_count = defaultdict(int)
    
    # Initial counts
    sum_count[0] = 1  # Base case: sum of 0 can be achieved in one way (empty set)

    result = 0
    current_sum = 0
    current_product = 1

    # Loop over the numbers
    for i in range(n):
        # Update the current sum and product
        current_sum += numbers[i]
        current_product *= numbers[i]
        
        # If the current product exists in the sum_count, add the number of ways to reach this sum
        if current_product in sum_count:
            result += sum_count[current_product]
        
        # Update the sum_count with the current sum
        sum_count[current_sum] += 1
        
        # We need to remove contributions from the start of the current window
        if current_product != 1:
            product_count[current_product] += 1
        
        if i > 0:
            # Prevent division by zero and ensure we are only looking at valid products
            if numbers[i] != 0:
                current_product //= numbers[i - 1]
            else:
                current_product = 1  # Reset if we encounter zero (only if not the first element)

    return result

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    print(count_matching_ranges(n, numbers))