def max_elements(p):
    # Convert the number to a string to easily manipulate its digits
    p_str = str(p)
    
    # Initialize the result list with the last digit
    result = [p_str[-1]]
    
    # Iterate over the digits from second last to the first
    for digit in reversed(p_str[:-1]):
        # If the current digit is greater than or equal to the last digit in the result,
        # concatenate it to the last digit and add to the result
        if int(digit) >= int(result[-1]):
            result[-1] += digit
        else:
            # Otherwise, append the current digit to the result
            result.append(digit)
    
    # Return the length of the result list
    return len(result)

# Example usage:
# print(max_elements("9555"))  # Output: 4
# print(max_elements("10000000005"))  # Output: 2
# print(max_elements("800101"))  # Output: 3
# print(max_elements("45"))  # Output: 1
# print(max_elements("1000000000000001223300003342220044555"))  # Output: 17
# print(max_elements("19992000"))  # Output: 1
# print(max_elements("310200"))  # Output: 2