import sys

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
    
    # seq[i] will store how many times index i was incremented
    # Since N and K are up to 10^6, we cannot simulate the inner loop naively if jump is small.
    # However, the total number of operations is sum(N/jump) for each call.
    # In worst case (jump=1), this is O(N*K) which is 10^12 -> TLE.
    # We need a more efficient way to compute the final array or answer queries.
    
    # Observation:
    # The value at index i is the number of X_j such that i is divisible by X_j.
    # Let count[j] be the number of times jump value j appears in X.
    # Then seq[i] = sum(count[j] for j in divisors of i).
    # We can precompute the frequency of each jump value.
    # Then for each i from 0 to N-1, compute seq[i] by summing counts of its divisors.
    # But computing divisors for each i up to 10^6 might be slow if not optimized.
    # Alternatively, we can iterate over each unique jump value 'j' and add its count to all multiples of j.
    # This is a harmonic series approach: sum(N/j) for all unique j.
    # Since sum(N/j) for j=1..N is O(N log N), this is efficient enough (10^6 * 14 approx).
    
    # Step 1: Count frequencies of each jump
    jump_counts = {}
    for x in X:
        jump_counts[x] = jump_counts.get(x, 0) + 1
    
    # Step 2: Compute seq array
    # seq[i] = sum of jump_counts[j] for all j that divide i
    # We do this by iterating over each unique jump j and adding its count to multiples of j.
    seq = [0] * N
    for j, count in jump_counts.items():
        # Add 'count' to seq[j], seq[2j], seq[3j], ...
        for idx in range(j, N, j):
            seq[idx] += count
            
    # Step 3: Build prefix sums for range sum queries
    # prefix[i] = seq[0] + ... + seq[i]
    # Sum(L, R) = prefix[R] - (prefix[L-1] if L>0 else 0)
    prefix = [0] * N
    current_sum = 0
    for i in range(N):
        current_sum += seq[i]
        prefix[i] = current_sum
        
    # Step 4: Answer queries
    results = []
    for _ in range(Q):
        L = int(next(iterator))
        R = int(next(iterator))
        if L == 0:
            results.append(str(prefix[R]))
        else:
            results.append(str(prefix[R] - prefix[L-1]))
            
    print('\n'.join(results))

if __name__ == '__main__':
    solve()