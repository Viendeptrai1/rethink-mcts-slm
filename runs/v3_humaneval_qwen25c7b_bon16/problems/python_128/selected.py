def prod_signs(arr):
    if not arr:
        return None

    product_of_signs = 1
    magnitude_sum = 0

    for num in arr:
        if num == 0:
            return 0
        elif num < 0:
            product_of_signs *= -1
        magnitude_sum += abs(num)

    return product_of_signs * magnitude_sum