from typing import List

def fib4(n: int) -> int:
    """The Fib4 number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fib4(0) -> 0
    fib4(1) -> 0
    fib4(2) -> 2
    fib4(3) -> 0
    fib4(n) -> fib4(n-1) + fib4(n-2) + fib4(n-3) + fib4(n-4).
    Please write a function to efficiently compute the n-th element of the fib4 number sequence.  Do not use recursion.
    >>> fib4(5)
    4
    >>> fib4(6)
    8
    >>> fib4(7)
    14
    """
    if n == 0:
        return 0
    if n == 1:
        return 0
    if n == 2:
        return 2
    if n == 3:
        return 0
    
    # Initialize the first four values
    # We use a list to store the last 4 values to compute the next one
    # dp[i] represents fib4(i)
    dp = [0, 0, 2, 0]
    
    # Start computing from index 4 up to n
    for i in range(4, n + 1):
        # fib4(i) = fib4(i-1) + fib4(i-2) + fib4(i-3) + fib4(i-4)
        # Since we only need the last 4 values, we can compute the next value
        # and update our list. However, to keep it simple and clear, we'll just use a list
        # that grows or we can use a fixed size window.
        # Let's use a fixed size window of 4.
        # current = dp[0] + dp[1] + dp[2] + dp[3]
        # Then shift: dp[0] becomes dp[1], dp[1] becomes dp[2], etc.
        # But wait, the definition is:
        # fib4(4) = fib4(3) + fib4(2) + fib4(1) + fib4(0) = 0 + 2 + 0 + 0 = 2
        # fib4(5) = fib4(4) + fib4(3) + fib4(2) + fib4(1) = 2 + 0 + 2 + 0 = 4
        # fib4(6) = fib4(5) + fib4(4) + fib4(3) + fib4(2) = 4 + 2 + 0 + 2 = 8
        # fib4(7) = fib4(6) + fib4(5) + fib4(4) + fib4(3) = 8 + 4 + 2 + 0 = 14
        
        # So the recurrence holds.
        # We can maintain a list of the last 4 values.
        # Let's say our list `window` holds [fib4(i-4), fib4(i-3), fib4(i-2), fib4(i-1)]
        # Then fib4(i) = sum(window)
        # And the new window becomes [fib4(i-3), fib4(i-2), fib4(i-1), fib4(i)]
        
        # Initial window for i=4: [fib4(0), fib4(1), fib4(2), fib4(3)] = [0, 0, 2, 0]
        # This matches our initial `dp` list.
        
        current = sum(dp)
        # Shift the window: remove the first element, append the new one
        dp.pop(0)
        dp.append(current)
        
    return dp[-1]