def sort_third(l: list):
    # Extract elements at indices divisible by 3
    divisible_by_three = [l[i] for i in range(len(l)) if i % 3 == 0]
    
    # Sort the extracted elements
    divisible_by_three.sort()
    
    # Create a new list to store the result
    result = l[:]
    
    # Place the sorted elements back into their original positions
    index = 0
    for i in range(len(l)):
        if i % 3 == 0:
            result[i] = divisible_by_three[index]
            index += 1
    
    return result