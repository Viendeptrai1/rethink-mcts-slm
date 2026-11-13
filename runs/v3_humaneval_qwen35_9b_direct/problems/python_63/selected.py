from typing import List

def fibfib(n: int) -> int:
    """The FibFib number sequence is a sequence similar to the Fibbonacci sequnece that's defined as follows:
    fibfib(0) == 0
    fibfib(1) == 0
    fibfib(2) == 1
    fibfib(n) == fibfib(n-1) + fibfib(n-2) + fibfib(n-3).
    Please write a function to efficiently compute the n-th element of the fibfib number sequence.
    >>> fibfib(1)
    0
    >>> fibfib(5)
    4
    >>> fibfib(8)
    24
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    if n == 0:
        return 0
    if n == 1:
        return 0
    if n == 2:
        return 1
    
    # Initialize the first three values
    prev3 = 0  # fibfib(0)
    prev2 = 0  # fibfib(1)
    prev1 = 1  # fibfib(2)
    
    current = 0
    for i in range(3, n + 1):
        current = prev1 + prev2 + prev3
        # Shift the window
        prev3 = prev2
        prev2 = prev1
        prev1 = current
    
    return current