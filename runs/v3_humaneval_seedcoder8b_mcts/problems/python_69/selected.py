def search(lst):
    from collections import Counter
    
    # Count the frequency of each integer in the list
    frequency = Counter(lst)
    
    # Initialize the result as -1
    result = -1
    
    # Iterate over the frequency dictionary
    for num, freq in frequency.items():
        # Check if the number is greater than zero and its frequency is at least the number itself
        if num > 0 and freq >= num:
            # Update the result to the maximum number found that satisfies the condition
            result = max(result, num)
    
    return result