import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    robots = []
    for _ in range(N):
        x = int(next(iterator))
        d = int(next(iterator))
        robots.append((x, d))

    # Sort robots by coordinate X_i
    robots.sort(key=lambda p: p[0])

    MOD = 998244353

    # dp[i] = number of possible remaining sets considering robots i..N-1 (in sorted order)
    # However, the state needs to capture the "reach" of the activation chain.
    # 
    # Let's reframe: We process robots from right to left (largest X to smallest X).
    # When we are at robot i, we decide whether to activate it or not.
    # But the activation of a robot might trigger others to its right.
    # Actually, the problem asks for the number of possible *remaining* sets.
    # A set of robots remains if and only if we can choose an initial set of activations 
    # such that exactly those robots are NOT activated (directly or recursively).
    #
    # Alternative approach:
    # Consider the dependency graph. Robot i activates robot j if j is in [X_i, X_i + D_i).
    # Since robots move right, this is a DAG (no cycles because X_i < X_j implies i comes before j).
    # Actually, if X_i < X_j and X_j < X_i + D_i, then i activates j.
    #
    # We want to count the number of subsets S of {1..N} such that S is the set of robots 
    # that are NOT activated.
    # Let U be the set of all robots. Let A be the set of activated robots.
    # We want the number of possible sets U \ A.
    # This is equivalent to the number of possible sets A that can be formed.
    #
    # How is a set A formed?
    # We start with some initial set of activations I (non-empty or empty? The problem says 
    # "as long as there is a robot remaining", and we can do operations any number of times.
    # If we do 0 operations, A is empty. If we activate a set I, then A becomes the closure of I.
    # So any valid A must be the closure of some I.
    # Conversely, for any closed set A (meaning if i in A and i activates j, then j in A),
    # can we reach A? Yes, just activate all i in A.
    # But wait, the process is recursive: "if it touches another robot j... Robot j also gets activated".
    # This means if we activate a set I, the final set A is the smallest set such that I ⊆ A and A is closed.
    # Actually, the closure property is: if i is activated, and j is reachable from i (i.e., j in [X_i, X_i+D_i)),
    # then j is activated.
    # So A is closed if for every i in A, all j such that X_i <= X_j < X_i + D_i are also in A.
    #
    # We need to count the number of subsets A ⊆ {1..N} that are closed.
    #
    # Let's sort robots by X. Let the sorted robots be r_0, r_1, ..., r_{N-1}.
    # A set A is closed if for all i such that r_i ∈ A, and for all j > i such that r_j < r_i + D_i,
    # we must have r_j ∈ A.
    #
    # We can use DP. Process from right to left (largest X to smallest X).
    # Let dp[i] be the number of valid closed sets formed using robots from i to N-1.
    # When considering robot i:
    # Option 1: Robot i is NOT in the set A.
    #   Then there is no constraint imposed by i on robots to its right (since i is not active).
    #   The number of ways is dp[i+1].
    # Option 2: Robot i IS in the set A.
    #   Then all robots j > i such that X_j < X_i + D_i MUST be in A.
    #   Let next[i] be the smallest index j > i such that X_j >= X_i + D_i.
    #   Then all robots in range [i+1, next[i]-1] must be in A.
    #   Robots from next[i] to N-1 can be chosen freely (subject to their own closure constraints).
    #   The number of ways is dp[next[i]].
    #
    # So, dp[i] = dp[i+1] + dp[next[i]].
    # Base case: dp[N] = 1 (empty set of robots from N to N-1 is valid).
    #
    # Precomputation:
    # 1. Sort robots by X.
    # 2. For each i, find next[i] = first j > i such that X_j >= X_i + D_i.
    #    Since X is sorted, we can use binary search (bisect_left) on the X array.
    # 3. Compute dp backwards from N-1 to 0.
    #
    # The answer is dp[0].

    if N == 0:
        print(0)
        return

    # Extract X and D after sorting
    # robots is list of (x, d) sorted by x
    X = [r[0] for r in robots]
    # D is not needed explicitly after sorting, we just need X and D_i for each i
    D = [r[1] for r in robots]

    # Precompute next[i]
    # next[i] is the index of the first robot j > i such that X[j] >= X[i] + D[i]
    # If no such j exists, next[i] = N
    
    # We can use bisect_left on X to find the insertion point.
    # We need to search in X[i+1:] effectively, but bisect works on the whole array.
    # We want the first index j >= i+1 such that X[j] >= target.
    # bisect_left returns the first index where X[index] >= target.
    # We need to ensure index >= i+1. Since X is sorted, if the returned index is <= i, 
    # it means all elements are < target? No, X[i] < X[i]+D[i] is possible.
    # Actually, we search for value V = X[i] + D[i].
    # bisect_left(X, V) gives the first index k such that X[k] >= V.
    # Since X[i] < V (because D[i] >= 1), k will be > i.
    # So we can directly use bisect_left.
    
    import bisect

    next_idx = [0] * N
    for i in range(N):
        target = X[i] + D[i]
        # Find first j such that X[j] >= target
        k = bisect.bisect_left(X, target)
        if k < N:
            next_idx[i] = k
        else:
            next_idx[i] = N

    # DP
    # dp[i] = number of closed sets considering robots i..N-1
    # dp[N] = 1
    dp = [0] * (N + 1)
    dp[N] = 1

    for i in range(N - 1, -1, -1):
        # Option 1: i not in A
        ways1 = dp[i+1]
        # Option 2: i in A -> all j in [i+1, next_idx[i]-1] must be in A
        # The robots from next_idx[i] onwards are free to be chosen (subject to their own closure)
        ways2 = dp[next_idx[i]]
        
        total = (ways1 + ways2) % MOD
        dp[i] = total

    print(dp[0])

if __name__ == '__main__':
    solve()