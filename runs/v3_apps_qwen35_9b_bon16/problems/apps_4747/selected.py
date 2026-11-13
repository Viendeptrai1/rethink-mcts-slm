import sys
import math

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    
    # We use dynamic programming (memoization) to solve the problem.
    # Let dp[i] be the maximum expected score achievable with i rolls remaining.
    # Base case: With 0 rolls remaining, the expected score is 0 (though in our recursion logic,
    # we will handle the "stop" option differently).
    # Actually, let's define dp[i] as the max expected score given that we have i rolls left to use.
    # If we choose to stop now, we get the current roll value.
    # If we choose to reroll, we use 1 roll and are left with i-1 rolls, getting dp[i-1].
    # The optimal strategy for the current roll (value v) with i rolls remaining is:
    #   If v >= dp[i-1], we stop and take v.
    #   If v < dp[i-1], we reroll and get the expected value dp[i-1].
    # Therefore, the expected value dp[i] is:
    #   Sum over all possible rolls v (from 1 to n):
    #     if v >= dp[i-1]: v
    #     else: dp[i-1]
    # Then divide by n.
    
    # dp[0] represents having 0 rolls left. If we are forced to stop with 0 rolls left, 
    # technically we have no outcome, but in the recursive step, if we have 1 roll left,
    # the "reroll" option leads to 0 rolls left. However, the problem says we can roll k times.
    # Let's reframe:
    # Let E[r] be the max expected score with r rolls remaining.
    # For r = 0: We cannot roll anymore. But the game implies we must stop before rolling runs out?
    # No, "the die can only be rolled k times in total". We roll once, then choose stop or reroll.
    # So if we have made k rolls, we must stop.
    # Let's define dp[i] as the max expected score with i rolls *remaining* to be used for future decisions.
    # If i = 0, we have no more rolls, so we must accept the current roll? 
    # Actually, the decision is made AFTER a roll. 
    # Let's define dp[i] as the max expected score we can get starting a new round with i rolls allowed.
    # But the state is: we just rolled, and we have i rolls left to use for *future* rolls (including this current one? No).
    # Let's simplify.
    # Let f(r) be the max expected score when we have r rolls remaining to make decisions.
    # When we are in a state with r rolls remaining:
    #   We roll the die. We see value v.
    #   We can STOP and take v.
    #   Or we can REROLL if r > 0. If we reroll, we consume 1 roll, and then we are in state r-1.
    #   The expected value of state r-1 is f(r-1).
    #   So if v >= f(r-1), we stop. If v < f(r-1), we reroll (assuming r > 0).
    #   If r == 0, we have no choice but to stop (but this state shouldn't be reached as a "start of decision" unless k=0 which is not allowed).
    #   Wait, the definition of "r rolls remaining" needs to be precise.
    #   Start of game: k rolls available.
    #   Action: Roll.
    #   Decision: Stop or Reroll (if rolls > 0).
    #   If we reroll, we have k-1 rolls left for the next decision.
    #   So, let dp[i] be the max expected score with i rolls remaining to be used in future.
    #   Base case: dp[0] = 0? No, if we have 0 rolls left, we cannot reroll. But the decision happens after a roll.
    #   Let's define dp[i] as the optimal expected score given that we have just rolled and have i rolls *left* to potentially reroll.
    #   If i = 0, we must stop. So the value is the current roll. But the DP state is independent of the current roll.
    #   The DP state represents the expected value of the "next best outcome" we can achieve if we choose to reroll.
    #   Let E[i] = max expected score with i rolls remaining to use for *future* rolls (i.e., we have already rolled and are deciding).
    #   If we choose to reroll, we get E[i-1].
    #   If we stop, we get current roll.
    #   So, E[i] = (1/n) * sum( max(v, E[i-1]) for v in 1..n )
    #   Base case: E[0]. If we have 0 rolls left to use for future, it means we have already used all k rolls?
    #   Let's trace carefully.
    #   Total rolls allowed: k.
    #   Roll 1 happens. Now we have k-1 rolls left to use for rerolls.
    #   If we reroll, we go to state "k-1 rolls left".
    #   If we reroll again, "k-2".
    #   If we have 0 rolls left, we MUST stop.
    #   So, let dp[i] be the max expected score when we have i rolls remaining *available for rerolls*.
    #   If i = 0, we cannot reroll. We must stop. But what is the value? 
    #   The value dp[i] should represent the expected score of the optimal strategy starting from the moment we have just rolled and have i rerolls left.
    #   If i = 0, we stop. The expected value is the average of the current roll? 
    #   No, the current roll is random. The value dp[i] is a constant (the threshold expectation).
    #   Actually, the recurrence is:
    #   dp[i] = average of max(v, dp[i-1]) for v in 1..n.
    #   What is dp[0]? 
    #   If we have 0 rerolls left, we must stop. The value we get is the current roll v.
    #   But the decision is: take v or take dp[-1]?
    #   Let's redefine:
    #   Let dp[i] be the max expected score with i rolls *remaining* in the entire game (including the current one we are about to roll? No).
    #   Let's stick to the standard solution for this problem (often called "Dice Game" or "Optimal Stopping with Dice").
    #   Let dp[i] = max expected score with i rolls remaining.
    #   When we have i rolls remaining, we roll.
    #   We get v.
    #   We can stop -> get v.
    #   We can reroll -> we have i-1 rolls remaining. The expected value of that future path is dp[i-1].
    #   So we take max(v, dp[i-1]).
    #   Then dp[i] = (1/n) * sum(max(v, dp[i-1]) for v in 1..n).
    #   Base case: dp[0]. If we have 0 rolls remaining, we cannot roll. This state is unreachable as a starting point for a decision "after a roll" unless k=0.
    #   However, if we have 1 roll remaining:
    #     We roll. We get v.
    #     We can stop (get v) or reroll (get dp[0]).
    #     But if we reroll, we have 0 rolls left. So we can't roll again. We must have stopped?
    #     No, the problem says "die can only be rolled k times in total".
    #     If we have 1 roll left, we roll (1st time). Then we decide.
    #     If we decide to reroll, we use the 2nd roll (if k>=2).
    #     If k=1, we roll once. We decide stop or reroll. If we reroll, we need a 2nd roll. But we only have 1 total allowed.
    #     So if k=1, we MUST stop after the first roll.
    #     So if we are in the state "0 rolls remaining" (meaning we cannot reroll), the value is effectively 0? No.
    #     Let's re-evaluate the base case.
    #     dp[i] = expected score with i rolls allowed in the game.
    #     If i=1: We roll. Value v. We can stop (v) or reroll? No, reroll requires 2 rolls total. So we must stop.
    #     So dp[1] = average of v for v in 1..n = (n+1)/2.
    #     If i=2: We roll. Value v.
    #       Option Stop: v.
    #       Option Reroll: We use 1 roll. Remaining rolls = 1. Expected value = dp[1].
    #       So we take max(v, dp[1]).
    #       dp[2] = average(max(v, dp[1])).
    #     General: dp[i] = average(max(v, dp[i-1])).
    #     Base case: dp[1] = (n+1)/2.
    #     Wait, is dp[1] correct?
    #     If I have 1 roll allowed. I roll. I see v. Can I reroll? No, because that would be the 2nd roll.
    #     So I must stop. Expected score = (1+2+...+n)/n = (n+1)/2. Correct.
    #     
    #     So the algorithm:
    #     dp = [0.0] * (k + 1)
    #     dp[1] = (n + 1) / 2.0
    #     for i from 2 to k:
    #         threshold = dp[i-1]
    #         sum_val = 0.0
    #         for v from 1 to n:
    #             if v >= threshold:
    #                 sum_val += v
    #             else:
    #                 sum_val += threshold
    #         dp[i] = sum_val / n
    #     
    #     But wait, what if k=1? The loop range(2, 2) is empty. We just return dp[1]. Correct.
    #     What if k > n? It still works.
    #     
    #     Let's check sample 2: n=2, k=3.
    #     dp[1] = (2+1)/2 = 1.5.
    #     i=2: threshold = 1.5.
    #       v=1: 1 < 1.5 -> add 1.5
    #       v=2: 2 >= 1.5 -> add 2
    #       sum = 3.5. dp[2] = 3.5/2 = 1.75.
    #     i=3: threshold = 1.75.
    #       v=1: 1 < 1.75 -> add 1.75
    #       v=2: 2 >= 1.75 -> add 2
    #       sum = 3.75. dp[3] = 3.75/2 = 1.875.
    #     Matches sample output 1.875.
    #     
    #     Sample 3: n=6, k=2.
    #     dp[1] = 3.5.
    #     i=2: threshold = 3.5.
    #       v=1,2,3: < 3.5 -> add 3.5 each (3 * 3.5 = 10.5)
    #       v=4,5,6: >= 3.5 -> add 4,5,6 (sum = 15)
    #       total = 25.5. dp[2] = 25.5 / 6 = 4.25.
    #     Matches sample output 4.25.
    #     
    #     Sample 1: n=1, k=1.
    #     dp[1] = (1+1)/2 = 1.0. Correct.
    
    # Edge case: k=1.
    # If k=1, we just output (n+1)/2.
    
    # Implementation details:
    # Use a list or just variables. Since k <= 100, O(k*n) is 10000 operations, trivial.
    
    if k == 0:
        # Problem says k >= 1, but just in case.
        print(0.0)
        return

    # dp[i] stores the expected score with i rolls allowed
    dp = [0.0] * (k + 1)
    
    # Base case for 1 roll
    dp[1] = (n + 1) / 2.0
    
    # Iterate for 2 to k
    for i in range(2, k + 1):
        threshold = dp[i-1]
        total = 0.0
        # Sum max(v, threshold) for v in 1..n
        # Optimization: find the split point where v >= threshold
        # Since n is small (100), linear scan is fine.
        for v in range(1, n + 1):
            if v >= threshold:
                total += v
            else:
                total += threshold
        dp[i] = total / n
        
    print(dp[k])

if __name__ == '__main__':
    solve()