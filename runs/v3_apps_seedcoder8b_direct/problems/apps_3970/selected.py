def largest_k_multiple_free_subset(n, k, arr):
    # Sort the array to process elements in increasing order
    arr.sort()
    
    # Initialize a set to keep track of elements in the k-multiple free subset
    free_set = set()
    
    for num in arr:
        # Check if the current number is a multiple of any number in the free set
        is_free = True
        for multiple in range(num, num + k * (len(free_set) + 1), num):
            if multiple in free_set:
                is_free = False
                break
        
        # If it's free, add it to the free set
        if is_free:
            free_set.add(num)
    
    # Return the size of the free set
    return len(free_set)

# Read input
n, k = map(int, input().split())
arr = list(map(int, input().split()))

# Get the result and print it
result = largest_k_multiple_free_subset(n, k, arr)
print(result)