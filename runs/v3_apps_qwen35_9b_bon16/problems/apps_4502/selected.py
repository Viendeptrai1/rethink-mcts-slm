import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:]))
    
    # We will simulate the process but optimize the reversals.
    # Instead of actually reversing the list (O(n^2)), we use a deque and a boolean flag.
    # The flag indicates whether the current logical sequence is reversed relative to the deque.
    
    from collections import deque
    dq = deque()
    is_reversed = False  # False means the front of the deque is the start of b
    
    for x in a:
        if is_reversed:
            # Current state is reversed, so appending to end means appending to left of deque
            dq.appendleft(x)
        else:
            # Current state is normal, so appending to end means appending to right of deque
            dq.append(x)
        
        # Now reverse the order
        is_reversed = not is_reversed
    
    # After the loop, we need to output based on the final state
    if is_reversed:
        # If is_reversed is True, the logical sequence b is the reverse of the deque content
        print(*(reversed(dq)))
    else:
        # If is_reversed is False, the logical sequence b is the deque content as is
        print(*dq)

if __name__ == '__main__':
    solve()