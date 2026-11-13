import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])

    # We need a, b, c such that:
    # a + b ≡ 0 (mod K)
    # b + c ≡ 0 (mod K)
    # c + a ≡ 0 (mod K)
    #
    # Adding all three: 2(a + b + c) ≡ 0 (mod K)
    # From a+b ≡ 0 => b ≡ -a
    # From b+c ≡ 0 => c ≡ -b = a
    # Then c+a = 2a ≡ 0 (mod K)
    # So a must satisfy 2a ≡ 0 (mod K) and then b = -a mod K, c = a mod K.
    #
    # Thus, for a given a, b and c are uniquely determined modulo K.
    # Specifically:
    # a ≡ r (mod K)
    # b ≡ -r (mod K) ≡ (K - r) % K
    # c ≡ r (mod K)
    # And we also need 2a ≡ 0 (mod K), which implies 2r ≡ 0 (mod K).
    #
    # So r must be a multiple of K / gcd(2, K).
    # Let g = gcd(2, K). Then r must be a multiple of K/g.
    # The possible values for r in [1, K] are: K/g, 2*K/g, ..., (g)*K/g = K.
    # There are exactly g such values.
    #
    # However, we need to count how many a in [1, N] have a % K == r for each valid r.
    # For a fixed remainder r (1 <= r <= K), the number of a in [1, N] with a % K == r is:
    #   count = N // K
    #   if r <= N % K: count += 1
    # But note: if r == 0, we treat it as K for positive integers.
    #
    # Actually, let's reframe:
    # a % K can be in [0, K-1]. But since a is positive, if a % K == 0, then a is a multiple of K.
    # Let's define rem = a % K. If rem == 0, we can consider it as K for symmetry, but mathematically:
    # Conditions:
    #   a + b = m1 * K
    #   b + c = m2 * K
    #   c + a = m3 * K
    # => 2(a+b+c) = (m1+m2+m3)*K => a+b+c must be a multiple of K/gcd(2,K).
    #
    # Simpler approach:
    # From the equations, we deduced:
    #   a ≡ c (mod K)
    #   b ≡ -a (mod K)
    #   and 2a ≡ 0 (mod K)
    #
    # So a must be such that 2a is divisible by K.
    # Let g = gcd(2, K). Then a must be a multiple of K/g.
    # Let M = K // g. Then a must be a multiple of M.
    # Also, once a is chosen, b is determined as (-a mod K) and c = a mod K (but we take positive representatives).
    # However, note that b and c must also be in [1, N].
    #
    # Actually, the constraints on a, b, c are:
    #   a in [1, N], b in [1, N], c in [1, N]
    #   a ≡ c (mod K)
    #   b ≡ -a (mod K)
    #   2a ≡ 0 (mod K)
    #
    # So the valid a's are multiples of M = K // gcd(2, K).
    # For each such a, b is uniquely determined modulo K: b ≡ (-a) mod K.
    # But note: if a is a multiple of M, then 2a is a multiple of K, so -a mod K is well-defined.
    # Specifically, let r = a % K. Then b % K = (K - r) % K.
    # And c % K = r.
    #
    # However, we must count the number of a in [1, N] such that:
    #   1. 2a is divisible by K
    #   2. The corresponding b = some value in [1, N] with b % K = (K - (a%K)) % K
    #   3. The corresponding c = some value in [1, N] with c % K = (a%K)
    #
    # But note: the condition "2a divisible by K" is necessary and sufficient for the existence of b and c modulo K.
    # However, for a fixed a satisfying 2a ≡ 0 (mod K), the required residues for b and c are fixed.
    # Let r = a % K. Then we need:
    #   b ≡ -r (mod K)  => b = k1*K + (K-r) if r != 0, or b = k1*K if r==0.
    #   c ≡ r (mod K)   => c = k2*K + r.
    #
    # The number of b in [1, N] with b % K = (K-r)%K is the same as the number of integers in [1, N] congruent to a fixed residue modulo K.
    # Similarly for c.
    #
    # However, note that if r = 0, then (K-r)%K = 0. So the residue is 0.
    #
    # Let's define:
    #   count_residue(x) = number of integers in [1, N] such that x % K == (x % K) [but note: if x%K==0, then multiples of K]
    # Actually, for a residue r in [0, K-1]:
    #   The number of a in [1, N] with a % K == r is:
    #      base = N // K
    #      rem = N % K
    #      if r == 0:
    #          return base + (1 if rem >= K else 0) -> but rem < K, so actually if r==0, we count multiples: base, and if N is multiple of K then the last one is included? 
    #      Actually, simpler: 
    #          The residues of 1, 2, ..., N mod K are:
    #          1, 2, ..., K-1, 0, 1, 2, ..., 
    #          The number of times residue r appears (for r in [0, K-1]):
    #          Let full_cycles = N // K
    #          Let extra = N % K
    #          Then for r in [1, extra]: count = full_cycles + 1
    #          For r in [extra+1, K-1]: count = full_cycles
    #          For r = 0: count = full_cycles + (1 if extra == 0? no) -> actually residue 0 appears at K, 2K, ...
    #          The number of multiples of K in [1, N] is N // K.
    #          So for r=0: count = N // K.
    #          For r in [1, K-1]:
    #              count = N // K + (1 if r <= N % K else 0)
    #
    # So:
    #   def count_residue(r):
    #       if r == 0:
    #           return N // K
    #       else:
    #           return N // K + (1 if r <= N % K else 0)
    #
    # Now, the valid a's are those with 2a ≡ 0 (mod K).
    # Let M = K // gcd(2, K). Then a must be a multiple of M.
    # But note: a % K must be one of the residues that satisfy 2*(a%K) ≡ 0 (mod K).
    # Let r = a % K. Then 2r ≡ 0 (mod K) => r = 0 or r = K/2 (if K is even).
    # So there are two cases:
    #   Case 1: K is odd. Then 2r ≡ 0 (mod K) => r ≡ 0 (mod K). So only r=0 is valid.
    #   Case 2: K is even. Then 2r ≡ 0 (mod K) => r = 0 or r = K/2.
    #
    # Therefore:
    #   If K is odd:
    #       Only r = 0 is allowed for a.
    #       Then b must have residue 0 (since -0 = 0) and c must have residue 0.
    #       So a, b, c must all be multiples of K.
    #       Number of a in [1, N] with a%K==0: cnt0 = N // K.
    #       Total triples = cnt0 * cnt0 * cnt0.
    #
    #   If K is even:
    #       Two possibilities for r: 0 and K/2.
    #       Subcase r=0:
    #           a % K = 0 => b % K = 0, c % K = 0.
    #           Count for a: cnt0 = N // K.
    #           Count for b: cnt0.
    #           Count for c: cnt0.
    #           Triples from r=0: cnt0^3.
    #       Subcase r = K/2:
    #           a % K = K/2 => b % K = (K - K/2) % K = K/2, c % K = K/2.
    #           So a, b, c must all be ≡ K/2 (mod K).
    #           Count for a: cnt_half = count_residue(K/2)
    #           Similarly for b and c: cnt_half.
    #           Triples from r=K/2: cnt_half^3.
    #       Total = cnt0^3 + cnt_half^3.
    #
    # But wait: is it possible that a has residue 0 and b has residue K/2? 
    # No, because if a % K = 0, then b % K must be 0 (since b ≡ -a). 
    # And if a % K = K/2, then b % K must be K/2.
    # So the two cases are disjoint and cover all possibilities.
    #
    # Therefore, algorithm:
    #   cnt0 = N // K
    #   if K is odd:
    #       ans = cnt0 ** 3
    #   else:
    #       r_half = K // 2
    #       cnt_half = N // K + (1 if r_half <= N % K else 0)
    #       ans = cnt0 ** 3 + cnt_half ** 3
    #
    # Let's test with sample: N=3, K=2.
    #   K is even.
    #   cnt0 = 3 // 2 = 1.
    #   r_half = 1.
    #   cnt_half = 3 // 2 + (1 if 1 <= 3%2=1 else 0) = 1 + 1 = 2.
    #   ans = 1^3 + 2^3 = 1 + 8 = 9. Matches sample.
    #
    # Another test: N=2, K=4.
    #   K even.
    #   cnt0 = 2//4 = 0.
    #   r_half = 2.
    #   cnt_half = 2//4 + (1 if 2<=2%4=2 else 0) = 0+1=1.
    #   ans = 0 + 1 = 1.
    #   Check: triples (a,b,c) in [1,2]^4 such that a+b, b+c, c+a divisible by 4.
    #   Only possibility: a=2, b=2, c=2 -> 2+2=4, 2+2=4, 2+2=4. Yes.
    #   Are there others? 
    #   If a=1: then b must be 3 mod 4 -> not in [1,2]. So no.
    #   So 1 is correct.
    #
    # Another test: N=4, K=4.
    #   cnt0 = 4//4=1.
    #   r_half=2.
    #   cnt_half = 4//4 + (1 if 2<=0? no, 4%4=0) -> 1 + 0 = 1? 
    #   Wait: N%K = 0. So r_half=2 <= 0? False. So cnt_half=1.
    #   But residues in [1,4]: 
    #       1%4=1, 2%4=2, 3%4=3, 4%4=0.
    #       So residue 2 appears once (at 2). 
    #   So cnt_half=1.
    #   ans = 1^3 + 1^3 = 2.
    #   Triples: 
    #       (4,4,4) -> 8,8,8 divisible by 4? yes.
    #       (2,2,2) -> 4,4,4 divisible by 4? yes.
    #       Any others? 
    #       If a=4, then b=4, c=4.
    #       If a=2, then b=2, c=2.
    #       So 2 is correct.
    #
    # Another test: N=5, K=4.
    #   cnt0 = 5//4=1.
    #   r_half=2.
    #   N%K=1. 2<=1? False -> cnt_half=1.
    #   ans = 1+1=2.
    #   Residues: 1,2,3,0,1 -> residue 2 appears once (at 2). residue 0 appears once (at 4).
    #   So only (2,2,2) and (4,4,4). Correct.
    #
    # N=6, K=4.
    #   cnt0 = 6//4=1.
    #   r_half=2.
    #   N%K=2. 2<=2 -> True -> cnt_half=1+1=2.
    #   ans = 1 + 8 = 9.
    #   Residues: 1,2,3,0,1,2 -> residue 2 appears at 2 and 6 -> 2 times.
    #   residue 0 appears at 4 -> 1 time.
    #   So (4,4,4) -> 1 triple.
    #   (2,2,2), (6,6,6) -> 2^3=8 triples.
    #   Total 9. Correct.

    if K % 2 == 1:
        cnt0 = N // K
        ans = cnt0 ** 3
    else:
        cnt0 = N // K
        r_half = K // 2
        rem = N % K
        cnt_half = cnt0 + (1 if r_half <= rem else 0)
        ans = cnt0 ** 3 + cnt_half ** 3

    print(ans)

if __name__ == '__main__':
    solve()