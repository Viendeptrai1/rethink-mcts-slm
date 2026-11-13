import sys
from math import gcd
from functools import reduce

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)

    N = int(next(iterator))
    K = int(next(iterator))
    
    X = []
    for _ in range(K):
        X.append(int(next(iterator)))
        
    Q = int(next(iterator))
    
    queries = []
    for _ in range(Q):
        L = int(next(iterator))
        R = int(next(iterator))
        queries.append((L, R))
        
    # We need to compute the frequency of each index i being incremented.
    # An index i is incremented by a call with jump J if i % J == 0.
    # Since N, K up to 10^6, we cannot simulate the array directly if many updates hit same indices,
    # but actually the constraint is that we perform K updates.
    # However, simulating "for each X in X: for i in 0..N step X: arr[i]++" is O(N * K) in worst case (e.g., all X=1), which is 10^12 -> TLE.
    # We need a faster way.
    
    # Observation:
    # Instead of iterating over the array for each update, we can iterate over the updates and mark contributions?
    # No, that's what we are trying to avoid.
    #
    # Alternative approach:
    # For a fixed index i, how many times is it incremented?
    # count[i] = number of X_j such that i % X_j == 0.
    # This looks like a divisor sum problem.
    # We can invert the problem: For each X_j, it contributes +1 to indices 0, X_j, 2*X_j, ...
    # This is exactly what the problem statement says.
    #
    # Can we optimize the simulation?
    # If we have many small X_j, the loop is long. If we have large X_j, the loop is short.
    # Worst case is all X_j = 1, then we do N operations K times -> 10^12.
    # We need to group identical X_j values.
    # Let distinct_jumps be a frequency map of the jumps.
    # Then we only iterate for distinct jumps.
    # Sum of (N / x) for distinct x.
    # In worst case, distinct jumps are 1, 2, 3, ... M.
    # Sum N/i for i=1 to M is O(N log N).
    # Since K <= 10^6, the number of distinct jumps is at most min(N, K).
    # But wait, if K=10^6 and all X are distinct primes near 10^6? Then distinct count is 10^6, but each loop runs 1 time. Total ops = 10^6.
    # If K=10^6 and all X=1, distinct count = 1, loop runs N times. Total ops = N = 10^6.
    # What if K=10^6, and we have jumps 1, 2, 4, 8, ...? Distinct count ~20, total ops N/1 + N/2 + ... + N/2^20 ~ 2N.
    # The worst case for "sum of N/x" over distinct x in [1, N] is when we pick smallest x's.
    # The sum is bounded by N * (1 + 1/2 + 1/3 + ... + 1/M).
    # If we have all jumps from 1 to K (where K <= N), the sum is N * H_K ~ N log K.
    # With N, K = 10^6, N log K ~ 10^6 * 14 ~ 1.4 * 10^7 operations. This is well within time limits for Python (usually ~10^8 ops/sec, though Python is slower, 10^7 simple ops should pass in 1-2 sec).
    #
    # So the strategy:
    # 1. Count frequency of each jump value.
    # 2. For each unique jump value j, iterate i from 0 to N-1 with step j, adding freq[j] to seq[i].
    # 3. Build prefix sums of seq to answer range sum queries in O(1).
    #
    # Complexity: O(N log N + K + Q). This is efficient enough.

    # Step 1: Frequency of jumps
    from collections import Counter
    jump_counts = Counter(X)
    
    # Step 2: Build the array
    seq = [0] * N
    
    # Iterate over unique jumps
    for jump, count in jump_counts.items():
        # Optimization: if jump > N, loop doesn't run (though problem says X_i < N, so jump < N)
        # Indices: 0, jump, 2*jump, ...
        for i in range(0, N, jump):
            seq[i] += count
            
    # Step 3: Prefix sums
    # pref[i] = seq[0] + ... + seq[i]
    # Sum(L, R) = pref[R] - (pref[L-1] if L>0 else 0)
    
    pref = [0] * N
    current_sum = 0
    for i in range(N):
        current_sum += seq[i]
        pref[i] = current_sum
        
    # Step 4: Answer queries
    results = []
    for L, R in queries:
        if L == 0:
            results.append(pref[R])
        else:
            results.append(pref[R] - pref[L-1])
            
    # Output results
    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()