import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    X = int(input_data[0])
    K = int(input_data[1])
    D = int(input_data[2])

    # Work with absolute value since the problem is symmetric
    X = abs(X)

    # Calculate how many steps of size D are needed to reach the nearest point <= 0
    # We want to find the largest multiple of D that is <= X
    steps_to_zero = X // D
    remainder = X % D

    if steps_to_zero <= K:
        # We can reach the point 'remainder' (which is between 0 and D)
        # We have (K - steps_to_zero) moves left.
        # Since we are at 'remainder', any further move will take us to 'remainder + D' or 'remainder - D'.
        # 'remainder - D' would be negative, so its absolute value is D - remainder.
        # 'remainder + D' would be larger than 'remainder'.
        # So the best we can do is oscillate between 'remainder' and 'D - remainder'.
        # The number of remaining moves is (K - steps_to_zero).
        # If the remaining moves is even, we can stay at 'remainder'.
        # If it is odd, we must move to 'D - remainder'.
        remaining_moves = K - steps_to_zero
        if remaining_moves % 2 == 0:
            print(remainder)
        else:
            print(D - remainder)
    else:
        # We cannot reach the point 'remainder' because we don't have enough moves.
        # We will overshoot zero. The closest we can get is by moving 'steps_to_zero' times towards zero.
        # The position will be X - steps_to_zero * D = remainder.
        # But wait, if steps_to_zero > K, we can only make K moves towards zero.
        # The position will be X - K * D.
        # Since X < K * D (because steps_to_zero = floor(X/D) > K implies X >= (K+1)*D),
        # the result X - K*D will be positive but less than D.
        # Actually, let's re-evaluate:
        # If steps_to_zero > K, it means X // D > K, so X > K * D.
        # We move K steps towards zero: new position = X - K * D.
        # This is the closest we can get because we can't cross zero.
        print(X - K * D)

if __name__ == '__main__':
    solve()