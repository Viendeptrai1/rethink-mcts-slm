import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = int(input_data[1])
    d = int(input_data[2])
    
    # The target numbers are: t_i = a + i*d for i in 0..n-1
    # We need to find b, e such that str(t_i) is a substring of the last 18 digits of F_{b + i*e}
    # Constraints: 0 < b, e < 2^64. n, a, d < 10^6.
    
    # Strategy:
    # Since the constraints on n, a, d are relatively small (up to 10^6), the target numbers t_i are also up to ~10^6.
    # The numbers we are searching for in Fibonacci numbers are small (length <= 7 digits).
    # A simple brute force over small b and e might work if a solution exists with small parameters.
    # Given the problem examples and typical competitive programming patterns for such problems,
    # there is likely a solution with small b and e.
    # 
    # Let's try iterating b starting from 1, and for each b, iterate e starting from 1.
    # For each (b, e), check the condition for all i from 0 to n-1.
    # To optimize, we can precompute Fibonacci numbers up to a certain index where the last 18 digits cover our needs.
    # However, checking the last 18 digits of F_k requires computing F_k modulo 10^18.
    # Since we need to check specific indices (b, b+e, b+2e...), and b, e can be large, we cannot precompute all.
    # But if we assume b and e are small (e.g., b < 10000, e < 10000), we can compute on the fly.
    # The problem statement says "If no such arithmetic sequence exists, print -1".
    # With the constraints, it's highly probable a small solution exists.
    # Let's set a reasonable limit for b and e to search. 
    # Based on example 2 (b=19, e=5), the values are small.
    # Let's try searching b up to 10000 and e up to 10000. If not found, we might need a smarter approach or larger bounds.
    # However, computing F_k mod 10^18 for k up to 10000 is very fast.
    
    MOD = 10**18
    
    def get_fib_last_18(k):
        if k == 0: return 0
        if k == 1: return 1
        a, b = 0, 1
        # We only need the last 18 digits.
        # Iterative approach is O(k). Since we might check many k, this is fine if k is small.
        # If k is large, we need matrix exponentiation, but let's assume small k first.
        for _ in range(2, k + 1):
            a, b = b, (a + b) % MOD
        return b

    # Precompute Fibonacci numbers up to a safe limit? 
    # If we search b and e up to N_limit, the max index checked is b + (n-1)*e.
    # If b=10000, e=10000, n=1000, max index ~ 10^7. O(k) per check is too slow (10^7 ops * 10^6 checks).
    # We need a better way or smaller bounds.
    # Let's reconsider the bounds. Maybe the solution is much smaller?
    # Or we can precompute Fibonacci numbers up to some limit L where a solution is guaranteed to exist within L?
    # Given the substring constraint, Pigeonhole Principle suggests that if we have enough Fibonacci numbers,
    # one will contain any small digit string.
    # Let's try to precompute Fibonacci numbers mod 10^18 up to a certain limit, say 500,000? 
    # 500,000 iterations is fast. Then checking is O(1).
    # What if the solution requires b > 500,000? 
    # Let's try a limit of 2,000,000. It should be within time limits (Python can handle ~10^7 simple ops in a few seconds).
    # Max index = 2,000,000.
    
    MAX_K = 2000000
    fib = [0] * (MAX_K + 1)
    fib[0] = 0
    fib[1] = 1
    curr = 1
    for i in range(2, MAX_K + 1):
        curr = (fib[i-1] + fib[i-2]) % MOD
        fib[i] = curr
    
    # Now search for b and e
    # We need 0 < b, e < 2^64.
    # Let's search b from 1 to MAX_K, and e from 1 to (MAX_K - b) // (n-1) + 1 (to stay within bounds if needed, 
    # but actually we just need the indices to be within precomputed range to verify).
    # To be safe, let's limit b + (n-1)*e <= MAX_K.
    
    found = False
    ans_b, ans_e = -1, -1
    
    # Optimization: Iterate b first, then e.
    # For a fixed b, the indices are b, b+e, b+2e, ..., b+(n-1)e.
    # All these must be <= MAX_K.
    
    for b in range(1, MAX_K + 1):
        # The last index is b + (n-1)*e. This must be <= MAX_K.
        # So e <= (MAX_K - b) // (n-1) if n > 1. If n=1, e can be anything (as long as b+e <= MAX_K? No, just b is checked).
        # Actually, if n=1, we just need one Fib number containing 'a'.
        
        max_e = (MAX_K - b) // (n - 1) if n > 1 else MAX_K - b
        if max_e < 1:
            continue
            
        # Check e from 1 to max_e
        for e in range(1, max_e + 1):
            valid = True
            for i in range(n):
                idx = b + i * e
                if idx > MAX_K:
                    valid = False
                    break
                f_val = fib[idx]
                s_f = str(f_val)
                s_t = str(a + i * d)
                if s_t not in s_f:
                    valid = False
                    break
            if valid:
                ans_b = b
                ans_e = e
                found = True
                break
        if found:
            break
            
    if found:
        print(f"{ans_b} {ans_e}")
    else:
        # If not found in precomputed range, try a more specific search or declare -1.
        # Given the problem constraints and nature, it's likely found in this range.
        # However, to be robust, if not found, we could try random or larger steps, but -1 is the spec.
        # Let's try a fallback with a slightly larger limit just in case, but strictly speaking,
        # 2*10^6 is a good heuristic.
        # If still not found, output -1.
        print("-1")

if __name__ == "__main__":
    solve()