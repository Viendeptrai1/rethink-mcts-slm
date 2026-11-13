def derivative(xs: list):
    return [i * coef for i, coef in enumerate(xs[1:], start=1)]