import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    idx = 0
    
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    
    cards = []
    for _ in range(n * k):
        cards.append(int(data[idx])); idx += 1
        
    favorites = []
    for _ in range(n):
        favorites.append(int(data[idx])); idx += 1
        
    h = []
    for _ in range(k):
        h.append(int(data[idx])); idx += 1
        
    from collections import Counter
    card_counts = Counter(cards)
    
    # Group players by their favorite number
    players_by_fav = {}
    for f in favorites:
        if f not in players_by_fav:
            players_by_fav[f] = []
        players_by_fav[f].append(f)
        
    # Sort favorite numbers to process groups in a deterministic order
    sorted_favs = sorted(players_by_fav.keys())
    
    # dp[i][j] = max joy using first i groups of players, having used j cards of the current favorite number
    # However, since groups are independent in terms of which specific cards they use (only count matters),
    # we can process each unique favorite number group independently and sum up the results.
    # But wait, the total number of cards of a specific value is limited.
    # So for each unique favorite number X:
    #   Let count_X be the total available cards with value X.
    #   Let num_players_X be the number of players who have X as favorite.
    #   We need to distribute at most count_X cards among these num_players_X players.
    #   Each player j can take t_j cards (0 <= t_j <= k), such that sum(t_j) <= count_X.
    #   The joy for player j taking t_j cards is h[t_j] if t_j > 0 else 0.
    #   We want to maximize sum of joys.
    
    # Since the groups of players with different favorite numbers are completely independent
    # (a card with value A cannot help a player who likes B), we can solve the subproblem
    # for each favorite number and sum the maximum joys.
    
    total_max_joy = 0
    
    for fav in sorted_favs:
        count_X = card_counts[fav]
        num_players = len(players_by_fav[fav])
        
        # dp[t] = max joy achievable with exactly t cards distributed among the players processed so far
        # Initialize dp[0] = 0, others = -infinity (or a very small number)
        # Since we want to maximize, and joy is non-negative, we can use -1 to indicate unreachable states
        # But actually, we can always distribute 0 cards, so dp[0] = 0 is always reachable.
        # Other states might not be reachable if we don't have enough cards or players.
        
        # We iterate through each player in this group
        # dp[t] will store the max joy using t cards distributed among the players considered so far
        
        # Initialize dp array of size (count_X + 1) with -1
        # However, count_X can be up to n*k = 5000. This is fine.
        # But note: we cannot distribute more than k cards to a single player.
        # Also, the total cards distributed cannot exceed count_X.
        
        # Let's redefine: dp[t] = max joy using exactly t cards distributed among the current set of players.
        # Initialize with -1, except dp[0] = 0.
        
        dp = [-1] * (count_X + 1)
        dp[0] = 0
        
        # Process each player who likes 'fav'
        for _ in range(num_players):
            # We create a new_dp array for the next state
            # To optimize, we can iterate backwards or use a temporary array
            new_dp = list(dp)
            
            # For the current player, they can take t cards where 0 <= t <= k
            # But we are limited by the remaining cards? 
            # Actually, the state dp[t] represents the total cards used so far.
            # When we consider the next player, if we give them t cards, the new total cards used is old_t + t.
            # We must ensure old_t + t <= count_X.
            
            # Iterate over all possible previous total card counts
            for used in range(count_X + 1):
                if dp[used] == -1:
                    continue
                
                # Try giving the current player t cards, where 0 <= t <= k
                for t in range(k + 1):
                    new_used = used + t
                    if new_used > count_X:
                        break
                    
                    joy_gain = 0
                    if t > 0:
                        joy_gain = h[t-1] # h is 0-indexed, h_t corresponds to index t-1
                    
                    new_val = dp[used] + joy_gain
                    if new_val > new_dp[new_used]:
                        new_dp[new_used] = new_val
            
            dp = new_dp
        
        # After processing all players for this favorite number, the answer for this group is the max value in dp
        # Note: We can use anywhere from 0 to count_X cards.
        current_group_max = 0
        for val in dp:
            if val > current_group_max:
                current_group_max = val
        total_max_joy += current_group_max
        
    print(total_max_joy)

if __name__ == '__main__':
    solve()