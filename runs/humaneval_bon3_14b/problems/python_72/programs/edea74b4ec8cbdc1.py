def will_it_fly(q, w):
    # Check if the list is palindromic (balanced)
    is_balanced = q == q[::-1]
    
    # Calculate the sum of the elements in the list
    total_weight = sum(q)
    
    # Check if the sum is less than or equal to the maximum possible weight
    is_within_weight_limit = total_weight <= w
    
    # The object will fly if it's balanced and within the weight limit
    return is_balanced and is_within_weight_limit