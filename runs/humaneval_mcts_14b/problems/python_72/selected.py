def will_it_fly(q, w):
    # Check if the list is a palindrome
    is_balanced = q == q[::-1]
    
    # Calculate the sum of the elements in the list
    total_weight = sum(q)
    
    # Check if the sum of the elements is less than or equal to the maximum possible weight
    within_weight_limit = total_weight <= w
    
    # The object will fly if it's balanced and within the weight limit
    return is_balanced and within_weight_limit