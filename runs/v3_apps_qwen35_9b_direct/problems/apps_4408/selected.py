import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        n = int(next(iterator))
        k = int(next(iterator))
        
        cards = []
        for _ in range(n * k):
            cards.append(int(next(iterator)))
            
        favorites = []
        for _ in range(n):
            favorites.append(int(next(iterator)))
            
        h = []
        for _ in range(k):
            h.append(int(next(iterator)))
    except StopIteration:
        return

    from collections import Counter
    
    card_counts = Counter(cards)
    fav_counts = Counter(favorites)
    
    # Identify unique numbers that appear in both cards and favorites
    relevant_numbers = set(card_counts.keys()) & set(fav_counts.keys())
    
    # For each relevant number, we have:
    # - total available cards: card_counts[num]
    # - total players who like this number: fav_counts[num]
    # We need to distribute these cards among the players who like this number
    # to maximize joy. Players who don't like a number get 0 joy from it.
    
    # Since the joy function h is the same for all players and depends only on the count of matching cards,
    # and the distribution of cards for different numbers is independent (a card with value X only helps players who like X),
    # we can solve the problem for each number independently and sum the results.
    
    total_joy = 0
    
    for num in relevant_numbers:
        available_cards = card_counts[num]
        interested_players = fav_counts[num]
        
        # We need to distribute 'available_cards' to 'interested_players' players.
        # Each player can receive at most k cards of this type (since they only get k cards total, 
        # but actually the constraint is global: each player gets exactly k cards total. 
        # However, since we are solving per number, the constraint is that a player cannot receive more than k cards of THIS number.
        # But wait, the problem says each player gets exactly k cards TOTAL. 
        # Does a player get cards of different types? Yes.
        # Can a player get more than k cards of a specific favorite number? No, because they only hold k cards total.
        # So for a specific number, a player can receive at most min(k, available_cards) cards? 
        # Actually, the constraint is simply: a player can receive at most k cards of this specific number.
        # But since we are optimizing per number, and the total cards a player holds is k, 
        # the maximum any player can get for a specific number is k.
        
        # However, there is a subtle constraint: The sum of cards a player gets across ALL numbers is k.
        # But since we are distributing cards of value X only to players who like X, 
        # and cards of value Y only to players who like Y, etc., 
        # the "total k cards per player" constraint is automatically satisfied if we ensure that 
        # for each player, the sum of cards they receive from all numbers they like is <= k?
        # NO. The problem says "each of them will hold exactly k cards".
        # This means we must distribute ALL cards.
        # The cards that are NOT favorite for a player are just "filler".
        # Since we have exactly n*k cards and n players each getting k cards, 
        # the distribution is always possible as long as we assign the favorite cards optimally 
        # and fill the rest with non-favorite cards.
        # The only constraint linking different numbers is the total capacity of k per player.
        # But since we are only counting joy from favorite matches, and non-favorite cards give 0 joy,
        # we want to maximize the joy from favorite matches.
        # Is it possible that assigning too many favorite cards to one player prevents us from assigning other favorite cards?
        # Yes, if a player likes multiple numbers, they can only take k cards total.
        # Example: Player likes A and B. There are cards for A and B.
        # If we give the player k cards of A, they get 0 cards of B.
        # So we cannot solve numbers independently if a player likes multiple numbers!
        
        # Let's re-read carefully.
        # "The players have to distribute all the cards... each of them will hold exactly k cards."
        # "Joy level... if the player holds t cards containing his favorite number."
        # Note: "his favorite number" (singular).
        # "The favorite number of the j-th player is f_j."
        # This implies each player has exactly ONE favorite number.
        # "Each player counts the number of cards he has that contains his favorite number."
        # So a player only cares about cards with value f_j.
        # Cards with other values are irrelevant for their joy.
        # Therefore, the sets of players interested in different numbers are disjoint.
        # Player j only likes f_j. They do not care about other numbers.
        # So the problem CAN be solved independently for each unique favorite number.
        # The constraint "each player gets k cards" is satisfied by filling the remaining slots with non-favorite cards.
        # Since we have n*k cards total, and we are distributing all of them, 
        # and the "filler" cards can go anywhere, there is no conflict.
        # The only limit for a player regarding a specific number X is that they can receive at most k cards of X.
        
        # So for a specific number 'num':
        # We have 'interested_players' players who like 'num'.
        # We have 'available_cards' cards of value 'num'.
        # We need to distribute 'available_cards' into 'interested_players' buckets.
        # Each bucket can hold at most k cards.
        # We want to maximize sum(h[count]) for the counts in the buckets.
        # Note: h[0] = 0.
        
        # Strategy:
        # We have a limited resource (cards) and a set of bins (players).
        # We want to fill bins to maximize joy.
        # Since h is strictly increasing (h_{t-1} < h_t), we prefer higher counts.
        # However, we might have many players and few cards, or few players and many cards.
        # This is a variation of the knapsack problem or resource allocation.
        # Since k is small (<= 10), we can use dynamic programming.
        
        # Let dp[i][j] = max joy using first i players and having used j cards.
        # i ranges from 0 to interested_players.
        # j ranges from 0 to available_cards (and also <= i*k, but bounded by available_cards).
        
        # Transition:
        # For player i (1-indexed), we can give them t cards, where 0 <= t <= min(k, available_cards - j).
        # dp[i][j + t] = max(dp[i][j + t], dp[i-1][j] + h[t])
        
        # Optimization:
        # interested_players can be up to n (500).
        # available_cards can be up to n*k (5000).
        # DP state space: 500 * 5000 = 2.5 million. Transitions: k (10).
        # Total operations: 25 million. This is acceptable for Python within 1-2 seconds.
        
        # Let's implement this DP.
        
        num_players = interested_players
        num_cards = available_cards
        
        # dp[j] = max joy with j cards distributed so far
        # Initialize with -infinity, dp[0] = 0
        dp = [-float('inf')] * (num_cards + 1)
        dp[0] = 0
        
        # Precompute valid t for each step? No, t is always 0..k.
        # But we must ensure we don't exceed num_cards.
        
        for p in range(num_players):
            # Create new_dp for current player
            new_dp = [-float('inf')] * (num_cards + 1)
            
            # Current max cards we could have distributed before this player
            # Actually, we iterate j from 0 to num_cards
            # But we can optimize the range.
            # Before this player, we could have distributed at most p*k cards.
            # Also at most num_cards.
            # So j goes up to min(num_cards, p*k).
            
            max_prev = min(num_cards, p * k)
            
            for j in range(max_prev + 1):
                if dp[j] == -float('inf'):
                    continue
                
                # Try giving t cards to current player
                # t can be from 0 to k
                # Also j + t <= num_cards
                limit = min(k, num_cards - j)
                
                for t in range(limit + 1):
                    val = dp[j] + h[t]
                    if val > new_dp[j + t]:
                        new_dp[j + t] = val
            
            dp = new_dp
            
        # The answer for this number is the max value in dp array
        current_max = 0
        for val in dp:
            if val > current_max:
                current_max = val
        total_joy += current_max

    print(total_joy)

if __name__ == '__main__':
    solve()