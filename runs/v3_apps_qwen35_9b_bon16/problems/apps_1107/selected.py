import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    
    # Identify the indices (0-based) where Vasya (player 0) makes a move
    # Player 0 moves at turns 1, 1+n, 1+2n, ...
    # Turn number j (1-based) corresponds to index j-1 in string s.
    # So Vasya moves at indices 0, n, 2n, ...
    
    vasya_indices = [i for i in range(0, len(s), n)]
    
    max_juice = 0
    
    # Try all possible combinations of moves for Vasya's turns
    # Each turn has 2 possibilities: 'a' or 'b'
    # Since n <= 2000 and game length <= 2000, max turns is 2000.
    # Max Vasya turns = ceil(2000/n). For n=4, max 500 turns. 2^500 is too big.
    # However, the condition to drink juice depends only on the last 3 moves.
    # This is a dynamic programming problem or a sliding window approach.
    # We need to maximize juice for Vasya.
    # Let dp[i][last3] = max juice Vasya can get from turn i to end, given the last 3 moves before turn i.
    # But the state "last 3 moves" includes moves by others which are fixed.
    # The state we need to track is the suffix of length 3 of the move history.
    # State: (index_in_game, last_3_moves_tuple) -> max future juice for Vasya.
    # Actually, we process forward. Let's use DP going forward.
    # dp[i][state] = boolean or count? We want max count.
    # Let's define dp[i][suffix] = maximum juice Vasya can get from turns i+1 onwards,
    # given that the moves at turns i-2, i-1, i form the sequence 'suffix'.
    # Wait, the decision at turn i (if Vasya's turn) affects whether he drinks juice at turn i
    # AND affects the suffix for future turns.
    # If it's not Vasya's turn, his move is fixed, so no choice, just update suffix and add juice if applicable (but he can't drink on non-Vasya turns).
    
    # Let's refine the state.
    # We iterate through turns 0 to L-1 (L = len(s)).
    # State: (current_turn_index, last_3_moves_string)
    # Value: max juice Vasya can get from current_turn_index to end.
    # Since L is up to 2000, we can memoize.
    # The "last_3_moves" can be represented as a string of length 3 (or fewer if at start).
    # Actually, we only need the last 3 moves to determine if the current move triggers a drink.
    # Condition: if j >= 4 (1-based) => index >= 3 (0-based) AND s[j-3]==s[j-2]==s[j-1]==s[j].
    
    from functools import lru_cache
    
    L = len(s)
    
    # Precompute which turns are Vasya's
    is_vasya = [False] * L
    for i in range(0, L, n):
        is_vasya[i] = True
        
    # We will use recursion with memoization.
    # turn: current turn index (0 to L-1)
    # history: string of last moves (length up to 3)
    # But history length varies. Let's normalize: always keep the last 3 moves.
    # If turn < 3, history can be padded or we just check length.
    # Actually, simpler: history is a tuple of the last 3 moves encountered so far.
    # If fewer than 3 moves have occurred, just store what we have.
    # However, for consistency in the state key, maybe pad with a special char or just use tuple of variable length.
    # Given constraints, let's use a tuple of the last 3 moves. If less than 3, pad with None or just use the existing ones.
    # Better: state_key = (turn, tuple of last up to 3 moves).
    
    # But wait, the condition "if j >= 4 and ... same moves" implies we look back 3 turns.
    # So we need the moves at turn-1, turn-2, turn-3.
    # If current turn is t, we need moves at t-1, t-2, t-3.
    # If t < 3, condition fails automatically.
    
    # DP state: dp(turn, last_3) -> max future juice
    # last_3: tuple (m1, m2, m3) where m1 is move at turn-1, m2 at turn-2, m3 at turn-3.
    # If turn-1 doesn't exist, use a placeholder (e.g., None).
    
    memo = {}
    
    def get_max_juice(turn, last_1, last_2, last_3):
        # last_1, last_2, last_3 are characters or None
        state = (turn, last_1, last_2, last_3)
        if state in memo:
            return memo[state]
        
        if turn >= L:
            return 0
        
        current_char = s[turn]
        
        if is_vasya[turn]:
            # Vasya can choose 'a' or 'b'
            best = 0
            for choice in ['a', 'b']:
                # Check if he drinks juice on this turn
                drink = 0
                if turn >= 3:
                    # Check if last 3 moves + current are all same
                    # Moves at turn-1, turn-2, turn-3, turn
                    # last_1 is turn-1, last_2 is turn-2, last_3 is turn-3
                    if last_1 == last_2 == last_3 == choice:
                        drink = 1
                
                # Recurse
                future = get_max_juice(turn + 1, choice, last_1, last_2)
                total = drink + future
                if total > best:
                    best = total
            
            memo[state] = best
            return best
        else:
            # Not Vasya's turn, move is fixed to s[turn]
            drink = 0
            if turn >= 3:
                if last_1 == last_2 == last_3 == current_char:
                    drink = 0 # Vasya doesn't drink on non-Vasya turns
                    # Wait, the problem says "if the players who had turns number j - 1, j - 2, j - 3, made during their turns the same moves as player b_i on the current turn, then he had drunk a glass of juice"
                    # "he" refers to the player making the current turn (b_i).
                    # So Vasya only drinks on Vasya's turns.
                    # So if it's not Vasya's turn, he never drinks.
            
            # Prepare next state
            next_last_1 = current_char
            next_last_2 = last_1
            next_last_3 = last_2
            
            future = get_max_juice(turn + 1, next_last_1, next_last_2, next_last_3)
            
            memo[state] = future
            return future

    # Initial call: turn 0, no history
    # We can pass None, None, None
    result = get_max_juice(0, None, None, None)
    print(result)

if __name__ == '__main__':
    solve()