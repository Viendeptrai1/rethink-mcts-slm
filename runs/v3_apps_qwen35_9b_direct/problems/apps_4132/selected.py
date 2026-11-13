import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        a = []
        for _ in range(n):
            a.append(int(next(iterator)))
    except StopIteration:
        return

    # We want to minimize the final health.
    # Strategy: Always have the monster with the smallest current health attack the monster with the largest current health.
    # This is equivalent to simulating the process where we repeatedly:
    # 1. Pick the smallest element (attacker).
    # 2. Pick the largest element (victim).
    # 3. Subtract attacker from victim.
    # 4. If victim becomes <= 0, it dies (remove from consideration).
    # 5. Repeat until 1 monster remains.
    #
    # However, simulating step-by-step with a max-heap and min-heap might be too slow if many monsters die one by one.
    # But note: In each step, one monster dies. We start with N monsters and end with 1, so exactly N-1 deaths occur.
    # Each death requires one operation. Total operations = N-1.
    # With N up to 10^5, O(N log N) is acceptable.
    #
    # Algorithm:
    # Use a min-heap for available monsters (to get the smallest attacker quickly).
    # Use a max-heap for available monsters (to get the largest victim quickly).
    # But we need to maintain consistency. Since a monster can be both the smallest and largest (if only one left), 
    # we can just use one heap? 
    # Actually, we need to efficiently pick min and max. Two heaps are good.
    # However, when a monster dies, we remove it from both heaps. Lazy deletion is easier.
    #
    # Steps:
    # 1. Create a min-heap `min_h` with all A_i.
    # 2. Create a max-heap `max_h` with all A_i (store negative values for max-heap behavior).
    # 3. While len(alive) > 1:
    #    a. Get smallest attacker from min_h. Skip dead ones.
    #    b. Get largest victim from max_h. Skip dead ones.
    #    c. Update victim health: victim = victim - attacker.
    #    d. If victim <= 0, mark as dead.
    #    e. Push updated victim back to both heaps if still alive.
    #    f. Decrement alive count.
    #
    # But wait: The problem says "A random alive monster attacks another random alive monster". We are to find the MINIMUM possible final health.
    # This implies we can choose the sequence of attacks optimally.
    # Optimal strategy: Always let the smallest current health attack the largest current health.
    # Why? Because we want to reduce the large numbers as much as possible using small numbers, and preserve the small numbers to continue attacking.
    # Actually, once a monster attacks, its health doesn't change. Only the victim's health changes.
    # So the set of "attackers" remains constant in value until they die.
    # To minimize the final result, we should use the smallest available health to chip away at the largest available health repeatedly until the largest dies, then move to the next largest, etc.
    #
    # Revised Strategy:
    # Sort the initial healths: A[0] <= A[1] <= ... <= A[N-1].
    # The smallest monster (A[0]) will attack the largest (A[N-1]), then the new largest, etc., until the largest dies.
    # Then the next smallest (A[1]) will attack the new largest, and so on.
    #
    # However, note: After A[0] attacks A[N-1] multiple times, A[0] remains A[0]. The victim decreases.
    # When the victim dies, we remove it. Then we take the next largest and attack it with A[0] until it dies?
    # But what if A[0] is not enough to kill the next largest even once? Then we might need to use A[1] as well?
    # Actually, the optimal strategy is:
    # Use the smallest monster to attack the largest monster until the largest monster dies.
    # Then use the smallest monster (which is still alive) to attack the next largest, and so on.
    # BUT: What if the smallest monster dies? It can't die because it only attacks and never takes damage.
    # Wait: The problem says "the health of the monster attacked is reduced by the amount equal to the current health of the monster attacking".
    # The attacker does NOT lose health. Only the victim loses health.
    # Therefore, the smallest monster will NEVER die as long as there is at least one other monster to attack.
    # So the smallest monster (initially min(A)) will survive until the very end?
    # Not necessarily: The smallest monster might be attacked by someone else? 
    # No, we are choosing the sequence to MINIMIZE the final health. We can choose who attacks whom.
    # To minimize the final health, we should avoid having the smallest monster attacked.
    # Instead, we should use the smallest monster to attack everyone else until they die.
    # Since the smallest monster never loses health, it will remain the smallest throughout.
    # And since it never dies, it will be the last one alive?
    # Let's verify: 
    # Suppose we have [2, 10, 8, 40]. 
    # Smallest is 2. 
    # 2 attacks 40 -> 40 becomes 38.
    # 2 attacks 38 -> 36.
    # ... until 40 dies? 
    # 40 / 2 = 20 times. After 20 attacks, 40 becomes 0 and dies.
    # Now we have [2, 10, 8]. 
    # 2 attacks 10 -> 8.
    # 2 attacks 8 -> 6.
    # 2 attacks 6 -> 4.
    # 2 attacks 4 -> 2.
    # 2 attacks 2 -> 0. Dies.
    # Now we have [2, 8]. 
    # 2 attacks 8 -> 6.
    # 2 attacks 6 -> 4.
    # 2 attacks 4 -> 2.
    # 2 attacks 2 -> 0. Dies.
    # Now we have [2, 4]? Wait, let's re-simulate carefully.
    # Initial: [2, 10, 8, 40]
    # Use 2 to kill 40: 40 - 2*20 = 0 -> dies. Remaining: [2, 10, 8]
    # Use 2 to kill 10: 10 - 2*5 = 0 -> dies. Remaining: [2, 8]
    # Use 2 to kill 8: 8 - 2*4 = 0 -> dies. Remaining: [2]
    # Final health: 2.
    # This matches the sample output.
    #
    # But what if the smallest doesn't divide evenly?
    # Example: [3, 10]
    # 3 attacks 10: 10-3=7, 7-3=4, 4-3=1. 10 becomes 1.
    # Now [3, 1]. 
    # 3 attacks 1: 1-3 = -2 -> dies.
    # Final: 3.
    # Is there a better way? 
    # If 1 attacks 3: 3-1=2, 2-1=1. Then [1, 1]. 
    # Then 1 attacks 1: 1-1=0 -> dies. Final: 1.
    # Oh! So the strategy of always using the smallest to attack the largest is NOT optimal in this case.
    # In the example [3, 10], if we let 10 attack 3, we get 3->2->1, then 1 attacks 3->2->1, then 1 attacks 1->0. Final 1.
    # But if we let 3 attack 10 repeatedly, we get 10->1, then 3 attacks 1-> -2, final 3.
    # So the optimal strategy is NOT simply "smallest attacks largest".
    #
    # Re-evaluating:
    # We want to minimize the final health. The final health is the health of the last survivor.
    # Notice that the operation is: victim = victim - attacker.
    # This is similar to the Euclidean algorithm for GCD, but we can choose the order.
    # Actually, the final health will be the GCD of all initial healths? 
    # Let's check: 
    # [3, 10]: GCD(3,10)=1. Final min=1. Matches.
    # [2, 10, 8, 40]: GCD(2,10,8,40)=2. Final min=2. Matches.
    # Another example: [4, 6]. GCD=2.
    # Option 1: 4 attacks 6 -> 2. Then 4 attacks 2 -> 2. Then 2 attacks 4? No, 4 is still 4. 
    # Wait, if 4 attacks 6: 6-4=2. Now [4,2]. 
    # Then 4 attacks 2: 2-4=-2 -> dies. Final 4.
    # Option 2: 2 attacks 4: 4-2=2. Now [4,2] (same state). 
    # Then 2 attacks 4: 4-2=2. Now [2,2]. 
    # Then 2 attacks 2: 2-2=0 -> dies. Final 2.
    # So min final is 2, which is GCD(4,6).
    #
    # Hypothesis: The minimum possible final health is the GCD of all A_i.
    # Why? 
    # Because any operation (v = v - a) preserves the GCD of the set of numbers.
    # Proof: Let g = gcd(S). Then every element in S is a multiple of g. 
    # When we do v = v - a, the new set S' has v' = v - a, which is also a multiple of g. 
    # So the GCD of the set remains a divisor of the original GCD. 
    # Actually, the GCD of the set might increase? No, because we are only subtracting, the common divisors can only stay the same or the set of common divisors can shrink? 
    # Wait: gcd(a, b) = gcd(a, b-a). So the GCD of the entire set is invariant under the operation.
    # Therefore, the GCD of the final single number must be equal to the GCD of the initial set.
    # And since the final number is a multiple of the GCD, the minimum possible value is exactly the GCD.
    # Can we always achieve the GCD?
    # Yes, by simulating the Euclidean algorithm: repeatedly subtract the smaller from the larger until one becomes 0, then take the non-zero one, and continue with the rest.
    # Essentially, we can reduce the set to the GCD.
    #
    # Therefore, the answer is simply gcd(A_1, A_2, ..., A_N).
    #
    # Constraints: N up to 10^5, A_i up to 10^9.
    # We can compute the GCD of all numbers in O(N log(min(A))).
    # This is efficient enough.

    import math
    from functools import reduce

    def gcd_list(numbers):
        return reduce(math.gcd, numbers)

    result = gcd_list(a)
    print(result)

if __name__ == '__main__':
    solve()