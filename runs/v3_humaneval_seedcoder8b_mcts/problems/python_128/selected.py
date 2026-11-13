def prod_signs(arr):
    if not arr:
        return None
    
    def sign(x):
        return 1 if x > 0 else -1 if x < 0 else 0
    
    sign_product = 1
    magnitude_sum = 0
    all_zeros = True
    
    for num in arr:
        sign_product *= sign(num)
        magnitude_sum += abs(num)
        if num != 0:
            all_zeros = False
    
    return 0 if all_zeros else magnitude_sum * sign_product