def prod_signs(arr):
    if not arr:
        return None
    
    sign_product = 1
    magnitude_sum = 0
    
    for num in arr:
        if num == 0:
            return 0
        sign_product *= (1 if num > 0 else -1)
        magnitude_sum += abs(num)
    
    return sign_product * magnitude_sum

# Example usage:
# print(prod_signs([1, 2, 2, -4]))  # Output: -9
# print(prod_signs([0, 1]))         # Output: 0
# print(prod_signs([]))             # Output: None