def simplify(x, n):
    # Split the fractions into numerators and denominators
    x_num, x_den = map(int, x.split('/'))
    n_num, n_den = map(int, n.split('/'))
    
    # Cross multiply to check if the product is a whole number
    # x * n = (x_num * n_num) / (x_den * n_den)
    # For it to be a whole number, (x_num * n_num) must be divisible by (x_den * n_den)
    return (x_num * n_num) % (x_den * n_den) == 0