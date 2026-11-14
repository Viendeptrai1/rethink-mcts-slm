import sys
from sys import stdin

def solve():
    input_data = stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
        
        # We need to count how many times each index is updated.
        # Instead of simulating the process which would be O(N*K) and too slow,
        # we can use a difference array approach or simply accumulate counts.
        # However, N and K are up to 10^6, so O(N*K) is definitely TLE.
        # The constraints suggest an O(N + K) or O((N+K) log N) solution.
        
        # Let's re-evaluate the problem.
        # We have K operations. Each operation j adds 1 to indices 0, j, 2j, ...
        # We need to answer Q range sum queries on the final array.
        # The maximum value of an element can be K. The sum can be large, so use 64-bit integers.
        
        # Direct simulation:
        # For each jump X_i, we iterate 0, X_i, 2X_i...
        # Total operations = N/1 + N/2 + ... + N/K in worst case? No.
        # Total operations = sum(N // X_i). If all X_i = 1, total is N*K = 10^12 -> TLE.
        # We need a faster way to compute the final array values.
        
        # Observation:
        # The value at index i is the number of divisors of i (including 0? No, 0 is special)
        # plus the number of times 0 was updated.
        # Actually, for a specific jump X, index i is updated if i % X == 0.
        # So seq[i] = count of X_j such that X_j divides i (for i > 0).
        # For i = 0, it is updated for every X_j, so seq[0] = K.
        
        # So for i > 0: seq[i] = number of X_j in the input list that divide i.
        # This is equivalent to: for each distinct value v in X, if v divides i, add count[v].
        
        # Algorithm:
        # 1. Count frequency of each jump size in the input. Let this be freq[v].
        # 2. Create an array `counts` of size N+1 initialized to 0.
        # 3. For each distinct jump size v present in input:
        #      For each multiple m = v, 2v, 3v, ... < N:
        #          counts[m] += freq[v]
        # 4. Set counts[0] = K.
        # 5. Compute prefix sums of `counts` to answer range sum queries in O(1).
        #    prefix[i] = sum(counts[0]...counts[i])
        #    Query(L, R) = prefix[R] - prefix[L-1] (if L>0 else prefix[R])
        
        # Complexity:
        # Step 3 iterates N/v for each distinct v.
        # Sum of N/v over all v <= N is O(N log N) (harmonic series).
        # Since we only iterate over distinct v present in input, it's bounded by O(N log N).
        # With N=10^6, N log N is approx 2*10^7 operations, which fits within time limits (usually 1-2 sec).
        
        freq = [0] * (N + 1)
        for _ in range(K):
            x = int(next(iterator))
            freq[x] += 1
            
        counts = [0] * (N + 1)
        
        # Process each distinct jump size
        for v in range(1, N + 1):
            if freq[v] == 0:
                continue
            c = freq[v]
            # Add c to all multiples of v
            for m in range(v, N + 1, v):
                counts[m] += c
        
        # Handle index 0 separately as per problem statement (i starts at 0)
        counts[0] = K
        
        # Compute prefix sums
        # prefix[i] will store sum(counts[0]...counts[i])
        prefix = [0] * (N + 1)
        current_sum = 0
        for i in range(N + 1):
            current_sum += counts[i]
            prefix[i] = current_sum
            
        Q = int(next(iterator))
        output = []
        
        for _ in range(Q):
            L = int(next(iterator))
            R = int(next(iterator))
            
            if L == 0:
                ans = prefix[R]
            else:
                ans = prefix[R] - prefix[L-1]
            output.append(str(ans))
            
        sys.stdout.write('\n'.join(output) + '\n')
        
    except StopIteration:
        pass

if __name__ == '__main__':
    solve()