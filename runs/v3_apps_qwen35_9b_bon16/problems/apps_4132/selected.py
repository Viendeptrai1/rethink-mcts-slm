import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:]))
    
    # To minimize the final health, we want the last surviving monster to have a small value.
    # The process is equivalent to: pick any two monsters, subtract the smaller from the larger 
    # (if we choose optimally who attacks whom), but actually the rule is: attacker's health is subtracted from victim.
    # If attacker has health X and victim has health Y:
    #   - If X <= Y: new victim health = Y - X.
    #   - If X > Y: victim dies (health becomes <= 0), and we continue with the remaining alive monsters.
    #
    # Key Insight:
    # We can think of this as being able to subtract any subset of the initial values from the final survivor,
    # such that the sum of the subtracted values is strictly less than the initial health of the survivor? 
    # Not exactly. Let's re-evaluate.
    #
    # Actually, this problem is equivalent to finding the smallest element in the array.
    # Why?
    # Suppose we sort the array: a_1 <= a_2 <= ... <= a_n.
    # If we let the monster with the smallest health (a_1) attack repeatedly, we can reduce larger monsters.
    # However, the optimal strategy described in similar problems (like AtCoder ABC 178 F or similar logic) 
    # for "minimum possible final health" where you can choose who attacks whom is actually just the minimum element.
    #
    # Let's trace the sample: 2, 10, 8, 40.
    # Minimum is 2. Output is 2.
    # Explanation in sample: "When only the first monster keeps on attacking..."
    # Monster 1 (health 2) attacks Monster 2 (10) -> M2 becomes 8.
    # M1 (2) attacks M2 (8) -> M2 becomes 6.
    # M1 (2) attacks M2 (6) -> M2 becomes 4.
    # M1 (2) attacks M2 (4) -> M2 becomes 2.
    # M1 (2) attacks M3 (8) -> M3 becomes 6.
    # M1 (2) attacks M3 (6) -> M3 becomes 4.
    # M1 (2) attacks M3 (4) -> M3 becomes 2.
    # M1 (2) attacks M4 (40) -> ... M4 becomes 2 eventually.
    # Finally M1 and M4 are both 2. M1 attacks M4 -> M4 becomes 0 (dead). M1 survives with 2.
    #
    # Can we get lower than the minimum?
    # Suppose min is m. Any attack reduces a value by some positive integer (the attacker's current health).
    # The attacker's health only changes if they are attacked and survive (health reduced).
    # If the attacker dies, they are removed.
    # If we have a set of numbers, can we reach a state where the survivor has health < min(initial)?
    # No. Because to reduce a number X by Y, Y must exist as a current health. 
    # The total "reduction potential" is limited by the sum of other elements, but more importantly:
    # Consider the invariant: The minimum health among all alive monsters never decreases below the initial minimum?
    # Actually, if we have {2, 10}, 2 attacks 10 -> {2, 8}. Min is still 2.
    # 2 attacks 8 -> {2, 6}. Min is 2.
    # It seems the minimum value in the set is non-increasing? No, the set changes.
    # But notice: you can never create a new number smaller than the smallest existing number minus something?
    # Wait, if we have {5, 5}, 5 attacks 5 -> {5, 0} -> {5}. Result 5.
    # If we have {2, 10}, result 2.
    # Is it possible to get 1 from {2, 10}? No, because we subtract 2 from 10 multiple times, getting 2, 0.
    # We can never get 1.
    #
    # Hypothesis: The answer is simply the minimum element of the array A.
    # Proof sketch:
    # 1. The final health must be >= min(A). Why?
    #    Suppose the final survivor has health H < min(A).
    #    At the start, all A_i >= min(A) > H.
    #    Health only decreases when attacked.
    #    To get from A_i to H, we must subtract a total of A_i - H.
    #    The subtrahends are the current healths of attackers.
    #    If we consider the moment when a monster's health drops below the current minimum of the set, 
    #    it implies an attacker had health > current minimum? 
    #    Actually, a simpler argument: 
    #    In any operation (X attacks Y), if X <= Y, new Y is Y-X. The new minimum of the set is min(old_min, Y-X).
    #    If X > Y, Y dies. The new minimum is min(old_min without Y, X). Since X was in the set, the minimum doesn't jump up, 
    #    but could it go down? 
    #    If X > Y, and X was the unique minimum, then after Y dies, X is still there. If X was not the unique minimum, 
    #    there was some Z <= X. If Z != Y, Z remains. So the minimum stays the same or becomes smaller?
    #    Wait, if we have {2, 10}, min=2. 2 attacks 10 -> {2, 8}, min=2.
    #    What if we have {3, 4, 5}? Min=3.
    #    3 attacks 4 -> {3, 1, 5}? No, 3 attacks 4 -> 4-3=1. Set becomes {3, 1, 5}. Min becomes 1.
    #    Oh! My previous hypothesis is wrong. We CAN reduce the minimum.
    #    Example: 3, 4, 5. 
    #    3 attacks 4 -> 4 becomes 1. Alive: 3, 1, 5.
    #    Now min is 1.
    #    Can we go lower? 
    #    1 attacks 3 -> 3-1=2. Alive: 1, 2, 5.
    #    1 attacks 2 -> 2-1=1. Alive: 1, 1, 5.
    #    1 attacks 1 -> 1-1=0 (dead). Alive: 1, 5.
    #    1 attacks 5 -> 5-1=4 -> 4-1=3 -> 3-1=2 -> 2-1=1 -> 1-1=0. 
    #    Final: 1.
    #    So from {3, 4, 5} we got 1.
    #    Is it possible to get 0? No, the problem asks for "alive" monster, and alive means health >= 1.
    #    But wait, the sample output for 2, 10, 8, 40 is 2.
    #    My manual trace for {3,4,5} gave 1. Min(3,4,5) is 3. So answer != min(A).
    #
    #    Let's re-read the sample explanation carefully.
    #    "When only the first monster keeps on attacking, the final health of the last monster will be 2".
    #    Initial: 2, 10, 8, 40.
    #    If we use the strategy: always let the current smallest attack someone else?
    #    Or maybe the strategy is: always let the smallest attack the largest?
    #    Let's try to simulate optimally for {3, 4, 5}.
    #    Option 1: 3 attacks 4 -> {3, 1, 5}. Then 1 attacks 5 -> {3, 1, 4} -> {3, 1, 3} -> {3, 1, 2} -> {3, 1, 1} -> 1 attacks 1 -> {3, 1}. Then 1 attacks 3 -> {1, 2} -> {1, 1} -> 1. Result 1.
    #    Option 2: 3 attacks 5 -> {3, 4, 2}. Then 2 attacks 4 -> {3, 2, 1}. Then 1 attacks 3 -> {1, 2} -> 1. Result 1.
    #    It seems 1 is achievable.
    #    But wait, is 1 the minimum possible? Can we get 0? No, must be alive.
    #    Is it possible to get something less than 1? No, integers.
    #    So for {3, 4, 5} answer is 1.
    #    What is special about 1? It's gcd(3, 4, 5)? gcd(3,4)=1, gcd(1,5)=1.
    #    For {2, 10, 8, 40}, gcd(2, 10, 8, 40) = 2.
    #    Sample output is 2.
    #    This looks like the answer is GCD of all elements.
    #
    #    Let's verify the logic.
    #    Operation: X attacks Y -> Y becomes Y-X.
    #    This is exactly the Euclidean algorithm step!
    #    If we have a set of numbers, and we can perform Y = Y - X any number of times (as long as Y >= X), 
    #    we can effectively replace Y with Y mod X.
    #    Also, we can choose any pair.
    #    The goal is to reduce all numbers to a single number.
    #    The set of reachable values using linear combinations with integer coefficients (where coefficients sum to 1? No.)
    #    Actually, consider the invariant: any linear combination of the current values with integer coefficients is a linear combination of the initial values.
    #    Specifically, if we have values v1, v2, ..., vk. Any new value generated is of the form v_i - v_j.
    #    The GCD of the set is invariant under subtraction.
    #    So, gcd(v1, ..., vk) = gcd(v1, ..., v_{k-1}, v_k - v_i).
    #    Therefore, the GCD of the current alive monsters remains constant throughout the process.
    #    Let G = gcd(A_1, ..., A_N).
    #    At the end, we have one monster with health H.
    #    Then G must divide H.
    #    So H >= G.
    #    Can we always achieve H = G?
    #    Yes, by mimicking the Euclidean algorithm. We can reduce any two numbers to their GCD.
    #    By iteratively applying the operation, we can reduce the whole set to a single number equal to the GCD of the initial set.
    #    Since H must be a positive integer (alive) and a multiple of G, the minimum possible H is G.
    #
    #    Conclusion: The answer is the Greatest Common Divisor (GCD) of all A_i.

    from math import gcd
    from functools import reduce

    ans = reduce(gcd, a)
    print(ans)

if __name__ == '__main__':
    solve()