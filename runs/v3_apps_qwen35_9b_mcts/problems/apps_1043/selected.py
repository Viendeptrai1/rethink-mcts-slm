import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = [int(x) for x in data[1:]]
    
    # Find friend's strength
    friend_strength = -1
    for i in range(n):
        if a[i] == -1:
            friend_strength = i + 1
            a[i] = 0  # Mark friend as having 0 cost (already handled logic-wise)
            break
    
    # We need to determine the minimum cost.
    # The tournament is a complete binary tree of height log2(n).
    # At each level, the number of participants halves.
    # To win, the friend must defeat log2(n) opponents.
    # However, the friend doesn't necessarily fight the strongest available opponents directly.
    # We can arrange the bracket such that the friend fights opponents who are "weak enough" to be beaten naturally,
    # OR we bribe opponents who are stronger.
    # But wait, the problem says "you distribute the boxers into pairs as you wish" at each stage.
    # This means we can construct the entire bracket.
    
    # Key Insight:
    # In a standard tournament, to win, you must win log2(n) matches.
    # In each match, if your strength < opponent's strength, you must bribe the opponent.
    # If your strength >= opponent's strength, you win naturally (cost 0).
    # Since we can arrange the bracket, we want to pair the friend against opponents with strength <= friend_strength as much as possible.
    # If there are not enough such opponents to cover all log2(n) rounds, we must bribe the strongest possible opponents that are still "beatable" or just bribe the cheapest ones among those stronger than the friend?
    # Actually, the constraint is simpler:
    # The friend needs to win k = log2(n) matches.
    # In each match, the opponent must be eliminated.
    # If the opponent is stronger than the friend, we MUST bribe them (cost = a[opp]).
    # If the opponent is weaker or equal, we don't need to bribe (cost = 0).
    # BUT, there is a catch: The opponents the friend faces are the winners of previous sub-tournaments.
    # Those winners might be very strong.
    # However, we can arrange the initial bracket such that the friend faces specific opponents in specific rounds.
    # Specifically, in round 1, the friend can face any of the n-1 other boxers.
    # In round 2, the friend can face any boxer who won their first match (excluding the friend).
    # ...
    # In round k, the friend can face any boxer who won their previous k-1 matches.
    
    # To minimize cost, we want the friend to face opponents with strength <= friend_strength whenever possible.
    # If we run out of such opponents, we are forced to face opponents with strength > friend_strength, and we must bribe them.
    # Which ones do we bribe? The ones with the smallest bribe cost among those stronger than the friend?
    # Not exactly. The set of opponents available at round r depends on how we arranged the previous rounds.
    # But notice: The total number of boxers with strength <= friend_strength is fixed. Let this count be C.
    # The friend needs to win k matches.
    # If C >= k, can we always win with 0 cost?
    # Yes. We can arrange the bracket so that in every round, the friend faces a boxer with strength <= friend_strength.
    # Since there are C such boxers, and we need k opponents, if C >= k, we can pick k distinct boxers from this set to be the friend's opponents in the k rounds.
    # How?
    # Round 1: Friend vs (some weak boxer). That weak boxer is eliminated.
    # Round 2: Friend vs (another weak boxer who won their first match).
    # ...
    # We just need to ensure that the "weak" boxers we want to use as opponents actually reach the round where they face the friend.
    # Since we control the bracket, we can put the friend in one half, and distribute the "weak" boxers in the other halves such that they advance to meet the friend.
    # Actually, it's even simpler: We can construct the tree bottom-up.
    # At any point, if we need the friend to face a specific set of opponents, we can ensure they meet.
    # The only limitation is that an opponent must win their own sub-tournament to reach the friend.
    # But if an opponent is weak (strength <= friend), they can win their sub-tournament naturally against even weaker boxers.
    # So, if we have enough boxers with strength <= friend_strength, we can use them as the friend's opponents in all rounds.
    # Cost = 0.
    
    # What if C < k?
    # Then we are forced to face (k - C) opponents who have strength > friend_strength.
    # For these matches, we must bribe.
    # Which ones? We should choose the ones with the minimum bribe cost among all boxers with strength > friend_strength.
    # Wait, is it just the global minimums?
    # Yes, because we can arrange the bracket so that the friend faces the specific k-C strongest (in terms of bribe cost) boxers that are stronger than the friend.
    # The other boxers (stronger than friend but not chosen to fight the friend) can be eliminated by other boxers in the sub-tournaments.
    # Since we can arrange the bracket arbitrarily, we can isolate the "expensive" strong boxers to fight each other or fight weak boxers, ensuring they don't reach the friend unless we want them to.
    # Actually, if a strong boxer (strength > friend) is not scheduled to fight the friend, they must be eliminated by someone else.
    # Can they be eliminated? Yes, if there is someone stronger than them, or if we bribe someone to beat them.
    # But we want to minimize cost.
    # If we don't schedule a strong boxer to fight the friend, we don't pay to bribe them. We just need to ensure they lose to someone else.
    # Since there is a global maximum strength boxer (n), they can eliminate anyone.
    # So, the strategy is:
    # 1. Count how many boxers have strength <= friend_strength. Let this be `count_weak`.
    # 2. The number of matches the friend must win is `k = log2(n)`.
    # 3. If `count_weak >= k`, the answer is 0.
    # 4. If `count_weak < k`, we need to bribe `k - count_weak` opponents.
    #    These opponents must be chosen from the set of boxers with strength > friend_strength.
    #    To minimize cost, we pick the `k - count_weak` boxers with the smallest `a_i` values from that set.
    
    # Let's verify this logic with the examples.
    # Example 1: n=4, a=[3, 9, 1, -1]. Friend is strength 4.
    # Boxers: 1, 2, 3, 4(Friend).
    # Strengths <= 4: 1, 2, 3, 4. Count = 4.
    # k = log2(4) = 2.
    # 4 >= 2 -> Cost 0. Correct.
    
    # Example 2: n=8, a=[11, -1, 13, 19, 24, 7, 17, 5].
    # Indices (1-based): 1:11, 2:-1(Friend), 3:13, 4:19, 5:24, 6:7, 7:17, 8:5.
    # Friend strength = 2.
    # Boxers with strength <= 2: Only boxer 2 (friend). Count = 1.
    # k = log2(8) = 3.
    # We need 3 opponents. We have 1 weak opponent available.
    # We need to bribe 3 - 1 = 2 opponents.
    # Opponents with strength > 2: 1, 3, 4, 5, 6, 7, 8.
    # Their costs: 11, 13, 19, 24, 7, 17, 5.
    # Sorted costs: 5, 7, 11, 13, 17, 19, 24.
    # Pick smallest 2: 5 and 7. Sum = 12.
    # Output 12. Correct.
    
    # Logic seems solid.
    
    import math
    
    k = int(math.log2(n))
    
    # Count boxers with strength <= friend_strength
    # Note: friend_strength is the index (1-based) because strengths are 1..n.
    # The input array `a` is 0-indexed, so a[i] corresponds to strength i+1.
    # We need to count how many i (0 to n-1) have (i+1) <= friend_strength.
    # Since strengths are 1, 2, ..., n, the boxers with strength <= friend_strength are exactly the first `friend_strength` boxers.
    # However, one of them is the friend.
    # The friend is included in the count of "boxers with strength <= friend_strength".
    # But the friend cannot fight themselves.
    # So the number of *other* boxers with strength <= friend_strength is `friend_strength - 1`.
    
    count_weak_others = friend_strength - 1
    
    if count_weak_others >= k:
        print(0)
    else:
        needed = k - count_weak_others
        # Collect costs of boxers with strength > friend_strength
        # These are boxers with indices from friend_strength to n-1 (0-based)
        # i.e., strengths friend_strength+1 to n.
        strong_costs = []
        for i in range(friend_strength, n):
            strong_costs.append(a[i])
        
        strong_costs.sort()
        total_cost = sum(strong_costs[:needed])
        print(total_cost)

if __name__ == '__main__':
    solve()