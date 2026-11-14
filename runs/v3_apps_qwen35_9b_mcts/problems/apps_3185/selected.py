import sys
import math

def solve():
    try:
        line = sys.stdin.read().strip()
        if not line:
            return
        n_fact_str = line
    except Exception:
        return

    if n_fact_str == "1":
        print(1)
        return

    num_digits = len(n_fact_str)

    # Stirling's approximation for log10(n!)
    # log10(n!) ≈ log10(sqrt(2*pi*n)) + n*log10(n/e)
    # We solve for n such that log10(n!) ≈ num_digits - 1 (since log10(x) = d-1 means x has d digits)
    # Actually, if x has D digits, then D-1 <= log10(x) < D.
    # So we target log10(n!) ≈ num_digits - 1.

    # Initial guess using the simplified form: n * log10(n/e) ≈ num_digits
    # Let's use a binary search approach with Stirling's formula for efficiency and precision.
    # Range for n:
    # 1! = 1 (1 digit)
    # 21! has 20 digits (example in problem)
    # 10^6 digits implies n is roughly 550,000 (since log10(n!) ~ n log10 n)
    # Upper bound: if n = 10^6, log10(n!) ~ 10^6 * 6 = 6*10^6 digits, which is way too big.
    # If digits = 10^6, n is approx 550,000.
    # Let's set a safe upper bound.
    # log10(n!) ~ n log10(n) - n log10(e)
    # If n = 1,000,000, log10(n!) ~ 10^6 * 6 - 434294 = 5.5*10^6 digits.
    # So for 10^6 digits, n is definitely less than 1,000,000.
    # Let's use binary search between 1 and 2,000,000 to be safe.

    low = 1
    high = 2000000
    best_n = 1

    # We need a function to compute log10(n!) using Stirling's approximation
    def stirling_log10_fact(n):
        if n <= 1:
            return 0.0
        # Stirling's series: ln(n!) ≈ (n + 0.5)ln(n) - n + 0.5*ln(2*pi) + 1/(12n) - ...
        # We need log10, so divide by ln(10)
        ln_2pi = math.log(2 * math.pi)
        ln_10 = math.log(10)
        ln_n = math.log(n)
        # First few terms of Stirling's approximation
        val = (n + 0.5) * ln_n - n + 0.5 * ln_2pi
        # Add correction term 1/(12n) for better accuracy
        val += 1.0 / (12.0 * n)
        # Subtract next term 1/(360n^3) if needed, but 1/(12n) is usually enough for this range
        # Convert to log10
        return val / ln_10

    # Binary search for n such that log10(n!) is closest to num_digits - 1
    # Actually, we want the smallest n such that log10(n!) >= num_digits - 1?
    # No, we want the n where the number of digits matches exactly.
    # Number of digits D = floor(log10(n!)) + 1.
    # So we want floor(log10(n!)) + 1 == num_digits
    # => log10(n!) >= num_digits - 1 and log10(n!) < num_digits
    
    # Let's find n such that stirling_log10_fact(n) is approximately num_digits - 1
    target = num_digits - 1.0
    
    # Binary search
    while low <= high:
        mid = (low + high) // 2
        est = stirling_log10_fact(mid)
        if est < target:
            low = mid + 1
        else:
            high = mid - 1
            best_n = mid

    # Now best_n is the candidate. Let's verify by computing the actual factorial of best_n
    # and checking the number of digits. Since best_n is at most ~600,000, computing factorial directly
    # might be slow if we do it naively, but Python handles large integers well.
    # However, computing factorial of 600,000 takes significant time and memory.
    # We need a more robust check or a tighter estimate.
    
    # Alternative: The problem states the input is a valid factorial.
    # So there exists an exact n. Our Stirling approximation should get us very close.
    # Let's check best_n, best_n-1, best_n+1 to be sure.
    
    candidates = []
    for cand in [best_n - 1, best_n, best_n + 1]:
        if cand < 1:
            continue
        # Compute log10 of factorial precisely? No, too slow.
        # Just compute the number of digits of cand! by computing cand! and len(str(cand!))
        # But computing 600,000! is heavy.
        # Let's rely on the fact that Stirling is very accurate.
        # The error in Stirling for n=10^5 is negligible for integer part.
        # Let's just compute the factorial for the candidate that is closest to the target.
        pass

    # Re-evaluating the strategy:
    # Instead of full factorial computation which is O(n^2) or worse in multiplication steps,
    # we can use the property that the input is guaranteed to be a factorial.
    # We can compute the factorial iteratively and compare the number of digits at each step?
    # No, that's still slow for large n.
    
    # Wait, the constraints say "number of digits of n! is at most 10^6".
    # This means n! has up to 1,000,000 digits.
    # n is approximately 550,000.
    # Computing 550,000! in Python:
    # Python's int multiplication is efficient (Karatsuba/FFT for very large numbers).
    # Computing 550,000! might take a few seconds, which is acceptable for a single test case.
    # Let's try to compute the factorial of the estimated n and check the length.
    
    # To optimize, we can compute the factorial of the candidate and check its length.
    # If the length matches, we are done.
    # If not, we adjust.
    
    # Let's refine the binary search to find the n where len(str(factorial(n))) == num_digits
    # But we can't compute factorial inside the binary search loop because it's expensive.
    # We only compute it once for the final candidate.
    
    # Let's assume the Stirling approximation gives us the correct n or off by 1.
    # We will test best_n, best_n-1, best_n+1.
    
    final_n = -1
    
    # We need a function to compute factorial and check length
    def check_and_verify(n):
        # Compute factorial
        f = 1
        for i in range(2, n + 1):
            f *= i
        return len(str(f))

    # Test candidates
    for cand in [best_n - 1, best_n, best_n + 1]:
        if cand < 1:
            continue
        # Optimization: if we already found a match, break
        if final_n != -1:
            break
        # Check length
        # To avoid full computation if possible, we can check log10 sum?
        # No, we need exact length.
        # Let's compute.
        # Note: For very large n, this might be slow, but given the problem constraints and typical time limits,
        # and the fact that we only do this once (or twice), it should pass.
        # However, if the input is huge (10^6 digits), computing the factorial string might be slow due to string conversion.
        # We can check the length without converting to string?
        # len(str(f)) is O(digits). Converting int to string is O(digits^1.58) or similar.
        # With 10^6 digits, this is heavy.
        # Is there a way to avoid full string conversion?
        # We can use the fact that we know the input string.
        # We can compute the factorial and compare it to the input string directly?
        # Comparing two large integers is faster than converting to string.
        # But we need to know if the length matches first.
        # Actually, if we compute the factorial, we can just compare it to the input integer.
        # But converting the input string to int is also expensive (O(digits^2) or O(digits^1.58)).
        # However, Python's int(str) is optimized.
        
        # Let's try to compute the factorial and compare.
        # If the length of the computed factorial matches num_digits, then we check if it equals the input.
        # But wait, the problem says "You are given the value of n!".
        # So the input IS the factorial.
        # We just need to find n.
        # So if we compute factorial(cand) and its length is num_digits, then cand is the answer.
        # Because factorials are unique and strictly increasing.
        # So we don't need to compare the value, just the length!
        # Because if len(factorial(cand)) == num_digits, then cand must be the n.
        # (Since factorial is monotonic, and the input is a valid factorial, there's only one n with that many digits).
        
        # So the check is simply: len(str(factorial(cand))) == num_digits
        # But computing factorial(cand) and converting to string is the bottleneck.
        # Can we compute the number of digits of n! without computing n!?
        # Yes, using log10 sum.
        # digits = floor(sum(log10(i) for i in 1..n)) + 1
        # This is O(n). For n=550,000, this is 550,000 operations, which is very fast.
        # This avoids large integer arithmetic entirely!
        
        # Let's implement this log-sum method for verification.
        pass

    # Revised plan:
    # 1. Estimate n using Stirling's approximation and binary search.
    # 2. Verify the estimate by computing sum(log10(i)) for i from 1 to n and checking if floor(sum) + 1 == num_digits.
    # This is O(n) and avoids large numbers.
    
    # Let's implement the verification function
    def verify_digits(n):
        if n == 1:
            return 1
        # Compute sum of log10(i)
        # We can use math.lgamma for log10(n!) directly?
        # math.lgamma(n+1) returns ln(n!)
        # log10(n!) = ln(n!) / ln(10)
        # This is O(1) and very accurate!
        # Let's use lgamma.
        ln_fact = math.lgamma(n + 1)
        log10_fact = ln_fact / math.log(10)
        digits = int(math.floor(log10_fact)) + 1
        return digits

    # Now we can verify the candidate in O(1)
    for cand in [best_n - 1, best_n, best_n + 1]:
        if cand < 1:
            continue
        if verify_digits(cand) == num_digits:
            print(cand)
            return

    # Fallback if lgamma is not precise enough (unlikely for this range)
    # Or if the binary search was off.
    # We can do a linear scan around best_n if needed, but lgamma should be precise.
    # Let's add a small loop just in case.
    start = max(1, best_n - 5)
    for cand in range(start, best_n + 6):
        if verify_digits(cand) == num_digits:
            print(cand)
            return

if __name__ == "__main__":
    solve()