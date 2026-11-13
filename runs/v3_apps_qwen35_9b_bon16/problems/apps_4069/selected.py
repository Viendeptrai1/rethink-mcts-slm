import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    X = int(input_data[0])
    K = int(input_data[1])
    D = int(input_data[2])

    # Move towards zero as much as possible
    # Number of steps to reach the same side as zero or cross it
    steps_to_zero = abs(X) // D
    remainder = abs(X) % D

    if steps_to_zero >= K:
        # We cannot even reach zero or cross it within K moves
        # We just move K steps towards zero
        new_X = abs(X) - K * D
        print(new_X)
    else:
        # We can reach the point closest to zero on the same side
        # Then we have remaining moves to oscillate
        K -= steps_to_zero
        current_pos = remainder  # This is non-negative
        # Now we are at 'current_pos' and we have K moves left
        # If K is even, we can just go back and forth and end at current_pos
        # If K is odd, we must move one step to (current_pos - D) or (current_pos + D)
        # Since we want minimum absolute value, and current_pos < D (by definition of remainder),
        # the best we can do on an odd number of moves is to go to (current_pos - D)
        # whose absolute value is (D - current_pos)
        if K % 2 == 0:
            print(current_pos)
        else:
            print(D - current_pos)

if __name__ == '__main__':
    solve()