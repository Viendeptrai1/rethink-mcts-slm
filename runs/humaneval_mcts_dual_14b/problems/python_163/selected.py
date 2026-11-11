def generate_integers(a, b):
    def is_even_digit(n):
        return all(int(digit) % 2 == 0 for digit in str(n))
    
    if a > b:
        a, b = b, a
    
    result = []
    for num in range(a, b + 1):
        if is_even_digit(num):
            result.append(num)
    
    return result