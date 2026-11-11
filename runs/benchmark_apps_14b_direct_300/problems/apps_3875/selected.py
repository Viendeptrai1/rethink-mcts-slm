import sys
from fractions import Fraction

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    MOD = 1000000007
    
    def dp(i, j):
        if i == N:
            return Fraction(1, 1)
        if j == 0:
            return Fraction(A[i], 1) * dp(i + 1, 1) + Fraction(1 - A[i], 1) * dp(i + 1, 0)
        else:
            return Fraction(A[i] - j + 1, A[i]) * dp(i + 1, j + 1) + Fraction(j, A[i]) * dp(i + 1, j)
    
    result = Fraction(0, 1)
    for j in range(1, N + 1):
        result += j * dp(1, j)
    
    result = result % MOD
    print(result.numerator)

if __name__ == "__main__":
    main()