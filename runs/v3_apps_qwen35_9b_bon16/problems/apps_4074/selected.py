import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    t = int(next(iterator))
    
    results = []
    
    for _ in range(t):
        n = int(next(iterator))
        k = int(next(iterator))
        
        if k >= n:
            # We can buy exactly n shovels in one package of size n
            results.append(1)
        else:
            # We need to find the smallest divisor d of n such that d <= k
            # The number of packages will be n // d
            # To minimize packages, we need to maximize d (divisor of n, d <= k)
            
            # Check divisors from sqrt(n) down to 1
            best_d = 1
            limit = int(n**0.5)
            
            for i in range(limit, 0, -1):
                if n % i == 0:
                    d1 = i
                    d2 = n // i
                    
                    # Check d1
                    if d1 <= k:
                        best_d = max(best_d, d1)
                    # Check d2
                    if d2 <= k:
                        best_d = max(best_d, d2)
                    else:
                        # Since we are iterating downwards, once d2 > k, all larger divisors will also be > k
                        # But we must continue checking smaller divisors for d1 or other pairs
                        # Actually, if d2 > k, we just ignore d2. We still need to check if there's a larger valid divisor.
                        # However, since we start from sqrt, the first time we see a divisor d2 <= k, that is the largest possible divisor <= k?
                        # Not necessarily. Example: n=12, k=5. Divisors: 1,2,3,4,6,12. Valid <=5: 1,2,3,4. Max is 4.
                        # sqrt(12)=3. i=3: d1=3, d2=4. Both <=5. best_d becomes 4.
                        # i=2: d1=2, d2=6. d1<=5, d2>5. best_d remains 4.
                        # i=1: d1=1, d2=12. d1<=5. best_d remains 4.
                        # So logic holds.
                        pass
                
                if best_d > 1:
                    # Optimization: if we found a divisor d such that d*d == n, then d is the only candidate from this pair.
                    # If d*d < n, then d2 = n//d > d. If d2 <= k, then d2 is a better candidate than any d1 we will see later (since d1 decreases).
                    # So if we find a pair (d1, d2) with d2 <= k, then d2 is the largest possible divisor <= k because any other divisor <= k must be <= d2 (since d2 is the largest divisor <= sqrt(n) or we passed all larger ones).
                    # Actually, if d2 <= k, then d2 is the largest divisor <= k because any divisor > d2 must be > sqrt(n) and we would have encountered it as a d2 for a smaller d1 earlier? 
                    # No, we iterate d1 from sqrt down. The corresponding d2 goes from sqrt up.
                    # The largest divisor <= k could be either <= sqrt(n) or > sqrt(n).
                    # If there is a divisor > sqrt(n) that is <= k, the largest such divisor corresponds to the smallest divisor < sqrt(n).
                    # Our loop starts from sqrt(n) downwards. The first time we encounter a divisor d1, d2 = n//d1 is the largest divisor > sqrt(n).
                    # If d2 <= k, then d2 is the maximum possible divisor <= k (because any larger divisor would require a smaller d1, but d2 increases as d1 decreases; wait, d2 = n/d1, so as d1 decreases, d2 increases. So the first d2 we see that is <= k is the smallest d2? No.
                    # Let's re-evaluate.
                    # Divisors come in pairs (d, n/d).
                    # We want max d such that d <= k.
                    # If k >= n, answer is 1.
                    # If k < n, we look for largest divisor of n <= k.
                    # Let this max divisor be D.
                    # If D <= sqrt(n), then D is a divisor <= sqrt(n).
                    # If D > sqrt(n), then n/D < sqrt(n).
                    # We can iterate i from 1 to sqrt(n).
                    # If i divides n:
                    #   candidate1 = i
                    #   candidate2 = n // i
                    #   if candidate1 <= k: best = max(best, candidate1)
                    #   if candidate2 <= k: best = max(best, candidate2)
                    # To optimize, we can iterate i from sqrt(n) down to 1.
                    # First i that divides n:
                    #   d1 = i, d2 = n//i.
                    #   If d2 <= k, then d2 is the largest divisor <= k? 
                    #   Yes, because any divisor > d2 must be > sqrt(n). The divisors > sqrt(n) are of the form n/x where x < sqrt(n).
                    #   As x decreases from sqrt(n), n/x increases. So the largest divisor > sqrt(n) corresponds to the smallest x.
                    #   But we are iterating x (i) from sqrt(n) downwards. So the first divisor we find is the largest possible d1 (<= sqrt(n)) and consequently the smallest d2 (>= sqrt(n)).
                    #   Wait, we want the LARGEST divisor <= k.
                    #   If k is very large (>= n), answer 1.
                    #   If k is small, we need largest divisor <= k.
                    #   If there exists a divisor d > sqrt(n) such that d <= k, then the corresponding co-divisor x = n/d is < sqrt(n).
                    #   To maximize d, we need to minimize x.
                    #   So we should look for the smallest divisor x of n such that n/x <= k.
                    #   Alternatively, just iterate all divisors and pick max <= k. Since n <= 10^9, sqrt(n) <= 31622, which is fast enough.
                    #   So simply iterating from 1 to sqrt(n) is sufficient and correct.
                    pass
            
            # Re-implementing the loop clearly for correctness and simplicity given the constraint N <= 10^9
            best_d = 1
            limit = int(n**0.5)
            for i in range(1, limit + 1):
                if n % i == 0:
                    d1 = i
                    d2 = n // i
                    if d1 <= k:
                        if d1 > best_d:
                            best_d = d1
                    if d2 <= k:
                        if d2 > best_d:
                            best_d = d2
            
            results.append(n // best_d)

    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()