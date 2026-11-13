import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])

    # We need a+b ≡ 0 (mod K), b+c ≡ 0 (mod K), c+a ≡ 0 (mod K)
    # This implies a ≡ b ≡ c (mod K) and 2a ≡ 0 (mod K)
    # So a must be congruent to some r mod K where 2r ≡ 0 (mod K)
    # Count how many numbers in [1, N] satisfy 2x ≡ 0 (mod K)
    # Let count be C. Then each of a, b, c can be chosen independently from these C numbers.
    # Total triples = C^3

    count = 0
    # Iterate over residues r in [0, K-1] such that 2*r % K == 0
    # But we can compute directly: numbers x in [1, N] with 2x divisible by K
    # 2x = m*K => x = m*K/2
    # If K is even: x must be multiple of K/2
    # If K is odd: x must be multiple of K (since 2 and K coprime)
    
    if K % 2 == 0:
        step = K // 2
        count = (N // step)
    else:
        step = K
        count = (N // step)
    
    ans = count * count * count
    print(ans)

if __name__ == "__main__":
    solve()