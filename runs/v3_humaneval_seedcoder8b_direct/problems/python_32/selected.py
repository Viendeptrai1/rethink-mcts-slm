import math

def find_zero(xs: list):
    """ xs are coefficients of a polynomial.
    find_zero find x such that poly(x) = 0.
    find_zero returns only one zero point, even if there are many.
    Moreover, find_zero only takes list xs having even number of coefficients
    and largest non zero coefficient as it guarantees
    a solution.
    """
    # Degree of the polynomial
    n = len(xs) - 1
    
    # Check if the polynomial has an even number of coefficients
    if n % 2 != 0:
        raise ValueError("The polynomial must have an even number of coefficients.")
    
    # Check if the largest non-zero coefficient is present
    if xs[0] == 0:
        raise ValueError("The largest non-zero coefficient must be present.")
    
    # Use the fact that the polynomial has an even number of coefficients
    # and the largest non-zero coefficient guarantees a solution.
    # We can use the companion matrix method to find a root.
    
    # Construct the companion matrix
    companion = [[0] * n for _ in range(n)]
    for i in range(n - 1):
        companion[i][i + 1] = 1
    for i in range(n):
        companion[n - 1][i] = -xs[n - i] / xs[n]
    
    # Find the eigenvalues of the companion matrix
    # For simplicity, we use numpy to find the eigenvalues
    import numpy as np
    eigenvalues = np.linalg.eigvals(companion)
    
    # Return the first eigenvalue as the root
    return float(eigenvalues[0])