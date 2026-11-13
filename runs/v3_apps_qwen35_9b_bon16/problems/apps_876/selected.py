import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    k = int(next(iterator))
    
    a = []
    for _ in range(n):
        a.append(int(next(iterator)))
    
    # Check if any element in A^0 is already >= k
    for x in a:
        if x >= k:
            print(0)
            return
    
    # The operation p(x) creates a prefix sum array of x.
    # If we apply p repeatedly i times, the result corresponds to the (i)-th order prefix sums.
    # The element at index j in A^i is sum_{t=0 to j} C(i+t, i) * A^0_t.
    # We need the maximum element in A^i to be >= k.
    # Since A^0 has at least two positive elements, the sequence of maximums will strictly increase.
    # The growth is polynomial of degree n (the size of the array), so the maximum value grows as O(i^n).
    # Given k up to 10^18 and n up to 200000, we cannot simulate.
    # However, the maximum value in A^i is dominated by the term with the largest coefficient and value.
    # Specifically, max(A^i) = max_{j} ( sum_{t=0}^j C(i+t, i) * A^0_t ).
    # Since A^0_t >= 0 and at least two are positive, the function f(i) = max(A^i) is strictly increasing.
    # We can use binary search on i.
    
    # Lower bound for i: 1 (since A^0 < k)
    # Upper bound: We need an i such that the value exceeds k.
    # The smallest non-zero term in the sum for large i is roughly A^0_t * i^t / t! for small t.
    # Even with just two positive numbers, the growth is super-linear.
    # For n=2, it's quadratic. For larger n, it's higher degree.
    # Let's estimate an upper bound.
    # Consider the case where we have two positive numbers 1 and 1 at the end.
    # The value grows like i^2 / 2. To reach 10^18, i ~ sqrt(2*10^18) ~ 1.4e9.
    # If n is large, say n=200000, and we have positive numbers at the start, it grows very fast (i^200000).
    # So the answer is small for large n.
    # A safe upper bound for binary search:
    # If n >= 2, the minimum growth is quadratic (from the two positive numbers eventually contributing).
    # Actually, if the positive numbers are at indices 0 and 1, the growth is O(i^2).
    # Max possible answer is around 2*10^9 (since even with i^2, (2e9)^2 = 4e18 > 10^18).
    # Let's set high = 2 * 10^9 + 7.
    
    low = 1
    high = 2000000007  # Sufficiently large upper bound
    ans = high
    
    while low <= high:
        mid = (low + high) // 2
        if check(mid, n, a, k):
            ans = mid
            high = mid - 1
        else:
            low = mid + 1
            
    print(ans)

def check(i, n, a, k):
    # Calculate the maximum element in A^i.
    # A^i[j] = sum_{t=0}^{j} C(i+t, i) * a[t]
    # We need to compute this efficiently for all j from 0 to n-1.
    # Note that C(i+t, i) = C(i+t, t).
    # Also, C(i+t, i) = C(i+t-1, i) * (i+t) / t ?? No.
    # C(n, k) = C(n-1, k) * n / (n-k)
    # Here we have C(i+t, i). Let's denote C_t = C(i+t, i).
    # C_t = C(i+t-1, i) * (i+t) / t = C_{t-1} * (i+t) / t.
    # Base case: t=0 -> C_0 = C(i, i) = 1.
    # t=1 -> C_1 = C(i+1, i) = i+1.
    # Recurrence: C_t = C_{t-1} * (i + t) // t. Since we are dealing with integers and the combinatorics guarantee integer results.
    # However, we need to compute sums.
    # A^i[j] = sum_{t=0}^j C_t * a[t].
    # We can compute prefix sums of (C_t * a[t]) on the fly.
    # But i can be up to 2e9, so we cannot precompute factorials or anything.
    # We compute C_t iteratively.
    # C_t grows very fast. We should stop if the current term exceeds k or the running sum exceeds k.
    # Wait, a[t] can be up to 10^9. C_t can be large.
    # We need to be careful with overflow in Python (it handles large ints automatically) but performance.
    # n is up to 200,000. We iterate t from 0 to n-1.
    # Inside the loop, we update C_t and add to current sum.
    # If current sum >= k, return True immediately.
    
    # Optimization: If C_t becomes huge, and a[t] > 0, the sum will quickly exceed k.
    # But we must be precise.
    
    current_C = 1  # C(i+0, i) = 1
    current_sum = 0
    
    # We can also check if i is very large such that even the first positive a[t] makes it >= k.
    # But let's just simulate the summation for the whole array.
    # Is O(n) per check acceptable?
    # Binary search range ~ 2e9 -> log2(2e9) ~ 31 iterations.
    # 31 * 200,000 = 6.2 million operations. This is well within time limits (usually 1-2 seconds for Python).
    
    for t in range(n):
        val = a[t]
        if val > 0:
            # Update current sum
            current_sum += current_C * val
            
            if current_sum >= k:
                return True
        
        # Update current_C for next iteration: C(i+t+1, i) from C(i+t, i)
        # C(i+t+1, i) = C(i+t, i) * (i + t + 1) / (t + 1)
        # We need to do integer division. Since it's a binomial coefficient, it's exact.
        if t + 1 < n: # We only need next C if there is a next element
            # Check for potential division issues? No, math guarantees divisibility.
            # However, intermediate calculation (current_C * (i + t + 1)) might be large.
            # Python handles large ints, but let's see if we can prune.
            # If current_C is already huge, we might not need exact value if we know it will exceed k.
            # But we need to multiply by val later.
            # Let's just compute.
            current_C = (current_C * (i + t + 1)) // (t + 1)
    
    return False

if __name__ == '__main__':
    solve()