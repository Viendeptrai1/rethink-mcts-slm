def prod_signs(arr):
    if not arr:
        return None
    
    product_of_signs = 1
    sum_of_magnitudes = 0
    
    for num in arr:
        if num == 0:
            return 0
        magnitude = abs(num)
        sign = 1 if num > 0 else -1
        sum_of_magnitudes += magnitude
        product_of_signs *= sign
    
    return sum_of_magnitudes * product_of_signs