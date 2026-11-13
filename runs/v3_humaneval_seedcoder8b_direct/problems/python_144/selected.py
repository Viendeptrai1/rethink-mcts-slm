def simplify(x, n):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    x_num, x_den = map(int, x.split('/'))
    n_num, n_den = map(int, n.split('/'))

    numerator = x_num * n_num
    denominator = x_den * n_den

    common = gcd(numerator, denominator)
    simplified_numerator = numerator // common
    simplified_denominator = denominator // common

    return simplified_denominator == 1