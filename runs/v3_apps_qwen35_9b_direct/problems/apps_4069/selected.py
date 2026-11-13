import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    X = int(input_data[0])
    K = int(input_data[1])
    D = int(input_data[2])

    # Work with absolute value since the problem is symmetric
    x = abs(X)

    # Move towards 0 as much as possible
    steps_to_zero = x // D
    if steps_to_zero > K:
        # Cannot reach 0 or cross it; just move K steps towards 0
        ans = x - K * D
    else:
        # We can reach 0 or cross it
        remaining_steps = K - steps_to_zero
        pos_after_zero = x - steps_to_zero * D  # This is x % D
        # Now we are at pos_after_zero and have remaining_steps moves
        # Each move changes coordinate by +/- D
        # We want to minimize absolute value
        # After reaching pos_after_zero, we can go back and forth
        # The best we can do is to move towards 0 if possible, but we are already at the closest point to 0 on the line with step D
        # Actually, once we are at pos_after_zero (which is < D), any further move will take us to pos_after_zero - D or pos_after_zero + D
        # Since pos_after_zero < D, pos_after_zero - D is negative, and its absolute value is D - pos_after_zero
        # pos_after_zero + D is positive, absolute value is pos_after_zero + D
        # Clearly D - pos_after_zero < pos_after_zero + D because pos_after_zero < D
        # So if we have at least 1 move left, we should move to pos_after_zero - D
        # Then if we have more moves, we oscillate between pos_after_zero - D and pos_after_zero + D? 
        # Actually, let's re-evaluate:
        # Current position: p = x % D
        # Moves left: rem = K - (x // D)
        # Option 1: Move to p - D (value: p - D, abs: D - p)
        # Option 2: Move to p + D (value: p + D, abs: p + D) -> worse than D-p since p < D
        # So first move from p goes to p - D.
        # Now we are at p - D. Next move can go to (p - D) + D = p or (p - D) - D = p - 2D.
        # We want to minimize absolute value.
        # The two closest points to 0 reachable from p with step D are p and p - D.
        # Their absolute values are p and D - p.
        # If rem is even, we can end at p (by going back and forth: p -> p-D -> p -> p-D ... wait, no)
        # Let's trace:
        # Start at p.
        # 1 move: p - D (abs: D-p)
        # 2 moves: (p-D)+D = p (abs: p)
        # 3 moves: (p-D)-D = p-2D (abs: 2D-p) -> worse than D-p? Not necessarily, but p-2D is further from 0 than p-D if p < D.
        # Actually, the sequence of positions reachable from p with k moves is: p + m*D where m is integer and |m| <= k and m has same parity as k.
        # We want to minimize |p + m*D|.
        # Since p is in [0, D-1], the candidates for minimum absolute value are:
        # m = 0 -> p
        # m = -1 -> p - D (abs: D-p)
        # m = 1 -> p + D (abs: p+D) -> larger than p
        # m = -2 -> p - 2D (abs: 2D-p) -> larger than D-p
        # So the minimum is min(p, D-p).
        # We can reach m=0 if k is even (since we start at p, 0 moves -> p, 2 moves -> p, etc.)
        # We can reach m=-1 if k is odd (1 move -> p-D, 3 moves -> p-2D? No.)
        # Let's re-index.
        # We are at p. We have rem moves.
        # Position after rem moves: p + t*D, where t is an integer such that |t| <= rem and t ≡ rem (mod 2).
        # We want to minimize |p + t*D|.
        # Candidates for t:
        # If rem is even: t can be 0, -2, 2, ...
        #   t=0 -> p
        #   t=-2 -> p-2D (abs: 2D-p) which is > D-p > p (since p < D)
        #   So best is p.
        # If rem is odd: t can be -1, 1, -3, ...
        #   t=-1 -> p-D (abs: D-p)
        #   t=1 -> p+D (abs: p+D) -> worse
        #   t=-3 -> p-3D (abs: 3D-p) -> worse
        #   So best is D-p.
        # Therefore:
        # if rem % 2 == 0: ans = p
        # else: ans = D - p

        p = x % D
        if remaining_steps % 2 == 0:
            ans = p
        else:
            ans = D - p

    print(ans)

if __name__ == '__main__':
    solve()