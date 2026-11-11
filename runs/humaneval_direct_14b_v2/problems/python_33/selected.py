def sort_third(l: list):
    # Extract elements at indices divisible by three
    divisible_by_three = [l[i] for i in range(len(l)) if i % 3 == 0]
    # Sort these elements
    divisible_by_three.sort()
    
    # Create a new list to store the result
    result = []
    # Index to track position in the sorted list
    sorted_index = 0
    
    for i in range(len(l)):
        if i % 3 == 0:
            # Replace element at index i with sorted element
            result.append(divisible_by_three[sorted_index])
            sorted_index += 1
        else:
            # Keep the original element
            result.append(l[i])
    
    return result