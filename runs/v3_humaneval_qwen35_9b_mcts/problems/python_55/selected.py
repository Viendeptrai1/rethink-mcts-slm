class Solution:
    def fib(self, n: int) -> int:
        if n <= 0:
            return 0
        if n == 1:
            return 1
        
        def multiply(a, b):
            return [
                [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
                [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
            ]
        
        def power(matrix, exp):
            result = [[1, 0], [0, 1]]
            base = matrix
            while exp > 0:
                if exp % 2 == 1:
                    result = multiply(result, base)
                base = multiply(base, base)
                exp //= 2
            return result
        
        base_matrix = [[1, 1], [1, 0]]
        result_matrix = power(base_matrix, n - 1)
        return result_matrix[0][0]

def fib(n: int) -> int:
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    def multiply(a, b):
        return [
            [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
            [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
        ]
    
    def power(matrix, exp):
        result = [[1, 0], [0, 1]]
        base = matrix
        while exp > 0:
            if exp % 2 == 1:
                result = multiply(result, base)
            base = multiply(base, base)
            exp //= 2
        return result
    
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = power(base_matrix, n - 1)
    return result_matrix[0][0]