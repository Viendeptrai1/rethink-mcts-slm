import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # Determine who makes each turn
    # Turn 1 is by person 0, Turn 2 by person 1, etc.
    # Person index for turn j (1-based) is (j-1) % n
    # Vasya is person 0, so he moves on turns where (turn_index - 1) % n == 0
    # i.e., turn indices: 1, n+1, 2n+1, ...
    
    total_turns = len(s)
    
    # We need to decide the move for Vasya's turns to maximize his juice.
    # Juice is drunk if the current move equals the previous 3 moves.
    # The previous 3 moves are fixed by the input string for non-Vasya turns.
    # For Vasya's turns, we can choose 'a' or 'b'.
    
    # Let's parse the input string into a list of characters, but we will replace Vasya's moves with placeholders.
    # Actually, it's easier to simulate turn by turn.
    
    # State for DP:
    # We process turns from 1 to total_turns.
    # At any point, the "state" that affects future juice consumption is the last 3 moves made.
    # However, since we only care about Vasya's total juice, and the decision at turn t only affects:
    # 1. Whether Vasya drinks at turn t (if t is Vasya's turn and t >= 4)
    # 2. The sequence of last 3 moves for turns t+1, t+2, t+3...
    #
    # The "last 3 moves" can be represented as a tuple of 3 characters (or fewer if t < 4).
    # Since there are only 2 choices ('a', 'b'), the number of possible sequences of length up to 3 is small (2^3 = 8).
    #
    # DP state: dp[i][last_3] = maximum juice Vasya can get from turn i to the end,
    # given that the last 3 moves (moves at i-3, i-2, i-1) are 'last_3'.
    #
    # i ranges from 1 to total_turns + 1 (base case).
    # last_3 is a tuple of length 3 (we can pad with a special value or just handle lengths < 3).
    # To simplify, let's say last_3 always stores the last 3 moves. If fewer than 3 moves have been made,
    # we can pad with a dummy character that won't match 'a' or 'b', say '#'.
    # But actually, the condition "j >= 4 and moves j-1, j-2, j-3 are same as current" implies we need exactly 3 previous moves.
    # If j < 4, juice is never drunk.
    #
    # Let's define the state as (turn_index, last_3_moves_tuple).
    # last_3_moves_tuple will be a tuple of length 3.
    # For turn 1: previous moves are empty. We can represent this as ('#','#','#').
    #
    # Transitions:
    # From state (i, prev_3) where prev_3 = (m_{i-3}, m_{i-2}, m_{i-1}):
    # We are about to make move m_i at turn i.
    # If i is Vasya's turn:
    #   We try m_i = 'a' and m_i = 'b'.
    #   Calculate juice gained at this turn:
    #     if i >= 4 and m_i == m_{i-1} == m_{i-2} == m_{i-3}:
    #         juice = 1
    #     else:
    #         juice = 0
    #   New state for next turn: (i+1, (m_{i-2}, m_{i-1}, m_i))
    #   dp[i][prev_3] = max(dp[i][prev_3], juice + dp[i+1][new_prev_3])
    # If i is NOT Vasya's turn:
    #   The move m_i is fixed from the input string s (0-indexed: s[i-1]).
    #   Calculate juice (always 0 for Vasya since it's not his turn).
    #   New state: (i+1, (m_{i-2}, m_{i-1}, m_i))
    #   dp[i][prev_3] = juice + dp[i+1][new_prev_3]
    #
    # Base case:
    # dp[total_turns + 1][any] = 0
    
    # Mapping:
    # turn index i (1-based) corresponds to s[i-1]
    # Vasya moves if (i-1) % n == 0
    
    # We can use a dictionary for DP to handle sparse states or a 2D array if we map tuples to integers.
    # Since the tuple is always length 3 and chars are 'a', 'b', '#', we can map:
    # 'a' -> 0, 'b' -> 1, '#' -> 2.
    # Tuple of 3 ints -> integer key.
    
    # Let's implement with a dictionary for clarity and simplicity given the small state space.
    
    # Initial state: turn 1, previous 3 moves are ['#', '#', '#']
    # We'll use a memoization dictionary.
    
    memo = {}
    
    def get_key(last_3):
        # last_3 is a tuple of 3 chars
        # Convert to integer key
        # 'a': 0, 'b': 1, '#': 2
        mapping = {'a': 0, 'b': 1, '#': 2}
        return (mapping[last_3[0]], mapping[last_3[1]], mapping[last_3[2]])
    
    def dp(turn_idx, last_3):
        if turn_idx > total_turns:
            return 0
        
        state_key = get_key(last_3)
        if state_key in memo:
            return memo[state_key]
        
        # Determine whose turn it is
        # turn_idx is 1-based
        person_idx = (turn_idx - 1) % n
        is_vasya = (person_idx == 0)
        
        # Get the fixed move if not Vasya
        if not is_vasya:
            # Move is fixed from input
            # s is 0-indexed, so move is s[turn_idx - 1]
            fixed_move = s[turn_idx - 1]
            
            # Calculate juice for this turn
            # Condition: turn_idx >= 4 and current == prev1 == prev2 == prev3
            # last_3 is (m_{i-3}, m_{i-2}, m_{i-1})
            # current is fixed_move
            juice = 0
            if turn_idx >= 4:
                if fixed_move == last_3[0] and fixed_move == last_3[1] and fixed_move == last_3[2]:
                    # But wait, the problem says "if j >= 4 and the players who had turns number j - 1, j - 2, j - 3, made during their turns the same moves as player b_i on the current turn"
                    # This means m_j == m_{j-1} == m_{j-2} == m_{j-3}.
                    # Our last_3 is (m_{j-3}, m_{j-2}, m_{j-1}).
                    # So we check if fixed_move == last_3[0] and fixed_move == last_3[1] and fixed_move == last_3[2].
                    # However, note that if any of the previous moves were '#' (padding), they won't match 'a' or 'b', so juice won't be counted incorrectly for early turns.
                    # But we must ensure that the padding '#' doesn't accidentally match if we didn't pad correctly.
                    # Since 'a' and 'b' are never '#', if any of last_3 is '#', the condition fails.
                    # This is correct because for j < 4, we shouldn't count juice, and our padding ensures that.
                    juice = 1 if is_vasya else 0 # Only Vasya gets juice
            
            # Next state
            new_last_3 = (last_3[1], last_3[2], fixed_move)
            res = juice + dp(turn_idx + 1, new_last_3)
            memo[state_key] = res
            return res
        
        else:
            # Vasya's turn, he can choose 'a' or 'b'
            best_res = 0
            
            for choice in ['a', 'b']:
                # Calculate juice
                juice = 0
                if turn_idx >= 4:
                    if choice == last_3[0] and choice == last_3[1] and choice == last_3[2]:
                        juice = 1
                
                # Next state
                new_last_3 = (last_3[1], last_3[2], choice)
                res = juice + dp(turn_idx + 1, new_last_3)
                if res > best_res:
                    best_res = res
            
            memo[state_key] = best_res
            return best_res

    # Initial call
    # Turn 1, last_3 = ('#', '#', '#')
    result = dp(1, ('#', '#', '#'))
    print(result)

if __name__ == '__main__':
    solve()