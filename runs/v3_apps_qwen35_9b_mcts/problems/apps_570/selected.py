import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    a = int(input_data[0])
    b = int(input_data[1])

    # Vladik gives 1, 3, 5, ... (odd numbers) on turns 1, 3, 5, ...
    # Valera gives 2, 4, 6, ... (even numbers) on turns 2, 4, 6, ...
    # Vladik needs sum of first k odd numbers = k^2 <= a
    # Valera needs sum of first k even numbers = k*(k+1) <= b

    # Find max k for Vladik: k^2 <= a => k = floor(sqrt(a))
    k_vladik = int(a ** 0.5)

    # Find max k for Valera: k*(k+1) <= b
    # Solve k^2 + k - b <= 0
    # k = (-1 + sqrt(1 + 4*b)) / 2
    discriminant = 1 + 4 * b
    k_valera = int((-1 + discriminant ** 0.5) / 2)

    # The game ends when someone cannot make their required move.
    # Turn 1: Vladik needs 1 (k=1 for Vladik)
    # Turn 2: Valera needs 2 (k=1 for Valera)
    # Turn 3: Vladik needs 3 (k=2 for Vladik)
    # Turn 4: Valera needs 4 (k=2 for Valera)
    # ...
    # Turn t:
    # If t is odd (Vladik's turn), he needs to give t candies. This is the t-th odd number? No.
    # Let's re-evaluate the sequence of candies given.
    # Turn 1 (Vladik): gives 1. Total given by Vladik so far = 1.
    # Turn 2 (Valera): gives 2. Total given by Valera so far = 2.
    # Turn 3 (Vladik): gives 3. Total given by Vladik so far = 1+3 = 4.
    # Turn 4 (Valera): gives 4. Total given by Valera so far = 2+4 = 6.
    # Turn 5 (Vladik): gives 5. Total given by Vladik so far = 1+3+5 = 9.
    # Turn 6 (Valera): gives 6. Total given by Valera so far = 2+4+6 = 12.
    #
    # Vladik's total given after n turns (where n is odd, say 2m-1) is sum of first m odd numbers = m^2.
    # Valera's total given after n turns (where n is even, say 2m) is sum of first m even numbers = m(m+1).
    #
    # Let m be the number of full rounds completed (each round has Vladik then Valera).
    # After m rounds:
    # Vladik has given m^2 candies. He can complete round m if a >= m^2.
    # Valera has given m(m+1) candies. He can complete round m if b >= m(m+1).
    #
    # We need to find the first person who fails.
    # Check if Vladik can complete round m: if a < m^2, Vladik fails at turn 2m-1.
    # Check if Valera can complete round m: if b < m(m+1), Valera fails at turn 2m.
    #
    # Since we want the first failure, we can iterate m starting from 1.
    # However, a and b are up to 10^9, so O(1) math is better.
    #
    # Max m for Vladik: m_v = floor(sqrt(a))
    # Max m for Valera: m_v_val = floor((-1 + sqrt(1+4b))/2)
    #
    # If m_v < m_v_val, it means Vladik cannot complete round m_v + 1, while Valera can complete round m_v + 1.
    # So Vladik fails first.
    # If m_v >= m_v_val, it means Valera cannot complete round m_v_val + 1, while Vladik can complete round m_v_val + 1.
    # So Valera fails first.
    #
    # Wait, let's trace carefully.
    # Suppose a=1, b=1.
    # m_v = floor(sqrt(1)) = 1. Vladik can complete round 1 (give 1).
    # m_v_val = floor((-1 + sqrt(5))/2) = floor(( -1 + 2.236)/2) = floor(0.618) = 0. Valera cannot complete round 1 (needs 2, has 1).
    # So Valera fails first. Output: Valera. Correct.
    #
    # Suppose a=7, b=6.
    # m_v = floor(sqrt(7)) = 2. Vladik can complete round 1 (1) and round 2 (1+3=4). Total 4 <= 7.
    # m_v_val = floor((-1 + sqrt(25))/2) = floor(4/2) = 2. Valera can complete round 1 (2) and round 2 (2+4=6). Total 6 <= 6.
    # Both can complete round 2.
    # Next round is round 3.
    # Vladik needs 1+3+5 = 9. 9 > 7. Vladik fails.
    # Valera needs 2+4+6+8 = 20. But Vladik already failed.
    # So Vladik fails first. Output: Vladik. Correct.
    #
    # Logic:
    # Calculate max full rounds Vladik can complete: m_v = int(a**0.5)
    # Calculate max full rounds Valera can complete: m_val = int((-1 + (1+4*b)**0.5)/2)
    #
    # If m_v < m_val: Vladik runs out of candies before Valera. Vladik fails.
    # If m_val < m_v: Valera runs out of candies before Vladik. Valera fails.
    # If m_v == m_val: Both can complete m rounds.
    #   Next is round m+1.
    #   Vladik needs (m+1)^2. If a < (m+1)^2, Vladik fails.
    #   But since m_v = m, by definition a < (m+1)^2. So Vladik fails.
    #   Wait, if m_v == m_val, does Vladik always fail first?
    #   Let's check a=4, b=6.
    #   m_v = 2 (1+3=4).
    #   m_val = 2 (2+4=6).
    #   Round 3: Vladik needs 5. 4 < 5. Vladik fails.
    #   So if m_v == m_val, Vladik fails first.
    #
    # Therefore, if m_v <= m_val, Vladik fails first?
    # Let's re-verify a=1, b=1. m_v=1, m_val=0. m_v > m_val. Valera fails. Correct.
    # a=7, b=6. m_v=2, m_val=2. m_v == m_val. Vladik fails. Correct.
    # a=2, b=2.
    # m_v = 1 (1 <= 2, 4 > 2).
    # m_val = 1 (2 <= 2, 6 > 2).
    # m_v == m_val. Vladik fails?
    # Round 1: Vladik gives 1 (rem 1). Valera gives 2 (rem 0).
    # Round 2: Vladik needs 3. Has 1. Fails.
    # Yes, Vladik fails.
    #
    # What if a=10, b=2?
    # m_v = 3 (1+3+5=9 <= 10).
    # m_val = 0 (2 > 2? No, 2<=2. Wait. 2*(0+1)=0 <= 2. 2*(1+1)=4 > 2. So m_val=1? No.)
    # Formula for m_val: k(k+1) <= b.
    # If b=2: k=1 => 1*2=2 <= 2. k=2 => 2*3=6 > 2. So m_val=1.
    # m_v = 3.
    # m_v > m_val. Valera fails first.
    # Trace:
    # R1: V gives 1 (ok), Val gives 2 (ok).
    # R2: V gives 3 (ok, total 4), Val gives 4 (needs 4, has 2). Fails.
    # Correct.
    #
    # So the condition is:
    # if m_v <= m_val: Vladik fails first.
    # else: Valera fails first.
    #
    # Wait, let's re-check the equality case logic.
    # If m_v == m_val, it means both can complete m rounds.
    # The next move is Vladik's (round m+1).
    # Vladik needs (m+1)^2. Since m_v = m, we know (m+1)^2 > a.
    # So Vladik cannot make the move. Vladik fails.
    # So yes, if m_v <= m_val, Vladik fails.
    # If m_v > m_val, then Valera cannot complete round m_val+1, while Vladik can.
    # Valera fails.
    #
    # Final logic:
    # m_v = int(a**0.5)
    # m_val = int((-1 + (1+4*b)**0.5)/2)
    # if m_v <= m_val: print("Vladik")
    # else: print("Valera")

    if k_vladik <= k_valera:
        print("Vladik")
    else:
        print("Valera")

if __name__ == "__main__":
    solve()