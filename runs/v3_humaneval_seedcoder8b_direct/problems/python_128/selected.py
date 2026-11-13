def prod_signs(arr):
    if not arr:
        return None
    
    product = 1
    sum_magnitudes = 0
    
    for num in arr:
        if num > 0:
            product *= 1
            sum_magnitudes += num
        elif num < 0:
            product *= -1
            sum_magnitudes += abs(num)
        else:
            product *= 0
            sum_magnitudes += 0
    
    return sum_magnitudes * product