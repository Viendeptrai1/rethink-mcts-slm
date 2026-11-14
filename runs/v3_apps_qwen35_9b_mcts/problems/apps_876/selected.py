import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # Check if initial array already satisfies the condition
    if max(a) >= k:
        print(0)
        return

    # We simulate the process.
    # A^i = p(A^{i-1})
    # p(x) computes prefix sums.
    # Since n is up to 200,000 and k up to 10^18, and values grow exponentially,
    # the number of steps will be small (logarithmic in k relative to the sum).
    # However, we must be careful: if all elements are 0 except one, growth is linear.
    # But the problem states "At least two elements of A^0 are positive".
    # This guarantees exponential growth eventually.
    
    # Let's verify the growth rate.
    # If we have at least two positive numbers, the sum of the array grows by a factor 
    # roughly equal to the number of positive elements or more in subsequent steps.
    # Specifically, the sum of A^i is the sum of prefix sums of A^{i-1}.
    # Sum(A^i) = Sum_{j=0}^{n-1} (i+1 - j) * A^{i-1}_j ? No.
    # Let S be the sum of elements in array x.
    # The sum of elements in p(x) is sum_{i=1}^{n} prefix_sum(i) = sum_{j=0}^{n-1} A_j * (n - j).
    # So the total sum multiplies by a factor related to n and the distribution.
    # With at least two positive numbers, the "moment" (weighted sum) increases significantly.
    # The maximum element will grow exponentially.
    
    # Simulation approach:
    # Construct the next array explicitly.
    # Since n is 2e5, O(n) per step is fine if the number of steps is small.
    # How many steps? If min positive is 1 and we have two of them, the sum roughly doubles or triples each step.
    # 10^18 is about 2^60. Even with factor 2, 60 steps * 200,000 = 12 million operations, which is fine in Python.
    
    current_a = a
    
    step = 0
    while True:
        # Check max in current_a
        if max(current_a) >= k:
            print(step)
            return
        
        # Compute next array: prefix sums
        # y[i] = sum(x[0]...x[i])
        # We can do this in O(n)
        new_a = [0] * (n + 1)
        current_sum = 0
        for i in range(n):
            current_sum += current_a[i]
            new_a[i] = current_sum
        new_a[n] = current_sum # The last element is the sum of all previous
        
        current_a = new_a
        step += 1
        
        # Safety break, though theoretically unreachable given constraints
        if step > 1000000:
            break

if __name__ == '__main__':
    solve()