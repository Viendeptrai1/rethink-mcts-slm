import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    A = int(input_data[0])
    B = int(input_data[1])
    C = int(input_data[2])
    
    # We are selecting positive integers that are multiples of A.
    # Let the selected integers be k1*A, k2*A, ..., kn*A where ki >= 1.
    # The sum S = (k1 + k2 + ... + kn) * A.
    # We need S ≡ C (mod B).
    # Let K = k1 + k2 + ... + kn. Since we must select at least one integer and each ki >= 1,
    # K must be a positive integer (K >= 1).
    # So we need (K * A) ≡ C (mod B).
    # This is equivalent to solving K * A ≡ C (mod B) for K >= 1.
    
    # Let g = gcd(A, B).
    # The linear congruence A * K ≡ C (mod B) has solutions if and only if C is divisible by g.
    # If it is solvable, we can find the smallest non-negative solution K0.
    # Since we need K >= 1, if K0 is 0, we can add B/g to it (since the solutions are periodic with period B/g)
    # to get a positive solution.
    # However, note that if C == 0, then K=0 is a solution mathematically, but we require at least one positive integer.
    # But wait: if C=0, can we achieve sum ≡ 0 mod B?
    # Yes, for example, if we pick just A, the sum is A. If A is a multiple of B, then A ≡ 0 mod B.
    # Actually, the condition is simply: does there exist K >= 1 such that (K*A) % B == C?
    # The set of values { (K*A) % B for K = 1, 2, ... } is exactly the set of multiples of g = gcd(A, B) modulo B.
    # Specifically, the values generated are 0, g, 2g, ..., (B/g - 1)*g (modulo B).
    # So we just need to check if C is a multiple of gcd(A, B).
    
    import math
    g = math.gcd(A, B)
    
    if C % g == 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()