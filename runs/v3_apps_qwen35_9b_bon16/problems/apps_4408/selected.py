import sys
from collections import Counter

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    n = int(next(iterator))
    k = int(next(iterator))
    
    total_cards = n * k
    card_counts = Counter()
    for _ in range(total_cards):
        val = int(next(iterator))
        card_counts[val] += 1
        
    favorite_counts = Counter()
    for _ in range(n):
        val = int(next(iterator))
        favorite_counts[val] += 1
        
    h = []
    for _ in range(k):
        h.append(int(next(iterator)))
    
    # If a player gets t cards matching their favorite number, joy is h[t-1] for t>=1, else 0.
    # We need to distribute cards to maximize total joy.
    # Strategy: Group players by their favorite number.
    # For each distinct favorite number X:
    #   Let available_X = number of cards with value X.
    #   Let players_X = number of players who have favorite number X.
    #   We need to decide how many cards of value X each player gets (0 to k).
    #   Constraint: Sum of cards given to these players <= available_X.
    #   Also, sum of cards given to these players <= players_X * k (but this is loose since we can't give more than k).
    #   Actually, the constraint is simply that we cannot give more cards than available.
    #   And each player can receive at most k cards of this value? No, a player can receive at most k cards total, 
    #   but since we are considering only cards of value X, and a player only cares about cards of value X for joy,
    #   we can model this as: for each player, we assign t_i cards of value X (0 <= t_i <= k).
    #   Sum(t_i) <= available_X.
    #   We want to maximize sum(h[t_i - 1] if t_i > 0 else 0).
    #   Since the joy function h is strictly increasing, and we want to maximize sum of joys given a fixed number of cards available_X
    #   and a fixed number of players (players_X), this is a variation of the knapsack problem or can be solved with DP.
    #   
    #   However, note that we have multiple groups (different favorite numbers). The groups are independent because:
    #   Cards of value X can only contribute to players who like X.
    #   Players who like Y cannot get joy from cards of value X.
    #   Therefore, we can solve for each distinct favorite number independently and sum the results.
    #   
    #   For a specific favorite number X:
    #     Let P = players_X (number of players who like X)
    #     Let C = available_X (number of cards with value X)
    #     We need to distribute at most C cards among P players.
    #     Each player j gets t_j cards (0 <= t_j <= k).
    #     Constraint: sum(t_j) <= C.
    #     Objective: maximize sum( joy(t_j) ) where joy(t) = h[t-1] if t>0 else 0.
    #     
    #   This can be solved with DP.
    #   Let dp[i][j] = maximum joy using a subset of first i players with exactly j cards distributed.
    #   i ranges from 0 to P.
    #   j ranges from 0 to C (or min(C, P*k)).
    #   Transition: For player i, try assigning t cards (0 <= t <= k).
    #     dp[i][j] = max(dp[i-1][j-t] + joy(t)) for all valid t.
    #   
    #   Optimization: Since P can be up to 500 and k up to 10, and C can be up to 5000.
    #   However, note that C is bounded by total cards, but for a specific number, C <= total cards.
    #   But wait, the total number of cards is n*k. So C <= n*k = 5000.
    #   P <= n = 500.
    #   State space: 500 * 5000 = 2.5e6, which is acceptable.
    #   Transition takes O(k). Total complexity per group: O(P * C * k).
    #   Sum of P over all groups is n. Sum of C over all groups is total cards = n*k.
    #   However, the worst case is one group with P=n and C=n*k. Then complexity is O(n * (n*k) * k) = O(n^2 * k^2).
    #   With n=500, k=10: 500^2 * 100 = 250000 * 100 = 25,000,000. This might be slightly tight for Python in 1-2 seconds, but let's check constraints.
    #   Actually, C is the count of a specific number. In the worst case, all cards are the same number, so C = n*k.
    #   Is there a better way?
    #   
    #   Alternative approach for a group:
    #   We have P players and C cards. We want to choose non-negative integers t_1, ..., t_P such that sum(t_i) <= C and 0 <= t_i <= k.
    #   Maximize sum of joys.
    #   Since the joy function is concave? Not necessarily. h_t is strictly increasing but not necessarily concave.
    #   Example: h = [0, 10, 100]. Jump from 1 to 2 is 90.
    #   If it's not concave, we might prefer giving 2 cards to one player over 1 to two players even if 2 cards = 1+1.
    #   So DP is the safe way.
    #   
    #   Let's optimize the DP state.
    #   We only need the previous row. So space O(C).
    #   Also, we can limit j to min(C, P*k).
    #   
    #   Let's implement the DP carefully.
    
    total_joy = 0
    
    # Precompute joy values for t in 0..k
    # joy[t] = h[t-1] for t>=1, 0 for t=0
    joy_vals = [0] * (k + 1)
    for t in range(1, k+1):
        joy_vals[t] = h[t-1]
        
    distinct_favorites = favorite_counts.keys()
    
    for fav_num in distinct_favorites:
        p_count = favorite_counts[fav_num]
        c_count = card_counts[fav_num]
        
        if c_count == 0:
            continue
            
        # Limit the max cards we can distribute to p_count * k (though c_count might be less)
        # Actually, we can distribute at most c_count cards.
        # Also, we cannot give more than k cards to any player.
        # So max cards distributed is min(c_count, p_count * k). But since c_count could be large, 
        # we are limited by c_count.
        # However, we don't need to consider j > c_count.
        # Also, we don't need to consider j > p_count * k (obviously).
        limit = min(c_count, p_count * k)
        
        # dp[j] = max joy with exactly j cards distributed among current subset of players
        # Initialize with -infinity, but base case dp[0] = 0
        dp = [-float('inf')] * (limit + 1)
        dp[0] = 0
        
        # Process each player in this group
        for _ in range(p_count):
            new_dp = [-float('inf')] * (limit + 1)
            # We can iterate j from 0 to limit
            # But to save time, we can track the current max reachable j
            # Initially max_j is 0. After each player, max_j increases by at most k.
            current_max_j = 0
            
            for j in range(limit + 1):
                if dp[j] == -float('inf'):
                    continue
                
                # Try giving t cards to the new player
                # t can be from 0 to k
                # New total cards = j + t
                # Check if j+t <= limit
                for t in range(k + 1):
                    if j + t <= limit:
                        val = dp[j] + joy_vals[t]
                        if val > new_dp[j + t]:
                            new_dp[j + t] = val
                # Optimization: update current_max_j
                if j + k > current_max_j:
                    current_max_j = j + k
            
            dp = new_dp
            
        # The answer for this group is the maximum value in dp array
        # Because we can distribute *at most* c_count cards, so any dp[j] for j <= c_count is valid.
        # We take the max over all valid j (which is up to limit).
        group_max = 0
        for j in range(limit + 1):
            if dp[j] > group_max:
                group_max = dp[j]
        total_joy += group_max
        
    print(total_joy)

if __name__ == '__main__':
    solve()